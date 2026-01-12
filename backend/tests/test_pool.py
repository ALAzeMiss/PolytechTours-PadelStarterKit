# ============================================
# FICHIER : backend/tests/test_pool.py
# ============================================

import pytest
from fastapi import status
from app.models.models import Player, Team, Pool, User
from app.core.security import get_password_hash

@pytest.fixture
def test_players(db_session, test_admin):
    """Crée des joueurs de test"""
    players = []
    for i in range(4):
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
    for i in range(2):
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
def test_pool(db_session, test_teams):
    """Crée une poule de test"""
    pool = Pool(name="Test Pool")
    db_session.add(pool)
    db_session.commit()
    db_session.refresh(pool)

    # Assigner les équipes à la poule
    for team in test_teams:
        team.pool_id = pool.id
    db_session.commit()

    return pool

def test_create_pool_success(client, test_admin, test_teams):
    """Test création d'une poule avec succès"""

    # Connexion admin
    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Créer une poule
    response = client.post("/api/v1/pools/pools", json={
        "name": "Nouvelle Poule",
        "team_ids": [test_teams[0].id, test_teams[1].id]
    }, headers=headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Nouvelle Poule"
    assert data["id"] is not None

def test_create_pool_duplicate_name(client, test_admin, test_teams, test_pool):
    """Test création d'une poule avec nom déjà existant (409)"""

    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/api/v1/pools/pools", json={
        "name": "Test Pool",  # Nom déjà utilisé
        "team_ids": [test_teams[0].id]
    }, headers=headers)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert "existe déjà" in response.json()["detail"]

def test_create_pool_invalid_team_id(client, test_admin):
    """Test création d'une poule avec équipe inexistante (404)"""

    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/api/v1/pools/pools", json={
        "name": "Poule Invalide",
        "team_ids": [999]  # ID inexistant
    }, headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "introuvable" in response.json()["detail"]

def test_create_pool_team_already_in_pool(client, test_admin, test_pool):
    """Test création d'une poule avec équipe déjà dans une autre poule (400)"""

    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Essayer de créer une poule avec une équipe déjà dans test_pool
    response = client.post("/api/v1/pools/pools", json={
        "name": "Poule Conflit",
        "team_ids": [test_pool.teams[0].id]  # Équipe déjà dans une poule
    }, headers=headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "déjà dans une poule" in response.json()["detail"]

def test_get_pools(client, test_pool):
    """Test récupération de toutes les poules"""

    response = client.get("/api/v1/pools/pools")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(pool["name"] == "Test Pool" for pool in data)

def test_get_pool_by_id(client, test_pool):
    """Test récupération d'une poule spécifique"""

    response = client.get(f"/api/v1/pools/pools/{test_pool.id}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_pool.id
    assert data["name"] == "Test Pool"

def test_get_pool_not_found(client):
    """Test récupération d'une poule inexistante (404)"""

    response = client.get("/api/v1/pools/pools/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "introuvable" in response.json()["detail"]

def test_update_pool_success(client, test_admin, test_pool):
    """Test mise à jour d'une poule avec succès"""

    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.put(f"/api/v1/pools/pools/{test_pool.id}", json={
        "name": "Poule Modifiée",
        "team_ids": []
    }, headers=headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Poule Modifiée"

def test_update_pool_duplicate_name(client, test_admin, test_pool):
    """Test mise à jour d'une poule avec nom déjà existant (409)"""

    # Créer une deuxième poule
    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    pool2_response = client.post("/api/v1/pools/pools", json={
        "name": "Deuxième Poule",
        "team_ids": []
    }, headers=headers)
    pool2_id = pool2_response.json()["id"]

    # Essayer de renommer la première poule avec le nom de la deuxième
    response = client.put(f"/api/v1/pools/pools/{test_pool.id}", json={
        "name": "Deuxième Poule",
        "team_ids": []
    }, headers=headers)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert "existe déjà" in response.json()["detail"]

def test_update_pool_not_found(client, test_admin):
    """Test mise à jour d'une poule inexistante (404)"""

    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.put("/api/v1/pools/pools/999", json={
        "name": "Poule Inexistante",
        "team_ids": []
    }, headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "introuvable" in response.json()["detail"]

def test_delete_pool_success(client, test_admin, test_pool):
    """Test suppression d'une poule avec succès"""

    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.delete(f"/api/v1/pools/pools/{test_pool.id}", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert "supprimée" in response.json()["message"]

    # Vérifier que la poule n'existe plus
    get_response = client.get(f"/api/v1/pools/pools/{test_pool.id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_pool_not_found(client, test_admin):
    """Test suppression d'une poule inexistante (404)"""

    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.delete("/api/v1/pools/pools/999", headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "introuvable" in response.json()["detail"]