
# ============================================
# FICHIER : backend/app/api/team.py
# ============================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.models import Team, Player, Match
from app.schemas.team import TeamCreate, TeamUpdate, TeamResponse
from app.api.deps import get_current_admin

router = APIRouter(prefix="/teams", tags=["teams"])

@router.post("/", response_model=TeamResponse)
def create_team(team_data: TeamCreate, db: Session = Depends(get_db), current_admin = Depends(get_current_admin)):
    # Vérifier que les joueurs existent
    player1 = db.query(Player).filter(Player.id == team_data.player1_id).first()
    if not player1:
        raise HTTPException(status_code=404, detail="Joueur 1 introuvable")
    
    player2 = db.query(Player).filter(Player.id == team_data.player2_id).first()
    if not player2:
        raise HTTPException(status_code=404, detail="Joueur 2 introuvable")
    
    # Vérifier que les deux joueurs sont différents
    if team_data.player1_id == team_data.player2_id:
        raise HTTPException(status_code=400, detail="Les deux joueurs doivent être différents")
    
    # Vérifier qu'une équipe avec les mêmes joueurs et entreprise n'existe pas déjà
    existing_team = db.query(Team).filter(
        Team.company == team_data.company,
        ((Team.player1_id == team_data.player1_id) & (Team.player2_id == team_data.player2_id)) |
        ((Team.player1_id == team_data.player2_id) & (Team.player2_id == team_data.player1_id))
    ).first()
    if existing_team:
        raise HTTPException(status_code=409, detail="Une équipe avec ces joueurs et cette entreprise existe déjà")
    
    # Créer l'équipe
    db_team = Team(
        company=team_data.company,
        player1_id=team_data.player1_id,
        player2_id=team_data.player2_id,
        pool_id=team_data.pool_id
    )
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

@router.get("/", response_model=List[TeamResponse])
def get_teams(db: Session = Depends(get_db)):
    teams = db.query(Team).all()
    return teams

@router.get("/{team_id}", response_model=TeamResponse)
def get_team(team_id: int, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Équipe introuvable")
    return team

@router.put("/{team_id}", response_model=TeamResponse)
def update_team(team_id: int, team_data: TeamUpdate, db: Session = Depends(get_db), current_admin = Depends(get_current_admin)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Équipe introuvable")
    
    # Vérifier si on change les joueurs
    changing_players = (team_data.player1_id is not None and team_data.player1_id != team.player1_id) or \
                       (team_data.player2_id is not None and team_data.player2_id != team.player2_id)
    
    if changing_players:
        # Vérifier si l'équipe a joué des matchs
        matches_count = db.query(Match).filter(
            (Match.team1_id == team_id) | (Match.team2_id == team_id)
        ).count()
        if matches_count > 0:
            raise HTTPException(status_code=400, detail="Impossible de changer les joueurs car l'équipe a déjà joué des matchs")
        
        # Vérifier que les nouveaux joueurs existent
        if team_data.player1_id is not None:
            player1 = db.query(Player).filter(Player.id == team_data.player1_id).first()
            if not player1:
                raise HTTPException(status_code=404, detail="Nouveau joueur 1 introuvable")
        
        if team_data.player2_id is not None:
            player2 = db.query(Player).filter(Player.id == team_data.player2_id).first()
            if not player2:
                raise HTTPException(status_code=404, detail="Nouveau joueur 2 introuvable")
        
        # Vérifier que les deux joueurs sont différents
        new_player1_id = team_data.player1_id if team_data.player1_id is not None else team.player1_id
        new_player2_id = team_data.player2_id if team_data.player2_id is not None else team.player2_id
        if new_player1_id == new_player2_id:
            raise HTTPException(status_code=400, detail="Les deux joueurs doivent être différents")
    
    # Mettre à jour les champs
    for key, value in team_data.model_dump(exclude_unset=True).items():
        setattr(team, key, value)
    
    db.commit()
    db.refresh(team)
    return team

@router.delete("/{team_id}")
def delete_team(team_id: int, db: Session = Depends(get_db), current_admin = Depends(get_current_admin)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Équipe introuvable")
    
    # Vérifier si l'équipe a joué des matchs
    matches_count = db.query(Match).filter(
        (Match.team1_id == team_id) | (Match.team2_id == team_id)
    ).count()
    if matches_count > 0:
        raise HTTPException(status_code=400, detail="Impossible de supprimer l'équipe car elle a déjà joué des matchs")
    
    db.delete(team)
    db.commit()
    return {"message": "Équipe supprimée"}