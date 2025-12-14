# ============================================
# FICHIER : backend/app/schemas/match.py
# ============================================

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from enum import Enum
from datetime import date, time, datetime
from app.schemas.team import TeamInfo
import re

class MatchStatus(str, Enum):
    A_VENIR = "A_VENIR"
    ANNULE = "ANNULE"
    TERMINE = "TERMINE"

class MatchBase(BaseModel):
    match_date: date = Field(..., description="Date du match (YYYY-MM-DD)")
    match_time: time = Field(..., description="Heure du match (HH:MM)")
    court_number: int = Field(..., ge=1, le=10, description="Numéro de piste (1-10)")
    status: MatchStatus = MatchStatus.A_VENIR
    score_team1: Optional[str] = Field(None, description="Score équipe 1 (format: '6-4, 6-3' ou '6-4, 3-6, 7-5')")
    score_team2: Optional[str] = Field(None, description="Score équipe 2 (format: '6-4, 6-3' ou '6-4, 3-6, 7-5')")

    @field_validator('score_team1', 'score_team2')
    @classmethod
    def validate_score_format(cls, v):
        if v is None:
            return v
        
        # Format attendu : "X-Y, X-Y" ou "X-Y, X-Y, X-Y"
        pattern = r'^\d+-\d+(,\s*\d+-\d+){1,2}$'
        if not re.match(pattern, v):
            raise ValueError('Le score doit être au format "X-Y, X-Y" ou "X-Y, X-Y, X-Y"')
        
        # Valider chaque set
        sets = [s.strip() for s in v.split(',')]
        if len(sets) < 2 or len(sets) > 3:
            raise ValueError('Un match doit avoir 2 ou 3 sets')
        
        for set_score in sets:
            games = set_score.split('-')
            if len(games) != 2:
                raise ValueError('Chaque set doit être au format X-Y')
            
            try:
                x, y = int(games[0]), int(games[1])
                
                # Le vainqueur doit avoir au moins 6 jeux
                if max(x, y) < 6:
                    raise ValueError('Le vainqueur d\'un set doit avoir au moins 6 jeux')
                
                # Si un set se termine 7-X, X doit être <= 5
                if x == 7 and y > 5:
                    raise ValueError('Si un set se termine 7-X, X doit être <= 5')
                if y == 7 and x > 5:
                    raise ValueError('Si un set se termine 7-X, X doit être <= 5')
                
                # Si un set se termine 7-6, c'est un tie-break (valide)
                # Les autres cas > 7 ne sont pas autorisés
                if x > 7 or y > 7:
                    raise ValueError('Un score de set ne peut pas dépasser 7')
                    
            except ValueError as e:
                if 'invalid literal' in str(e):
                    raise ValueError('Les scores doivent être des nombres entiers')
                raise
        
        return v

    @field_validator('match_date')
    @classmethod
    def validate_date_not_past(cls, v):
        if v < datetime.now().date():
            raise ValueError('La date du match ne peut pas être dans le passé')
        return v

class MatchCreate(MatchBase):
    team1_id: int
    team2_id: int
    event_id: Optional[int] = None

    @field_validator('team2_id')
    @classmethod
    def validate_different_teams(cls, v, info):
        if 'team1_id' in info.data and v == info.data['team1_id']:
            raise ValueError('Les deux équipes doivent être différentes')
        return v

class MatchUpdate(BaseModel):
    match_date: Optional[date] = None
    match_time: Optional[time] = None
    court_number: Optional[int] = Field(None, ge=1, le=10)
    status: Optional[MatchStatus] = None
    score_team1: Optional[str] = Field(None, description="Score équipe 1")
    score_team2: Optional[str] = Field(None, description="Score équipe 2")

class MatchResponse(MatchBase):
    id: int
    team1_id: int
    team2_id: int
    event_id: Optional[int]

    class Config:
        from_attributes = True

# Schéma de réponse détaillée pour l'affichage
class MatchDetailResponse(BaseModel):
    id: int
    match_date: date
    match_time: time
    court_number: int
    status: MatchStatus
    score_team1: Optional[str]
    score_team2: Optional[str]
    team1: TeamInfo
    team2: TeamInfo
    event_id: Optional[int]

    class Config:
        from_attributes = True