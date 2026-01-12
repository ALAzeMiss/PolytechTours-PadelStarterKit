# ============================================
# FICHIER : backend/app/schemas/team.py
# ============================================

from pydantic import BaseModel, field_validator
from typing import Optional
import re
from app.schemas.player import PlayerInfo

class TeamBase(BaseModel):
    company: str
    pool_id: Optional[int] = None

    @field_validator('company')
    @classmethod
    def validate_company(cls, v):
        if not v:
            raise ValueError('Veuillez renseigner une entreprise')
        if not re.match(r'^[a-zA-ZÀ-ÿ0-9\s\'-]{2,100}$', v):
            raise ValueError('Nom d\'entreprise invalide')
        return v
    

class TeamCreate(TeamBase):
    player1_id: int
    player2_id: int

    @field_validator('player1_id', 'player2_id')
    @classmethod
    def validate_player_ids(cls, v):
        if v <= 0:
            raise ValueError('ID de joueur invalide')
        return v

class TeamUpdate(BaseModel):
    company: Optional[str] = None
    pool_id: Optional[int] = None
    player1_id: Optional[int] = None
    player2_id: Optional[int] = None

    @field_validator('company')
    @classmethod
    def validate_company(cls, v):
        if v is not None:
            if not v:
                raise ValueError('Veuillez renseigner une entreprise')
            if not re.match(r'^[a-zA-ZÀ-ÿ0-9\s\'-]{2,100}$', v):
                raise ValueError('Nom d\'entreprise invalide')
        return v

    @field_validator('player1_id', 'player2_id')
    @classmethod
    def validate_player_ids(cls, v):
        if v is not None and v <= 0:
            raise ValueError('ID de joueur invalide')
        return v

class TeamResponse(TeamBase):
    id: int
    player1_id: int
    player2_id: int

    class Config:
        from_attributes = True

# Schéma pour l'affichage détaillé dans les matchs
class TeamInfo(BaseModel):
    id: int
    company: str
    player1: PlayerInfo
    player2: PlayerInfo

    class Config:
        from_attributes = True