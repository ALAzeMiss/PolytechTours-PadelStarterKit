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
from app.models.models import User, Match

router = APIRouter(prefix="/matches", tags=["matches"])

def build_match_response(match: Match) -> MatchDetailResponse:
    """Construit une réponse MatchDetailResponse à partir d'un objet Match."""
    try:
        # Vérifier que toutes les équipes existent
        if not match.team1 or not match.team2:
            raise ValueError("Match incomplet: équipes manquantes")
        
        # Fonction helper pour obtenir les infos du joueur (avec fallback si manquant)
        def get_player_info(player):
            if not player:
                return PlayerInfo(id=0, first_name="Joueur", last_name="Manquant")
            return PlayerInfo(
                id=player.id,
                first_name=player.first_name,
                last_name=player.last_name
            )
        
        # Fonction helper pour obtenir les infos de l'équipe
        def get_team_info(team):
            return TeamInfo(
                id=team.id,
                company=team.company,
                player1=get_player_info(team.player1),
                player2=get_player_info(team.player2)
            )
        
        return MatchDetailResponse(
            id=match.id,
            match_date=match.match_date,
            match_time=match.match_time,
            court_number=match.court_number,
            status=match.status,
            score_team1=match.score_team1,
            score_team2=match.score_team2,
            team1=get_team_info(match.team1),
            team2=get_team_info(match.team2),
            event_id=match.event_id
        )
    except Exception as e:
        print(f"ERROR building match response for match {match.id}: {str(e)}")
        raise

@router.get("/", response_model=List[MatchDetailResponse])
def read_upcoming_matches(
    show_all: bool = Query(False, description="Afficher tous les matchs (pour les joueurs)"),
    company: Optional[str] = Query(None, description="Filtrer par entreprise"),
    pool_id: Optional[int] = Query(None, description="Filtrer par poule"),
    status: Optional[str] = Query(None, description="Filtrer par statut"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère la liste des matchs à venir dans les 30 prochains jours.
    """
    try:
        print(f"[DEBUG] Requête matchs - user: {current_user.email}, admin: {current_user.is_admin}, show_all: {show_all}")
        
        matches = get_upcoming_matches(
            db=db,
            user=current_user,
            show_all=show_all,
            company_filter=company,
            pool_filter=pool_id,
            status_filter=status
        )
        
        print(f"[DEBUG] {len(matches)} matchs trouvés en base")
        
        result = []
        for i, match in enumerate(matches):
            try:
                response = build_match_response(match)
                result.append(response)
            except Exception as e:
                print(f"[ERROR] Erreur pour match {match.id}: {str(e)}")
                raise
        
        print(f"[DEBUG] Retour de {len(result)} matchs au frontend")
        return result
    except Exception as e:
        print(f"[ERROR] Exception dans read_upcoming_matches: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{match_id}", response_model=MatchDetailResponse)
def read_match(
    match_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère un match par son ID.
    """
    match = get_match_by_id(db, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match introuvable")

    return build_match_response(match)


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
    
    return build_match_response(match)


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
    
    return build_match_response(match)


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