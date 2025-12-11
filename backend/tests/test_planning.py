# ============================================
# FICHIER : backend/tests/test_planning.py
# ============================================

import pytest
from fastapi import status
from app.main import app
from app.api import planning
from sqlalchemy import text


# S'assurer que les routes de planning sont montées pour les tests
app.include_router(planning.router)


def insert_sample_data(db_session):
    """Insère joueurs, équipes, événements et matchs minimal pour les tests."""
    # Players
    db_session.execute(text("""
        INSERT INTO players (first_name, last_name, company, license_number, birth_date)
        VALUES
          ('Jean','Dupont','Tech Corp','L900001','1990-01-01'),
          ('Marc','Petit','Innov Ltd','L900002','1991-02-02'),
          ('Alice','Durand','Club A','L900003','1992-03-03'),
          ('Bob','Martin','Club B','L900004','1993-04-04')
    """))

    # Teams
    db_session.execute(text("""
        INSERT INTO teams (company, player1_id, player2_id)
        VALUES
          ('Team Tech-Innov', (SELECT id FROM players WHERE license_number='L900001'), (SELECT id FROM players WHERE license_number='L900002')),
          ('Team ClubA-ClubB', (SELECT id FROM players WHERE license_number='L900003'), (SELECT id FROM players WHERE license_number='L900004'))
    """))

    # Events
    db_session.execute(text("""
        INSERT INTO events (event_date, event_time) VALUES
          ('2025-11-15','19:30'),
          ('2025-11-22','20:00')
    """))

    # Matches
    db_session.execute(text("""
        INSERT INTO matches (event_id, team1_id, team2_id, court_number, status)
        VALUES
          ((SELECT id FROM events WHERE event_date='2025-11-15' AND event_time='19:30'), (SELECT id FROM teams WHERE company='Team Tech-Innov'), (SELECT id FROM teams WHERE company='Team ClubA-ClubB'), 1, 'A_VENIR'),
          ((SELECT id FROM events WHERE event_date='2025-11-22' AND event_time='20:00'), (SELECT id FROM teams WHERE company='Team Tech-Innov'), (SELECT id FROM teams WHERE company='Team ClubA-ClubB'), 2, 'A_VENIR')
    """))

    db_session.commit()


def test_events_range_returns_events_and_matches(client, db_session, test_user):
    """Vérifie que /planning/events-range retourne les événements et leurs matchs"""
    insert_sample_data(db_session)
    # Se connecter pour obtenir un token
    login = client.post("/api/v1/auth/login", json={"email": "test@example.com", "password": "ValidP@ssw0rd123"})
    assert login.status_code == 200
    token = login.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    resp = client.get("/events?start=2025-11-01&end=2025-11-30", headers=headers)
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    assert isinstance(data, list)
    # Doit contenir au moins l'événement du 15/11
    ev_dates = [e["event_date"] for e in data]
    assert any('2025-11-15' in d for d in ev_dates)
    # vérifier que les matches sont présents pour un des events
    found = False
    for e in data:
        if e.get("matches"):
            found = True
            m = e["matches"][0]
            assert "court_number" in m
            assert "team1_id" in m and "team2_id" in m
            break
    assert found is True


def test_planning_day_returns_matches_for_date(client, db_session):
    """Vérifie que /planning/day/{date} renvoie les matchs de la journée"""
    insert_sample_data(db_session)

    resp = client.get("/events/day/2025-11-15")
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    assert data.get("date") == '2025-11-15'
    assert isinstance(data.get("matches"), list)
    assert len(data["matches"]) >= 1
    match = data["matches"][0]
    assert "team1" in match and "team2" in match
    assert "event_time" in match


def test_my_events_returns_matches_for_user(client, db_session, test_user):
    """Vérifie que /planning/my-events retourne uniquement les matchs où l'utilisateur participe."""
    # Insérer des données et lier un joueur au test_user
    insert_sample_data(db_session)

    # Lier le joueur 1 au test_user (user_id)
    db_session.execute(text("UPDATE players SET user_id = :uid WHERE license_number = 'L900001'"), {"uid": test_user.id})
    db_session.commit()

    # Se connecter pour obtenir un token
    login = client.post("/api/v1/auth/login", json={"email": "test@example.com", "password": "ValidP@ssw0rd123"})
    assert login.status_code == status.HTTP_200_OK
    token = login.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    resp = client.get("/events/my-events", headers=headers)
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    assert "matches" in data
    # Au moins un match doit être renvoyé car le joueur L900001 participe à Team Tech-Innov
    assert len(data["matches"]) >= 1
    m = data["matches"][0]
    assert m["team1"]["players"] or m["team2"]["players"]
