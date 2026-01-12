# ============================================
# FICHIER : backend/tests/test_player.py
# ============================================

import pytest
from fastapi import status

def test_create_player_success(client, test_admin):
    """Test creation d'un player avec les droits admin"""

    # Créer d'abord un user
    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}

    # Créer un user
    user_response = client.post("/api/v1/users/users", json={
        "email": "player@test.com",
        "is_admin": False
    }, headers=headers)
    user_id = user_response.json()["user"]["id"]

    # Créer un player
    response = client.post("/api/v1/players/players", json={
        "first_name": "John",
        "last_name": "Doe",
        "company": "Test Corp",
        "license_number": "L123456",
        "user_id": user_id
    }, headers=headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
    assert data["company"] == "Test Corp"
    assert data["license_number"] == "L123456"
    assert data["user_id"] == user_id

def test_create_player_invalid_first_name(client, test_admin):
    """Test creation avec prénom invalide (400)"""
    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    user_response = client.post("/api/v1/users/users", json={
        "email": "player1@test.com",
        "is_admin": False
    }, headers=headers)
    user_id = user_response.json()["user"]["id"]

    response = client.post("/api/v1/players/players", json={
        "first_name": "123",  # Invalide
        "last_name": "Doe",
        "company": "Test Corp",
        "user_id": user_id
    }, headers=headers)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_create_player_invalid_last_name(client, test_admin):
    """Test creation avec nom invalide (400)"""
    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    user_response = client.post("/api/v1/users/users", json={
        "email": "player2@test.com",
        "is_admin": False
    }, headers=headers)
    user_id = user_response.json()["user"]["id"]

    response = client.post("/api/v1/players/players", json={
        "first_name": "John",
        "last_name": "@#$",  # Invalide
        "company": "Test Corp",
        "user_id": user_id
    }, headers=headers)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_create_player_invalid_company(client, test_admin):
    """Test creation avec entreprise invalide (400)"""
    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    user_response = client.post("/api/v1/users/users", json={
        "email": "player3@test.com",
        "is_admin": False
    }, headers=headers)
    user_id = user_response.json()["user"]["id"]

    response = client.post("/api/v1/players/players", json={
        "first_name": "John",
        "last_name": "Doe",
        "company": "",  # Invalide
        "user_id": user_id
    }, headers=headers)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_create_player_invalid_license(client, test_admin):
    """Test creation avec licence invalide (400)"""
    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    user_response = client.post("/api/v1/users/users", json={
        "email": "player4@test.com",
        "is_admin": False
    }, headers=headers)
    user_id = user_response.json()["user"]["id"]

    response = client.post("/api/v1/players/players", json={
        "first_name": "John",
        "last_name": "Doe",
        "company": "Test Corp",
        "license_number": "INVALID",  # Invalide
        "user_id": user_id
    }, headers=headers)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_create_player_user_not_found(client, test_admin):
    """Test creation avec user_id inexistant (404)"""
    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/api/v1/players/players", json={
        "first_name": "John",
        "last_name": "Doe",
        "company": "Test Corp",
        "user_id": 99999  # Inexistant
    }, headers=headers)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_create_player_already_associated(client, test_admin):
    """Test creation avec user déjà associé à un player (409)"""
    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Créer un user
    user_response = client.post("/api/v1/users/users", json={
        "email": "player5@test.com",
        "is_admin": False
    }, headers=headers)
    user_id = user_response.json()["user"]["id"]

    # Créer un player
    client.post("/api/v1/players/players", json={
        "first_name": "John",
        "last_name": "Doe",
        "company": "Test Corp",
        "user_id": user_id
    }, headers=headers)

    # Tenter de créer un deuxième player pour le même user
    response = client.post("/api/v1/players/players", json={
        "first_name": "Jane",
        "last_name": "Smith",
        "company": "Test Corp",
        "user_id": user_id
    }, headers=headers)
    
    assert response.status_code == status.HTTP_409_CONFLICT

def test_create_player_duplicate_license(client, test_admin):
    """Test creation avec licence déjà existante (409)"""
    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Créer deux users
    user1_response = client.post("/api/v1/users/users", json={
        "email": "player6@test.com",
        "is_admin": False
    }, headers=headers)
    user1_id = user1_response.json()["user"]["id"]

    user2_response = client.post("/api/v1/users/users", json={
        "email": "player7@test.com",
        "is_admin": False
    }, headers=headers)
    user2_id = user2_response.json()["user"]["id"]

    # Créer un player avec une licence
    client.post("/api/v1/players/players", json={
        "first_name": "John",
        "last_name": "Doe",
        "company": "Test Corp",
        "license_number": "L123456",
        "user_id": user1_id
    }, headers=headers)

    # Tenter de créer un player avec la même licence
    response = client.post("/api/v1/players/players", json={
        "first_name": "Jane",
        "last_name": "Smith",
        "company": "Test Corp",
        "license_number": "L123456",
        "user_id": user2_id
    }, headers=headers)
    
    assert response.status_code == status.HTTP_409_CONFLICT

def test_create_player_unauthorized(client):
    """Test creation sans authentification (401)"""
    response = client.post("/api/v1/players/players", json={
        "first_name": "John",
        "last_name": "Doe",
        "company": "Test Corp",
        "user_id": 1
    })
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_create_player_forbidden(client, test_user):
    """Test creation avec user non admin (403)"""
    login_response = client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "ValidP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/api/v1/players/players", json={
        "first_name": "John",
        "last_name": "Doe",
        "company": "Test Corp",
        "user_id": 1
    }, headers=headers)
    
    assert response.status_code == status.HTTP_403_FORBIDDEN