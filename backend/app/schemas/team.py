# ============================================
# FICHIER : backend/app/schemas/team.py
# ============================================

from pydantic import BaseModel
from typing import Optional
from app.schemas.player import PlayerInfo

class TeamBase(BaseModel):
    company: Optional[str] = None
    pool_id: Optional[int] = None
    

class TeamCreate(TeamBase):
    player1_id: int
    player2_id: int

class TeamUpdate(BaseModel):
    company: Optional[str] = None
    pool_id: Optional[int] = None
    player1_id: Optional[int] = None
    player2_id: Optional[int] = None

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