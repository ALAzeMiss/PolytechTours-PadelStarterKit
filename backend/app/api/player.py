from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.database import get_db
from app.models.models import Player, User
from app.schemas.player import PlayerCreate, PlayerUpdate, PlayerResponse
from app.api.deps import get_current_admin


router = APIRouter(prefix="/players", tags=["players"])

@router.get("/", response_model=List[PlayerResponse])
def get_players(db: Session = Depends(get_db)):
    players = db.query(Player).options(joinedload(Player.user)).all()
    # Définir email pour chaque player
    for player in players:
        if player.user:
            player.email = player.user.email
    return players

@router.get("/{player_id}", response_model=PlayerResponse)
def get_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).options(joinedload(Player.user)).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    if player.user:
        player.email = player.user.email
    return player

@router.post("/", response_model=PlayerResponse)
def create_player(player_data: PlayerCreate, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    # Vérifier si l'utilisateur existe
    user = db.query(User).filter(User.id == player_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Aucun compte existant est associé à cette adresse email")
    
    # Vérifier si l'utilisateur a déjà un joueur
    existing_player = db.query(Player).filter(Player.user_id == player_data.user_id).first()
    if existing_player:
        raise HTTPException(status_code=409, detail="Un joueur est déjà associé à ce compte")
    
    # Vérifier l'unicité de la licence si fournie
    if player_data.license_number:
        existing_license = db.query(Player).filter(Player.license_number == player_data.license_number).first()
        if existing_license:
            raise HTTPException(status_code=409, detail="Cette licence est déjà associée à un joueur")
    
    db_player = Player(
        first_name=player_data.first_name,
        last_name=player_data.last_name,
        company=player_data.company,
        license_number=player_data.license_number,
        birth_date=player_data.birth_date,
        photo_url=player_data.photo_url,
        user_id=player_data.user_id
    )
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    # Charger user pour email
    db.refresh(db_player, attribute_names=['user'])
    if db_player.user:
        db_player.email = db_player.user.email
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
