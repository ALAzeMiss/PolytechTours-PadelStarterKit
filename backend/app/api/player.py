# backend/app/api/players.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.models import Player
from app.schemas.player import PlayerCreate, PlayerUpdate, PlayerResponse

router = APIRouter(prefix="/players", tags=["players"])

@router.get("/", response_model=List[PlayerResponse])
def get_players(db: Session = Depends(get_db)):
    return db.query(Player).all()

@router.get("/{player_id}", response_model=PlayerResponse)
def get_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@router.post("/", response_model=PlayerResponse)
def create_player(player_data: PlayerCreate, db: Session = Depends(get_db)):
    db_player = Player(
        first_name=player_data.first_name,
        last_name=player_data.last_name,
        email=player_data.email,
        date_naissance=player_data.date_naissance,
        numero_licence=player_data.numero_licence,
        level=player_data.level
    )
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

@router.put("/{player_id}", response_model=PlayerResponse)
def update_player(player_id: int, player_data: PlayerUpdate, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    update_data = player_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        # adapte le nom si nécessaire (ex: numero_licence vs licenceNumber côté frontend)
        setattr(player, key, value)

    db.commit()
    db.refresh(player)
    return player

@router.delete("/{player_id}")
def delete_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    db.delete(player)
    db.commit()
    return {"status": "deleted"}
