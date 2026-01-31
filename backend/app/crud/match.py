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

import re
from typing import List, Tuple

SET_RE = re.compile(r"^\s*(\d+)\s*-\s*(\d+)\s*$")

def parse_sets(score_str: str) -> List[Tuple[int, int]]:
    """
    "7-5, 6-4" -> [(7,5),(6,4)]
    """
    if not score_str or not isinstance(score_str, str):
        raise ValueError("Score manquant.")

    parts = [p.strip() for p in score_str.split(",") if p.strip()]
    if len(parts) < 2 or len(parts) > 3:
        raise ValueError('Format attendu : "X-Y, X-Y" ou "X-Y, X-Y, X-Y" (2 ou 3 sets).')

    sets = []
    for part in parts:
        m = SET_RE.match(part)
        if not m:
            raise ValueError(f'Set invalide "{part}". Format attendu : X-Y')
        a = int(m.group(1))
        b = int(m.group(2))
        sets.append((a, b))
    return sets

def validate_single_set(a: int, b: int) -> None:
    if a < 0 or b < 0:
        raise ValueError("Les jeux ne peuvent pas être négatifs.")
    if a == b:
        raise ValueError("Un set ne peut pas se terminer à égalité.")

    winner = max(a, b)
    loser = min(a, b)

    if winner < 6:
        raise ValueError("Le vainqueur d'un set doit avoir au moins 6 jeux.")

    # 6-x : x doit être <= 4 (2 jeux d'écart)
    if winner == 6:
        if loser > 4:
            raise ValueError("Un set à 6 jeux doit se finir avec 2 jeux d'écart (6-0 à 6-4).")
        return

    # 7-x : x <= 5 OU 7-6 tie-break
    if winner == 7:
        if loser == 6 or loser == 5:
            return  # tie-break
        raise ValueError("Si un set se termine à 7, l'adversaire doit avoir 5 (ou 6 en tie-break 7-6).")

    raise ValueError("Un set ne peut pas dépasser 7 jeux (formats attendus: 6-x ou 7-x).")

def validate_best_of_3(sets_team1: List[Tuple[int, int]]) -> None:
    """
    Vérifie qu'on a bien un match au meilleur de 3 :
    - 2 ou 3 sets
    - le match se termine en 2 sets gagnés (2-0 ou 2-1)
    """
    t1 = 0
    t2 = 0
    for (a, b) in sets_team1:
        if a > b:
            t1 += 1
        else:
            t2 += 1

    if len(sets_team1) == 2:
        if not (t1 == 2 or t2 == 2):
            raise ValueError("Avec 2 sets, le match doit finir 2-0.")
    else:  # 3 sets
        if not ((t1 == 2 and t2 == 1) or (t2 == 2 and t1 == 1)):
            raise ValueError("Avec 3 sets, le match doit finir 2-1.")

def validate_scores_inverse(score1: str, score2: str) -> None:
    """
    Vérifie :
    - format et règles tennis pour chaque set
    - mêmes nombres de sets
    - score2 est l'inverse exact set par set : (a-b) <-> (b-a)
    - meilleur de 3 cohérent
    """
    s1 = parse_sets(score1)
    s2 = parse_sets(score2)

    if len(s1) != len(s2):
        raise ValueError("Les deux scores doivent contenir le même nombre de sets.")

    for i, ((a1, b1), (a2, b2)) in enumerate(zip(s1, s2), start=1):
        validate_single_set(a1, b1)
        validate_single_set(a2, b2)

        # inverse exact
        if not (a2 == b1 and b2 == a1):
            raise ValueError(
                f"Incohérence au set {i} : équipe 1 a {a1}-{b1}, "
                f"équipe 2 doit avoir {b1}-{a1}."
            )

    # best-of-3 check (sur l'équipe 1 suffit, puisque l'autre est inverse)
    validate_best_of_3(s1)



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
    
    # Requête de base simple (sans joinedload d'abord)
    query = db.query(Match).filter(
        Match.match_date >= today,
        Match.match_date <= end_date
    )
    
    # Filtre par statut
    if status_filter:
        query = query.filter(Match.status == status_filter)
    
    # Si l'utilisateur est un joueur et ne veut pas voir tous les matchs
    if user and not user.is_admin and not show_all:
        # Récupérer le joueur associé à cet utilisateur
        player = db.query(Player).filter(Player.user_id == user.id).first()
        if player:
            # Récupérer les équipes du joueur
            player_teams = db.query(Team).filter(
                (Team.player1_id == player.id) | (Team.player2_id == player.id)
            ).all()
            team_ids = [team.id for team in player_teams]
            
            # Filtrer les matchs où le joueur participe
            if team_ids:
                query = query.filter(
                    (Match.team1_id.in_(team_ids)) | (Match.team2_id.in_(team_ids))
                )
            else:
                # Si le joueur n'a pas d'équipes, retourner une liste vide
                return []
    
    # Filtres admin - utiliser une jointure mais pas avec joinedload
    if company_filter:
        company_team_ids = db.query(Team.id).filter(Team.company == company_filter).subquery()
        query = query.filter(
            (Match.team1_id.in_(company_team_ids)) |
            (Match.team2_id.in_(company_team_ids))
        )
    
    if pool_filter:
        pool_team_ids = db.query(Team.id).filter(Team.pool_id == pool_filter).subquery()
        query = query.filter(
            (Match.team1_id.in_(pool_team_ids)) |
            (Match.team2_id.in_(pool_team_ids))
        )
    
    # Trier par date et heure
    matches = query.order_by(Match.match_date, Match.match_time).all()
    
    # Force le chargement des relations
    for match in matches:
        # Accéder aux attributs force le lazy loading
        _ = match.team1
        _ = match.team1.player1
        _ = match.team1.player2
        _ = match.team2
        _ = match.team2.player1
        _ = match.team2.player2
    
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
    Met à jour un match avec validation des contraintes + validation des scores inversés
    quand le match est terminé.
    """
    match = get_match_by_id(db, match_id)
    update_data = match_data.dict(exclude_unset=True)

    # --------------------------------------------------
    # 1) Date / heure / piste modifiables uniquement si A_VENIR
    # --------------------------------------------------
    if any(k in update_data for k in ("match_date", "match_time", "court_number")):
        if match.status != "A_VENIR":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Impossible de modifier la date/heure/piste d'un match qui n'est pas à venir"
            )

        new_date = update_data.get('match_date', match.match_date)
        new_time = update_data.get('match_time', match.match_time)
        new_court = update_data.get('court_number', match.court_number)

        if not check_court_availability(db, new_date, new_time, new_court, exclude_match_id=match_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ce terrain est déjà réservé à cette date et heure"
            )

    # --------------------------------------------------
    # 2) Validation changement de statut
    # --------------------------------------------------
    if 'status' in update_data:
        new_status = update_data['status']

        # On ne peut pas modifier un match déjà terminé ou annulé
        if match.status in ("TERMINE", "ANNULE") and new_status != match.status:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Impossible de modifier le statut d'un match terminé ou annulé"
            )

    # --------------------------------------------------
    # 3) Validation scores si TERMINE
    # --------------------------------------------------
    # Règle: si status devient TERMINE => score_team1 et score_team2 obligatoires,
    # et doivent être inverses exacts.
    if update_data.get("status") == "TERMINE":
        score1 = update_data.get("score_team1")
        score2 = update_data.get("score_team2")

        if not score1 or not score2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Pour terminer un match, vous devez renseigner score_team1 et score_team2 '
                       '(ex: "7-5, 6-4" et "5-7, 4-6").'
            )

        try:
            validate_scores_inverse(score1, score2)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    # Optionnel (mais recommandé) :
    # Si on ne termine PAS le match, on interdit de renseigner les scores
    if update_data.get("status") in ("A_VENIR", "ANNULE"):
        if "score_team1" in update_data or "score_team2" in update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Les scores ne peuvent être saisis que lorsque le match est terminé."
            )

    # --------------------------------------------------
    # 4) Appliquer les modifications
    # --------------------------------------------------
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