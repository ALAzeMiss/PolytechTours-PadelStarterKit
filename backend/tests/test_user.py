# ============================================
# FICHIER : backend/tests/test_user.py
# ============================================

import pytest
from fastapi import status

def test_create_user_success(client, test_admin):
    """Test creation d'un user avec les droits admin"""

    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/api/v1/users/users", json={
        "email": "test@test.com",
        "is_admin": True
    }, headers=headers)
    
    assert response.status_code == status.HTTP_201_CREATED

def test_create_user_with_invalid_email(client, test_admin):
    """Test creation d'un user avec une adresse mail invalide"""

    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}

<<<<<<< HEAD
    response = client.post("/api/v1/users", json={
=======
    response = client.post("/api/v1/users/users", json={
>>>>>>> main
        "email": "test@test",
        "is_admin": True
    }, headers=headers)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_create_user_with_invalid_email_2(client, test_admin):
    """Test creation d'un user avec une adresse mail invalide"""

    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}

<<<<<<< HEAD
    response = client.post("/api/v1/users", json={
        "email": "testtest.com",
=======
    response = client.post("/api/v1/users/users", json={
        "email": "test@test.c",
>>>>>>> main
        "is_admin": True
    }, headers=headers)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_create_user_with_invalid_email_3(client, test_admin):
    """Test creation d'un user avec une adresse mail invalide"""

    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}

<<<<<<< HEAD
    response = client.post("/api/v1/users", json={
=======
    response = client.post("/api/v1/users/users", json={
        "email": "testtest.com",
        "is_admin": True
    }, headers=headers)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_create_user_with_invalid_email_4(client, test_admin):
    """Test creation d'un user avec une adresse mail invalide"""

    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/api/v1/users/users", json={
>>>>>>> main
        "email": "testtest",
        "is_admin": True
    }, headers=headers)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_create_user_with_empty_email_field(client, test_admin):
    """Test creation d'un user avec le champ email vide"""

    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}

<<<<<<< HEAD
    response = client.post("/api/v1/users", json={
=======
    response = client.post("/api/v1/users/users", json={
>>>>>>> main
        "email": "",
        "is_admin": True
    }, headers=headers)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_create_user_without_email(client, test_admin):
    """Test creation d'un user sans champ email"""

    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}

<<<<<<< HEAD
    response = client.post("/api/v1/users", json={
=======
    response = client.post("/api/v1/users/users", json={
>>>>>>> main
        "is_admin": True
    }, headers=headers)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_create_user_with_wrong_format_email(client, test_admin):
    """Test creation d'un user avec un email du mauvais format"""

    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}

<<<<<<< HEAD
    response = client.post("/api/v1/users", json={
=======
    response = client.post("/api/v1/users/users", json={
>>>>>>> main
        "email": 123456,
        "is_admin": True
    }, headers=headers)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_create_user_without_admin_info(client, test_admin):
    """Test creation d'un user sans champ is_admin"""

    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}

<<<<<<< HEAD
    response = client.post("/api/v1/users", json={
=======
    response = client.post("/api/v1/users/users", json={
>>>>>>> main
        "email": "test@test.fr"
    }, headers=headers)
    
    assert response.status_code == status.HTTP_201_CREATED

def test_create_user_without_authentification(client, test_admin):
    """Test creation d'un user sans auythentification"""

<<<<<<< HEAD
    response = client.post("/api/v1/users", json={
=======
    response = client.post("/api/v1/users/users", json={
>>>>>>> main
        "email": "test@test.fr",
        "is_admin": True
    })
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_create_user_without_admin_rights(client, test_user):
    """Test creation d'un user sans les permissions admin"""

    login_response = client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "ValidP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}

<<<<<<< HEAD
    response = client.post("/api/v1/users", json={
=======
    response = client.post("/api/v1/users/users", json={
>>>>>>> main
        "email": "test@test.fr",
        "is_admin": True
    }, headers=headers)
    
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_create_user_with_already_existing_email(client, test_admin):
    """Test creation d'un user avec une adresse mail déjà existante"""

    login_response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminP@ssw0rd123"
    })
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}

<<<<<<< HEAD
    response = client.post("/api/v1/users", json={
=======
    response = client.post("/api/v1/users/users", json={
>>>>>>> main
        "email": "admin@example.com",
        "is_admin": True
    }, headers=headers)
    
    assert response.status_code == status.HTTP_409_CONFLICT
