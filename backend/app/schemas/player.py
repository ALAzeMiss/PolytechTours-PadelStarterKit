# ============================================
# FICHIER : backend/app/schemas/player.py
# ============================================

from pydantic import BaseModel, field_validator
from datetime import date
from typing import Optional
import re

class PlayerBase(BaseModel):
    first_name: str
    last_name: str
    company: str
    license_number: Optional[str] = None
    birth_date: Optional[date] = None
    photo_url: Optional[str] = None

    @field_validator('first_name')
    @classmethod
    def validate_first_name(cls, v):
        if not v:
            raise ValueError('Veuillez renseigner un prénom')
        if not re.match(r'^[a-zA-ZÀ-ÿ\s\'-]{2,50}$', v):
            raise ValueError('Prénom invalide')
        return v

    @field_validator('last_name')
    @classmethod
    def validate_last_name(cls, v):
        if not v:
            raise ValueError('Veuillez renseigner un nom')
        if not re.match(r'^[a-zA-ZÀ-ÿ\s\'-]{2,50}$', v):
            raise ValueError('Nom invalide')
        return v

    @field_validator('company')
    @classmethod
    def validate_company(cls, v):
        if not v:
            raise ValueError('Veuillez renseigner une entreprise')
        if not re.match(r'^[a-zA-ZÀ-ÿ0-9\s\'-]{2,100}$', v):
            raise ValueError('Nom d\'entreprise invalide')
        return v

    @field_validator('license_number')
    @classmethod
    def validate_license_number(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError('Veuillez renseigner une licence')
            if not re.match(r'^L\d{6}$', v):
                raise ValueError('Licence invalide')
        return v
    email: Optional[str] = None

class PlayerCreate(PlayerBase):
    user_id: int
    

class PlayerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    license_number: Optional[str] = None
    birth_date: Optional[date] = None
    photo_url: Optional[str] = None
    user_id: Optional[int] = None

class PlayerResponse(PlayerBase):
    id: int
    user_id: int
    email: Optional[str] = None

    class Config:
        from_attributes = True

# Schéma simplifié pour l'affichage dans les matchs
class PlayerInfo(BaseModel):
    id: int
    first_name: str
    last_name: str
    
    class Config:
        from_attributes = True