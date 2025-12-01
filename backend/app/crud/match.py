# ============================================
# FICHIER : backend/app/crud/match.py
# ============================================

from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from datetime import date, timedelta, datetime

from app.models.models import Match, Team, Player, Pool, User
from app.schemas.match import MatchCreate, MatchUpdate, MatchDetailResponse
from app.schemas.team import TeamInfo
from app.schemas.player import PlayerInfo


def check_court_availability(
    db: Session, 
    match_date: date, 
    match_time, 
    court_number: int, 
    exclude_match_id: int = None
) -> bool:
    """
    Vérifie si un terrain est disponible à une date et heure données.
    Retourne True si disponible, False sinon.
    """
    query = db.query(Match).filter(
        Match.match_date == match_date,
        Match.match_time == match_time,
        Match.court_number == court_number,
        Match.status != "ANNULE"  # On ne compte pas les matchs annulés
    )
    
    if exclude_match_id:
        query = query.filter(Match.id != exclude_match_id)
    
    existing_match = query.first()
    return existing_match is None


def get_upcoming_matches(
    db: Session,
    days: int = 30,
    user: User = None,
    show_all: bool = False,
    company_filter: str = None,
    pool_filter: int = None,
    status_filter: str = None
):
    """
    Récupère les matchs à venir dans les X prochains jours.
    Filtre selon le rôle de l'utilisateur et les paramètres demandés.
    """
    today = datetime.now().date()
    end_date = today + timedelta(days=days)
    
    # Requête de base avec jointures pour récupérer toutes les infos
    query = db.query(Match).options(
        joinedload(Match.team1).joinedload(Team.player1),
        joinedload(Match.team1).joinedload(Team.player2),
        joinedload(Match.team2).joinedload(Team.player1),
        joinedload(Match.team2).joinedload(Team.player2),
        joinedload(Match.team1).joinedload(Team.pools),
        joinedload(Match.team2).joinedload(Team.pools)
    ).filter(
        Match.match_date >= today,
        Match.match_date <= end_date
    )
    
    # Filtre par statut
    if status_filter:
        query = query.filter(Match.status == status_filter)
    
    # Si l'utilisateur est un joueur et ne veut pas voir tous les matchs
    if user and user.role == "JOUEUR" and not show_all:
        # Récupérer le joueur associé à cet utilisateur
        player = db.query(Player).filter(Player.user_id == user.id).first()
        if player:
            # Récupérer les équipes du joueur
            player_teams = db.query(Team).filter(
                (Team.player1_id == player.id) | (Team.player2_id == player.id)
            ).all()
            team_ids = [team.id for team in player_teams]
            
            # Filtrer les matchs où le joueur participe
            query = query.filter(
                (Match.team1_id.in_(team_ids)) | (Match.team2_id.in_(team_ids))
            )
    
    # Filtres admin
    if company_filter:
        query = query.join(Team, (Match.team1_id == Team.id) | (Match.team2_id == Team.id))
        query = query.filter(Team.company == company_filter)
    
    if pool_filter:
        query = query.join(Team, (Match.team1_id == Team.id) | (Match.team2_id == Team.id))
        query = query.filter(Team.pool_id == pool_filter)
    
    # Trier par date et heure
    matches = query.order_by(Match.match_date, Match.match_time).all()
    
    return matches


def create_match(db: Session, match_data: MatchCreate) -> Match:
    """
    Crée un nouveau match avec validation.
    """
    # Vérifier que les deux équipes sont différentes
    if match_data.team1_id == match_data.team2_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Les deux équipes doivent être différentes"
        )
    
    # Vérifier la disponibilité du terrain
    if not check_court_availability(
        db, 
        match_data.match_date, 
        match_data.match_time, 
        match_data.court_number
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ce terrain est déjà réservé à cette date et heure"
        )
    
    # Créer le match
    new_match = Match(
        team1_id=match_data.team1_id,
        team2_id=match_data.team2_id,
        event_id=match_data.event_id,
        match_date=match_data.match_date,
        match_time=match_data.match_time,
        court_number=match_data.court_number,
        status=match_data.status,
        score_team1=match_data.score_team1,
        score_team2=match_data.score_team2,
    )
    db.add(new_match)
    db.commit()
    db.refresh(new_match)
    return new_match


def get_all_matches(db: Session):
    """Récupère tous les matchs."""
    return db.query(Match).all()


def get_match_by_id(db: Session, match_id: int) -> Match:
    """Récupère un match par son ID."""
    match = db.query(Match).options(
        joinedload(Match.team1).joinedload(Team.player1),
        joinedload(Match.team1).joinedload(Team.player2),
        joinedload(Match.team2).joinedload(Team.player1),
        joinedload(Match.team2).joinedload(Team.player2)
    ).filter(Match.id == match_id).first()

    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match non trouvé"
        )

    return match


def update_match(db: Session, match_id: int, match_data: MatchUpdate) -> Match:
    """
    Met à jour un match avec validation des contraintes.
    """
    match = get_match_by_id(db, match_id)
    
    update_data = match_data.dict(exclude_unset=True)
    
    # Vérifier les contraintes
    if 'match_date' in update_data or 'match_time' in update_data:
        # On ne peut modifier la date/heure que si le statut est A_VENIR
        if match.status != "A_VENIR":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Impossible de modifier la date/heure d'un match qui n'est pas à venir"
            )
        
        # Vérifier la disponibilité du terrain avec les nouvelles valeurs
        new_date = update_data.get('match_date', match.match_date)
        new_time = update_data.get('match_time', match.match_time)
        new_court = update_data.get('court_number', match.court_number)
        
        if not check_court_availability(db, new_date, new_time, new_court, exclude_match_id=match_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ce terrain est déjà réservé à cette date et heure"
            )
    
    # Vérifier le changement de statut
    if 'status' in update_data:
        new_status = update_data['status']
        # On peut passer de A_VENIR à ANNULE ou TERMINE
        # On ne peut pas revenir en arrière
        if match.status == "TERMINE" or match.status == "ANNULE":
            if new_status != match.status:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Impossible de modifier le statut d'un match terminé ou annulé"
                )
    
    # Appliquer les modifications
    for key, value in update_data.items():
        setattr(match, key, value)

    db.commit()
    db.refresh(match)

    return match


def delete_match(db: Session, match_id: int) -> None:
    """
    Supprime un match uniquement si son statut est A_VENIR.
    """
    match = get_match_by_id(db, match_id)
    
    if match.status != "A_VENIR":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Seuls les matchs à venir peuvent être supprimés"
        )

    db.delete(match)
    db.commit()