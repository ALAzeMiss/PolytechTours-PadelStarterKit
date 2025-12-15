# ============================================
# FICHIER : backend/app/schemas/player.py
# ============================================

from pydantic import BaseModel
from datetime import date
from typing import Optional

class PlayerBase(BaseModel):
    first_name: str
    last_name: str
    company: Optional[str] = None
    license_number: Optional[str] = None
    birth_date: Optional[date] = None
    photo_url: Optional[str] = None

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

    class Config:
        from_attributes = True

# Schéma simplifié pour l'affichage dans les matchs
class PlayerInfo(BaseModel):
    id: int
    first_name: str
    last_name: str
    
    class Config:
        from_attributes = True