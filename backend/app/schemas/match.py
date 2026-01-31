# ============================================
# FICHIER : backend/app/schemas/match.py
# ============================================

from pydantic import BaseModel, Field, field_validator
from typing import Optional, Union
from enum import Enum
from datetime import date, time, datetime
from app.schemas.team import TeamInfo

class MatchStatus(str, Enum):
    A_VENIR = "A_VENIR"
    ANNULE = "ANNULE"
    TERMINE = "TERMINE"

class MatchBase(BaseModel):
    match_date: date = Field(..., description="Date du match (YYYY-MM-DD)")
    match_time: Union[time, str] = Field(..., description="Heure du match (HH:MM)")
    court_number: int = Field(..., ge=1, le=10, description="Numéro de piste (1-10)")
    status: MatchStatus = MatchStatus.A_VENIR
    score_team1: Optional[str] = Field(None, description='Format: "6-4, 3-6, 7-5"')
    score_team2: Optional[str] = Field(None, description='Format: "4-6, 6-3, 5-7"')

    @field_validator('match_time', mode='before')
    @classmethod
    def parse_time(cls, v):
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%H:%M').time()
            except ValueError:
                raise ValueError('Format d\'heure invalide, utilisez HH:MM')
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
    score_team1: Optional[str] = Field(None, description='Format: "6-4, 3-6, 7-5"')
    score_team2: Optional[str] = Field(None, description='Format: "4-6, 6-3, 5-7"')

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