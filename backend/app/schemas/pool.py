# ============================================
# FICHIER : backend/app/schemas/pool.py
# ============================================

from pydantic import BaseModel, field_validator
from datetime import datetime
import re

class PoolBase(BaseModel):
    name: str

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v:
            raise ValueError('Veuillez renseigner un nom de poule')
        if not re.match(r'^[a-zA-ZÀ-ÿ0-9\s\'-]{2,50}$', v):
            raise ValueError('Nom de poule invalide')
        return v


class PoolCreate(PoolBase):
    team_ids: list[int] = []

    @field_validator('team_ids')
    @classmethod
    def validate_team_ids(cls, v):
        if not isinstance(v, list):
            raise ValueError('team_ids doit être une liste')
        for id in v:
            if not isinstance(id, int) or id <= 0:
                raise ValueError('Chaque ID d\'équipe doit être un entier positif')
        return v

class PoolResponse(PoolBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True