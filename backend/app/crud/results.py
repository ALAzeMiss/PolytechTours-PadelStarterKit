# ============================================
# FICHIER : backend/app/crud/results.py
# ============================================

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, case, desc
from typing import List, Optional
from datetime import date, datetime

from app.models.models import Match, Team, Player, User, MatchStatus
from app.schemas.results import PersonalResultResponse, CompanyRankingResponse


def get_personal_results(
    db: Session,
    user: User,
    season_filter: Optional[str] = None
) -> List[Match]:
    """
    Récupère les résultats personnels d'un joueur (matchs terminés uniquement).
    Filtre par saison si spécifié.
    """
    # Récupérer le joueur associé à l'utilisateur
    player = db.query(Player).filter(Player.user_id == user.id).first()
    if not player:
        return []
    
    # Récupérer les équipes du joueur
    player_teams = db.query(Team).filter(
        (Team.player1_id == player.id) | (Team.player2_id == player.id)
    ).all()
    team_ids = [team.id for team in player_teams]
    
    # Requête de base : matchs terminés où le joueur participe
    query = db.query(Match).options(
        joinedload(Match.team1).joinedload(Team.player1),
        joinedload(Match.team1).joinedload(Team.player2),
        joinedload(Match.team2).joinedload(Team.player1),
        joinedload(Match.team2).joinedload(Team.player2)
    ).filter(
        Match.status == MatchStatus.TERMINE,
        (Match.team1_id.in_(team_ids)) | (Match.team2_id.in_(team_ids))
    )
    
    # Filtre par saison (si spécifié)
    if season_filter:
        # Pour l'instant, on considère "depuis le début de la saison" comme "depuis le début de l'année"
        # Vous pouvez ajuster cette logique selon votre définition de saison
        current_year = datetime.now().year
        query = query.filter(
            func.extract('year', Match.match_date) == current_year
        )
    
    # Trier par date décroissante (du plus récent au plus ancien)
    matches = query.order_by(desc(Match.match_date), desc(Match.match_time)).all()
    
    return matches


def calculate_set_difference(score: str) -> tuple:
    """
    Calcule le nombre de sets gagnés et perdus à partir d'un score.
    Format attendu: "6-4, 6-3" ou "6-4, 3-6, 7-5"
    Retourne (sets_won, sets_lost)
    """
    if not score:
        return (0, 0)
    
    sets_won = 0
    sets_lost = 0
    
    sets = [s.strip() for s in score.split(',')]
    for set_score in sets:
        try:
            games = set_score.split('-')
            x, y = int(games[0]), int(games[1])
            if x > y:
                sets_won += 1
            else:
                sets_lost += 1
        except:
            pass
    
    return (sets_won, sets_lost)


def get_company_ranking(db: Session) -> List[CompanyRankingResponse]:
    """
    Calcule et retourne le classement général des entreprises.
    
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
    # Récupérer toutes les entreprises
    companies = db.query(Team.company).distinct().all()
    company_names = [c[0] for c in companies]
    
    ranking_data = {}
    
    for company in company_names:
        # Récupérer toutes les équipes de cette entreprise
        teams = db.query(Team).filter(Team.company == company).all()
        team_ids = [t.id for t in teams]
        
        # Récupérer tous les matchs terminés de cette entreprise
        matches = db.query(Match).options(
            joinedload(Match.team1),
            joinedload(Match.team2)
        ).filter(
            Match.status == MatchStatus.TERMINE,
            (Match.team1_id.in_(team_ids)) | (Match.team2_id.in_(team_ids))
        ).all()
        
        victories = 0
        defeats = 0
        total_sets_won = 0
        total_sets_lost = 0
        
        for match in matches:
            # Déterminer quelle équipe appartient à l'entreprise
            is_team1 = match.team1_id in team_ids
            
            if not match.score_team1 or not match.score_team2:
                continue
            
            # Calculer les sets pour chaque équipe
            if is_team1:
                sets_won, sets_lost = calculate_set_difference(match.score_team1)
            else:
                sets_won, sets_lost = calculate_set_difference(match.score_team2)
            
            total_sets_won += sets_won
            total_sets_lost += sets_lost
            
            # Déterminer le vainqueur (celui qui a gagné le plus de sets)
            if is_team1:
                team1_sets, team1_sets_lost = calculate_set_difference(match.score_team1)
                team2_sets, team2_sets_lost = calculate_set_difference(match.score_team2)
                if team1_sets > team2_sets:
                    victories += 1
                else:
                    defeats += 1
            else:
                team1_sets, team1_sets_lost = calculate_set_difference(match.score_team1)
                team2_sets, team2_sets_lost = calculate_set_difference(match.score_team2)
                if team2_sets > team1_sets:
                    victories += 1
                else:
                    defeats += 1
        
        matches_played = victories + defeats
        points = victories * 3
        
        ranking_data[company] = {
            'company': company,
            'matches_played': matches_played,
            'victories': victories,
            'defeats': defeats,
            'points': points,
            'sets_won': total_sets_won,
            'sets_lost': total_sets_lost
        }
    
    # Créer la liste de classement
    ranking_list = []
    for company, data in ranking_data.items():
        ranking_list.append(CompanyRankingResponse(
            position=0,  # Sera défini après le tri
            company=data['company'],
            matches_played=data['matches_played'],
            victories=data['victories'],
            defeats=data['defeats'],
            points=data['points'],
            sets_won=data['sets_won'],
            sets_lost=data['sets_lost']
        ))
    
    # Trier selon les règles de classement
    ranking_list.sort(
        key=lambda x: (
            -x.points,  # Plus de points en premier (d'où le -)
            -x.victories,  # Plus de victoires en premier
            -(x.sets_won - x.sets_lost),  # Meilleure différence de sets
            x.company  # Ordre alphabétique
        )
    )
    
    # Attribuer les positions
    for idx, item in enumerate(ranking_list):
        item.position = idx + 1
    
    return ranking_list
