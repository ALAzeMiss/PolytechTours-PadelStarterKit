# ============================================
# FICHIER : backend/app/api/auth.py
# ============================================
 
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User, LoginAttempt
from app.schemas.auth import LoginRequest, TokenResponse, UserResponse, ChangePasswordRequest
from app.core.security import verify_password, get_password_hash, create_access_token
from app.api.deps import get_current_user
 
router = APIRouter()
 
MAX_ATTEMPTS = 5
LOCKOUT_MINUTES = 30
 
def check_attempts_before_login(db: Session, email: str):
    """Étape 1 : Vérifier si l'IP/Email est déjà bloqué avant même de tester le mdp"""
    attempt = db.query(LoginAttempt).filter(LoginAttempt.email == email).first()
   
    if attempt and attempt.locked_until:
        now = datetime.utcnow()
        if attempt.locked_until > now:
            minutes_remaining = int((attempt.locked_until - now).total_seconds() / 60)
            # On renvoie 403 car c'est un blocage temporaire
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "message": "Compte temporairement bloqué",
                    "locked_until": attempt.locked_until.isoformat(),
                    "minutes_remaining": minutes_remaining
                }
            )
    return attempt
 
def record_failed_attempt(db: Session, email: str):
    """Enregistre un échec et bloque si nécessaire"""
    attempt = db.query(LoginAttempt).filter(LoginAttempt.email == email).first()
   
    if not attempt:
        attempt = LoginAttempt(email=email)
        db.add(attempt)
   
    now = datetime.utcnow()
    attempt.attempts_count += 1
    attempt.last_attempt = now
   
    # Vérification si on dépasse la limite
    if attempt.attempts_count >= MAX_ATTEMPTS:
        attempt.locked_until = now + timedelta(minutes=LOCKOUT_MINUTES)
        db.commit()
        # On lève une 403 ici car le compte vient de passer en mode bloqué
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": f"Trop de tentatives. Compte bloqué {LOCKOUT_MINUTES} min.",
                "minutes_remaining": LOCKOUT_MINUTES
            }
        )
   
    db.commit()
    # On retourne le nombre d'essais restants pour l'affichage
    return MAX_ATTEMPTS - attempt.attempts_count
 
def reset_attempts(db: Session, email: str):
    """Réinitialise le compteur en cas de succès"""
    attempt = db.query(LoginAttempt).filter(LoginAttempt.email == email).first()
    if attempt:
        attempt.attempts_count = 0
        attempt.locked_until = None
        db.commit()
 
@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    # 1. Vérifier si le compte est DÉJÀ bloqué (avant même de vérifier le mdp)
    check_attempts_before_login(db, credentials.email)
 
    # 2. Récupérer l'utilisateur
    user = db.query(User).filter(User.email == credentials.email).first()
 
    # 3. Vérification unifiée (Existe + Mot de passe)
    # On utilise une variable pour savoir si c'est valide ou non
    is_valid_user = False
    print("user is : ", User)
    print("password verified : ", verify_password(credentials.password, user.password_hash))

    if user and verify_password(credentials.password, user.password_hash):
        is_valid_user = True
 
    # 4. Si invalide : On enregistre l'échec et on lève l'erreur
    if not is_valid_user:
        attempts_remaining = record_failed_attempt(db, credentials.email)
       
        # ICI : On utilise 400 (Bad Request) pour éviter le refresh du frontend
        # Et on ne dit pas si c'est l'email ou le mdp qui est faux
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Email ou mot de passe incorrect",
                "attempts_remaining": attempts_remaining
            }
        )
 
    # 5. Si valide mais inactif (Cas spécifique)
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Compte désactivé. Contactez l'administrateur."
        )
 
    # 6. Tout est bon : Reset des tentatives et Token
    reset_attempts(db, credentials.email)
   
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email,
            "is_admin": user.is_admin,
            "must_change_password": user.must_change_password
        }
    )
   
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.from_orm(user)
    )
 
@router.post("/change-password")
def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change le mot de passe de l'utilisateur connecté"""
   
    # Vérifier le mot de passe actuel
    if not verify_password(request.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mot de passe actuel incorrect"
        )
   
    # Vérifier que le nouveau mot de passe est différent
    if verify_password(request.new_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le nouveau mot de passe doit être différent de l'ancien"
        )
   
    # Mettre à jour le mot de passe
    current_user.password_hash = get_password_hash(request.new_password)
    current_user.must_change_password = False
    db.commit()
   
    return {"message": "Mot de passe modifié avec succès"}
 
@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    """Déconnecte l'utilisateur (côté client, suppression du token)"""
    return {"message": "Déconnexion réussie"}