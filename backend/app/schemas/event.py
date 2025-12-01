# ============================================
# FICHIER : backend/app/schemas/event.py
# ============================================

from pydantic import BaseModel
from datetime import date, time, datetime

class EventBase(BaseModel):
    event_date: date
    start_time: time

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True