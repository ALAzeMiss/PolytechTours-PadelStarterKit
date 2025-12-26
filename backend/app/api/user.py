# ============================================
# FICHIER : backend/app/api/user.py
# ============================================

from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User, LoginAttempt
from app.schemas.auth import LoginRequest, TokenResponse, UserResponse, ChangePasswordRequest, UserResponse
from app.schemas.user import CreateUserRequest, CreateUserResponse, UserSelectResponse
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
    print(user_data.email)
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
        must_change_password=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return CreateUserResponse(
        user=UserResponse.from_orm(new_user),
        temporary_password=temporary_password
    )

@router.get("/users/select", response_model=list[UserSelectResponse])
def get_users_for_select(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.get("/users", response_model=List[UserResponse])
def getUsers(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    is_active: Optional[bool] = None,
    is_admin: Optional[bool] = None,
    search: Optional[str] = None,  # recherche simple sur l'email
):
    query = db.query(User)

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    if is_admin is not None:
        query = query.filter(User.is_admin == is_admin)

    if search:
        query = query.filter(User.email.ilike(f"%{search}%"))

    users = (
        query.order_by(User.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    # UserResponse est un pydantic model -> renvoyer une liste d'objets "compatibles"
    return [UserResponse.from_orm(u) for u in users]