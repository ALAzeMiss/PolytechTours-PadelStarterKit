# ============================================
# FICHIER : backend/app/schemas/pool.py
# ============================================

from pydantic import BaseModel
from datetime import datetime

class PoolBase(BaseModel):
    id: str

class PoolCreate(PoolBase):
    pass

class PoolResponse(PoolBase):
    created_at: datetime

    class Config:
        from_attributes = True