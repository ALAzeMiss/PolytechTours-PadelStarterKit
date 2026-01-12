# ============================================
# FICHIER : backend/tests/test_team.py
# ============================================

import pytest
from fastapi import status
from app.models.models import Player, Team, User, Match
from app.core.security import get_password_hash

@pytest.fixture
def test_players(db_session, test_admin):
    """Crée des joueurs de test"""
    players = []
    for i in range(6):
        user = User(
            email=f"player{i}@test.com",
            password_hash=get_password_hash("ValidP@ssw0rd123"),
            is_admin=False,
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        player = Player(
            first_name=f"Player{i}",
            last_name=f"Test{i}",
            company=f"Company{i}",
            license_number=f"L{i}23456",
            user_id=user.id
        )
        db_session.add(player)
        db_session.commit()
        db_session.refresh(player)
        players.append(player)

    return players

@pytest.fixture
def test_teams(db_session, test_players):
    """Crée des équipes de test"""
    teams = []
    for i in range(3):
        team = Team(
            company=f"Team Company {i}",
            player1_id=test_players[i*2].id,
            player2_id=test_players[i*2+1].id
        )
        db_session.add(team)
        db_session.commit()
        db_session.refresh(team)
        teams.append(team)

    return teams

@pytest.fixture
def test_team_with_match(db_session, test_players):
    """Crée une équipe qui a joué un match"""
    team = Team(
        company="Team With Match",
        player1_id=test_players[4].id,
        player2_id=test_players[5].id
    )
    db_session.add(team)
    db_session.commit()
    db_session.refresh(team)

    # Créer un match pour cette équipe
    match = Match(
        team1_id=team.id,
        team2_id=None,  # Match incomplet pour le test
        match_date="2026-01-15",
        match_time="10:00:00",
        court_number=1,
        status="A_VENIR"
    )
    db_session.add(match)
    db_session.commit()

    return team

def test_create_team_success(client, test_admin, test_players):
    """Test création d'une équipe avec succès"""

    # Connexion admin
    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Créer une équipe
    response = client.post("/api/v1/teams/teams", json={
        "company": "Nouvelle Équipe",
        "player1_id": test_players[0].id,
        "player2_id": test_players[1].id
    }, headers=headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["company"] == "Nouvelle Équipe"
    assert data["player1_id"] == test_players[0].id
    assert data["player2_id"] == test_players[1].id
    assert data["id"] is not None

def test_create_team_player1_not_found(client, test_admin, test_players):
    """Test création d'une équipe avec joueur 1 inexistant (404)"""

    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/api/v1/teams/teams", json={
        "company": "Équipe Invalide",
        "player1_id": 999,  # ID inexistant
        "player2_id": test_players[0].id
    }, headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Joueur 1 introuvable" in response.json()["detail"]

def test_create_team_player2_not_found(client, test_admin, test_players):
    """Test création d'une équipe avec joueur 2 inexistant (404)"""

    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/api/v1/teams/teams", json={
        "company": "Équipe Invalide",
        "player1_id": test_players[0].id,
        "player2_id": 999  # ID inexistant
    }, headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Joueur 2 introuvable" in response.json()["detail"]

def test_create_team_same_player(client, test_admin, test_players):
    """Test création d'une équipe avec le même joueur (400)"""

    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/api/v1/teams/teams", json={
        "company": "Équipe Invalide",
        "player1_id": test_players[0].id,
        "player2_id": test_players[0].id  # Même joueur
    }, headers=headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "doivent être différents" in response.json()["detail"]

def test_create_team_duplicate(client, test_admin, test_teams):
    """Test création d'une équipe déjà existante (409)"""

    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Essayer de créer une équipe avec les mêmes joueurs et entreprise
    response = client.post("/api/v1/teams/teams", json={
        "company": test_teams[0].company,
        "player1_id": test_teams[0].player1_id,
        "player2_id": test_teams[0].player2_id
    }, headers=headers)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert "existe déjà" in response.json()["detail"]

def test_get_teams(client, test_teams):
    """Test récupération de toutes les équipes"""

    response = client.get("/api/v1/teams/teams")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3
    assert any(team["company"] == "Team Company 0" for team in data)

def test_get_team_by_id(client, test_teams):
    """Test récupération d'une équipe spécifique"""

    response = client.get(f"/api/v1/teams/teams/{test_teams[0].id}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_teams[0].id
    assert data["company"] == "Team Company 0"

def test_get_team_not_found(client):
    """Test récupération d'une équipe inexistante (404)"""

    response = client.get("/api/v1/teams/teams/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "introuvable" in response.json()["detail"]

def test_update_team_success(client, test_admin, test_teams):
    """Test mise à jour d'une équipe avec succès"""

    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.put(f"/api/v1/teams/teams/{test_teams[0].id}", json={
        "company": "Équipe Modifiée"
    }, headers=headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["company"] == "Équipe Modifiée"

def test_update_team_change_players_success(client, test_admin, test_teams, test_players):
    """Test changement de joueurs dans une équipe sans match"""

    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.put(f"/api/v1/teams/teams/{test_teams[0].id}", json={
        "player1_id": test_players[2].id,
        "player2_id": test_players[3].id
    }, headers=headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["player1_id"] == test_players[2].id
    assert data["player2_id"] == test_players[3].id

def test_update_team_change_players_with_match(client, test_admin, test_team_with_match, test_players):
    """Test changement de joueurs impossible si l'équipe a joué des matchs (400)"""

    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.put(f"/api/v1/teams/teams/{test_team_with_match.id}", json={
        "player1_id": test_players[0].id,
        "player2_id": test_players[1].id
    }, headers=headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "joué des matchs" in response.json()["detail"]

def test_update_team_same_player(client, test_admin, test_teams):
    """Test mise à jour avec le même joueur (400)"""

    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.put(f"/api/v1/teams/teams/{test_teams[0].id}", json={
        "player1_id": test_teams[0].player1_id,
        "player2_id": test_teams[0].player1_id  # Même joueur
    }, headers=headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "doivent être différents" in response.json()["detail"]

def test_update_team_not_found(client, test_admin):
    """Test mise à jour d'une équipe inexistante (404)"""

    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.put("/api/v1/teams/teams/999", json={
        "company": "Équipe Inexistante"
    }, headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "introuvable" in response.json()["detail"]

def test_delete_team_success(client, test_admin, test_teams):
    """Test suppression d'une équipe avec succès"""

    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.delete(f"/api/v1/teams/teams/{test_teams[0].id}", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert "supprimée" in response.json()["message"]

    # Vérifier que l'équipe n'existe plus
    get_response = client.get(f"/api/v1/teams/teams/{test_teams[0].id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_team_with_match(client, test_admin, test_team_with_match):
    """Test suppression impossible d'une équipe qui a joué des matchs (400)"""

    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.delete(f"/api/v1/teams/teams/{test_team_with_match.id}", headers=headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "joué des matchs" in response.json()["detail"]

def test_delete_team_not_found(client, test_admin):
    """Test suppression d'une équipe inexistante (404)"""

    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.delete("/api/v1/teams/teams/999", headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "introuvable" in response.json()["detail"]