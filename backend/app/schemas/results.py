# ============================================
# FICHIER : backend/app/schemas/results.py
# ============================================

from pydantic import BaseModel
from typing import Optional
from datetime import date, time

class PersonalResultResponse(BaseModel):
    """Schéma pour un résultat personnel de match"""
    id: int
    match_date: date
    match_time: time
    court_number: int
    adversary_company: str
    adversary_player1_name: str
    adversary_player2_name: str
    score_team1: Optional[str]
    score_team2: Optional[str]
    is_victory: bool
    user_team_id: int  # ID de l'équipe du joueur
    
    class Config:
        from_attributes = True


class CompanyRankingResponse(BaseModel):
    """Schéma pour le classement d'une entreprise"""
    position: int
    company: str
    matches_played: int
    victories: int
    defeats: int
    points: int
    sets_won: int  # Pour le tie-breaker
    sets_lost: int  # Pour le tie-breaker
    
    class Config:
        from_attributes = True
