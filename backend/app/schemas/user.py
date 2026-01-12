
# ============================================
# FICHIER : backend/app/schemas/user.py
# ============================================

from pydantic import BaseModel, EmailStr, validator
from app.schemas.auth import  UserResponse
import re


class CreateUserRequest(BaseModel):
    email: EmailStr
    is_admin: bool = False
    
    @validator('email')
    def validate_email(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("L'email ne peut pas être vide")
        return v.lower().strip()

class CreateUserResponse(BaseModel):
    user: UserResponse
    temporary_password: str
    
    class Config:
        from_attributes = True
        

class UserSelectResponse(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True


