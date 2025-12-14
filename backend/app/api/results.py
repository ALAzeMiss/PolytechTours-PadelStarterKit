# ============================================
# FICHIER : backend/app/api/results.py
# ============================================

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.crud.results import get_personal_results, get_company_ranking, calculate_set_difference
from app.database import get_db
from app.schemas.results import PersonalResultResponse, CompanyRankingResponse
from app.api.deps import get_current_user
from app.models.models import User, Player

router = APIRouter(tags=["results"])


@router.get("/personal", response_model=List[PersonalResultResponse])
def read_personal_results(
    season_filter: Optional[str] = Query(None, description="Filtre par saison (ex: 'current')"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les résultats personnels d'un joueur.
    Affiche uniquement les matchs terminés, du plus récent au plus ancien.
    """
    # Récupérer le joueur associé à l'utilisateur
    player = db.query(Player).filter(Player.user_id == current_user.id).first()
    if not player:
        return []
    
    matches = get_personal_results(db, current_user, season_filter)
    
    # Récupérer les équipes du joueur
    from app.models.models import Team
    player_teams = db.query(Team).filter(
        (Team.player1_id == player.id) | (Team.player2_id == player.id)
    ).all()
    player_team_ids = [team.id for team in player_teams]
    
    # Construire la réponse
    results = []
    for match in matches:
        # Déterminer si le joueur est dans team1 ou team2
        is_team1 = match.team1_id in player_team_ids
        
        # Déterminer l'équipe adverse
        if is_team1:
            adversary_team = match.team2
            user_team_id = match.team1_id
            user_score = match.score_team1
            adversary_score = match.score_team2
        else:
            adversary_team = match.team1
            user_team_id = match.team2_id
            user_score = match.score_team2
            adversary_score = match.score_team1
        
        # Déterminer si c'est une victoire
        is_victory = False
        if user_score and adversary_score:
            user_sets_won, _ = calculate_set_difference(user_score)
            adv_sets_won, _ = calculate_set_difference(adversary_score)
            is_victory = user_sets_won > adv_sets_won
        
        results.append(PersonalResultResponse(
            id=match.id,
            match_date=match.match_date,
            match_time=match.match_time,
            court_number=match.court_number,
            adversary_company=adversary_team.company,
            adversary_player1_name=f"{adversary_team.player1.first_name} {adversary_team.player1.last_name}",
            adversary_player2_name=f"{adversary_team.player2.first_name} {adversary_team.player2.last_name}",
            score_team1=match.score_team1,
            score_team2=match.score_team2,
            is_victory=is_victory,
            user_team_id=user_team_id
        ))
    
    return results


@router.get("/ranking", response_model=List[CompanyRankingResponse])
def read_company_ranking(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère le classement général des entreprises.
    
    Système de points:
    - Victoire: 3 points
    - Défaite: 0 point
    - Match annulé: ne compte pas
    
    Règles de classement:
    1. Total de points
    2. En cas d'égalité: nombre de victoires
    3. En cas d'égalité: différence de sets gagnés/perdus
    4. En cas d'égalité: ordre alphabétique
    """
    return get_company_ranking(db)
