# ============================================
# FICHIER : backend/app/api/user.py
# ============================================

from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User, LoginAttempt
from app.schemas.auth import LoginRequest, TokenResponse, UserResponse, ChangePasswordRequest, UserResponse
from app.schemas.user import CreateUserRequest, CreateUserResponse
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.security import get_password_hash
from app.api.deps import get_current_admin
import secrets
import string

router = APIRouter()


def generate_password(length: int = 12) -> str:
    # Génère un mot de passe sécurisé
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(secrets.choice(characters) for _ in range(length))
    
    if (any(c.isupper() for c in password) and 
        any(c.islower() for c in password) and 
        any(c.isdigit() for c in password) and 
        any(c in "!@#$%^&*" for c in password)):
        return password
    else:
        return generate_password(length)

@router.post("/users", response_model=CreateUserResponse)
def createUser(user_data: CreateUserRequest, db: Session = Depends(get_db),current_admin: User = Depends(get_current_admin) ):
    # Vérifier si l'email existe déjà
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email déjà utilisé")
    # Générer un mot de passe temporaire
    temporary_password = generate_password()
    
    # Créer le nouvel utilisateur
    new_user = User(
        email=user_data.email,
        password_hash=get_password_hash(temporary_password),
        is_admin=user_data.is_admin,
        is_active=False,
        must_change_password=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return CreateUserResponse(
        user=UserResponse.from_orm(new_user),
        temporary_password=temporary_password
    )
    

