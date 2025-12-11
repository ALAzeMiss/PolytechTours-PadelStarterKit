from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.crud.match import (
    get_upcoming_matches, 
    create_match, 
    update_match, 
    delete_match,
    get_match_by_id
)
from app.database import get_db
from app.schemas.match import MatchCreate, MatchUpdate, MatchDetailResponse
from app.schemas.team import TeamInfo
from app.schemas.player import PlayerInfo
from app.api.deps import get_current_user, get_current_admin
from app.models.models import User

router = APIRouter(tags=["matches"])

@router.get("/", response_model=List[MatchDetailResponse])
def read_upcoming_matches(
    show_all: bool = Query(False, description="Afficher tous les matchs (pour les joueurs)"),
    company: Optional[str] = Query(None, description="Filtrer par entreprise"),
    pool_id: Optional[str] = Query(None, description="Filtrer par poule"),
    status: Optional[str] = Query(None, description="Filtrer par statut"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère la liste des matchs à venir dans les 30 prochains jours.
    - Pour les joueurs : affiche uniquement leurs matchs par défaut (sauf si show_all=true)
    - Pour les admins : affiche tous les matchs avec possibilité de filtrer
    """
    matches = get_upcoming_matches(
        db=db,
        user=current_user,
        show_all=show_all,
        company_filter=company,
        pool_filter=pool_id,
        status_filter=status
    )
    
    # Construire la réponse détaillée
    result = []
    for match in matches:
        result.append(MatchDetailResponse(
            id=match.id,
            match_date=match.match_date,
            match_time=match.match_time,
            court_number=match.court_number,
            status=match.status,
            score_team1=match.score_team1,
            score_team2=match.score_team2,
            team1=TeamInfo(
                id=match.team1.id,
                company=match.team1.company,
                player1=PlayerInfo(
                    id=match.team1.player1.id,
                    first_name=match.team1.player1.first_name,
                    last_name=match.team1.player1.last_name
                ),
                player2=PlayerInfo(
                    id=match.team1.player2.id,
                    first_name=match.team1.player2.first_name,
                    last_name=match.team1.player2.last_name
                )
            ),
            team2=TeamInfo(
                id=match.team2.id,
                company=match.team2.company,
                player1=PlayerInfo(
                    id=match.team2.player1.id,
                    first_name=match.team2.player1.first_name,
                    last_name=match.team2.player1.last_name
                ),
                player2=PlayerInfo(
                    id=match.team2.player2.id,
                    first_name=match.team2.player2.first_name,
                    last_name=match.team2.player2.last_name
                )
            ),
            event_id=match.event_id
        ))
    
    return result


@router.post("/", response_model=MatchDetailResponse)
def create_new_match(
    match_data: MatchCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Crée un nouveau match.
    Réservé aux administrateurs.
    """
    match = create_match(db, match_data)
    
    # Recharger le match avec toutes les relations
    match = get_match_by_id(db, match.id)
    
    return MatchDetailResponse(
        id=match.id,
        match_date=match.match_date,
        match_time=match.match_time,
        court_number=match.court_number,
        status=match.status,
        score_team1=match.score_team1,
        score_team2=match.score_team2,
        team1=TeamInfo(
            id=match.team1.id,
            company=match.team1.company,
            player1=PlayerInfo(
                id=match.team1.player1.id,
                first_name=match.team1.player1.first_name,
                last_name=match.team1.player1.last_name
            ),
            player2=PlayerInfo(
                id=match.team1.player2.id,
                first_name=match.team1.player2.first_name,
                last_name=match.team1.player2.last_name
            )
        ),
        team2=TeamInfo(
            id=match.team2.id,
            company=match.team2.company,
            player1=PlayerInfo(
                id=match.team2.player1.id,
                first_name=match.team2.player1.first_name,
                last_name=match.team2.player1.last_name
            ),
            player2=PlayerInfo(
                id=match.team2.player2.id,
                first_name=match.team2.player2.first_name,
                last_name=match.team2.player2.last_name
            )
        ),
        event_id=match.event_id
    )


@router.patch("/{match_id}", response_model=MatchDetailResponse)
def update_existing_match(
    match_id: int,
    match_data: MatchUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Met à jour un match existant.
    Réservé aux administrateurs.
    """
    match = update_match(db, match_id, match_data)
    
    # Recharger avec toutes les relations
    match = get_match_by_id(db, match.id)
    
    return MatchDetailResponse(
        id=match.id,
        match_date=match.match_date,
        match_time=match.match_time,
        court_number=match.court_number,
        status=match.status,
        score_team1=match.score_team1,
        score_team2=match.score_team2,
        team1=TeamInfo(
            id=match.team1.id,
            company=match.team1.company,
            player1=PlayerInfo(
                id=match.team1.player1.id,
                first_name=match.team1.player1.first_name,
                last_name=match.team1.player1.last_name
            ),
            player2=PlayerInfo(
                id=match.team1.player2.id,
                first_name=match.team1.player2.first_name,
                last_name=match.team1.player2.last_name
            )
        ),
        team2=TeamInfo(
            id=match.team2.id,
            company=match.team2.company,
            player1=PlayerInfo(
                id=match.team2.player1.id,
                first_name=match.team2.player1.first_name,
                last_name=match.team2.player1.last_name
            ),
            player2=PlayerInfo(
                id=match.team2.player2.id,
                first_name=match.team2.player2.first_name,
                last_name=match.team2.player2.last_name
            )
        ),
        event_id=match.event_id
    )


@router.delete("/{match_id}")
def delete_existing_match(
    match_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Supprime un match.
    Possible uniquement si le statut est A_VENIR.
    Réservé aux administrateurs.
    """
    delete_match(db, match_id)
    return {"message": "Match supprimé avec succès"}