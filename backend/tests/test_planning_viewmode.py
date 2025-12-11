# ============================================
# FICHIER : backend/tests/test_planning_viewmode.py
# ============================================

from sqlalchemy import text
from fastapi import status
from app.main import app
from app.api import planning

# S'assurer que les routes de planning sont montées pour les tests
app.include_router(planning.router)


def insert_viewmode_data(db_session):
    """Insère des players, teams, events et matchs similaires au script de seed.
    Deux dates : 2025-12-21 (un match impliquant l'utilisateur, un sans lui)
    et 2025-12-22 (deux matchs sans l'utilisateur).
    """
    # Players
    db_session.execute(text("""
        INSERT INTO players (first_name, last_name, company, license_number, birth_date)
        VALUES
          ('User','Player','Club User','L910020','1995-05-05'),
          ('Partner','User','Club User','L910021','1994-06-06'),
          ('Other','One','Club X','L910022','1990-07-07'),
          ('Other','Two','Club Y','L910023','1991-08-08'),
          ('Stranger','A','Club Z','L910024','1988-09-09')
    """))

    # Teams
    db_session.execute(text("""
        INSERT INTO teams (company, player1_id, player2_id)
        VALUES
          ('Team User-A', (SELECT id FROM players WHERE license_number='L910020'), (SELECT id FROM players WHERE license_number='L910021')),
          ('Team Other-A', (SELECT id FROM players WHERE license_number='L910022'), (SELECT id FROM players WHERE license_number='L910023')),
          ('Team Stranger', (SELECT id FROM players WHERE license_number='L910024'), (SELECT id FROM players WHERE license_number='L910023'))
    """))

    # Events
    db_session.execute(text("""
        INSERT INTO events (event_date, event_time) VALUES
          ('2025-12-21','18:00'),
          ('2025-12-22','20:00')
    """))

    # Matches
    db_session.execute(text("""
        INSERT INTO matches (event_id, team1_id, team2_id, court_number, status)
        VALUES
          ((SELECT id FROM events WHERE event_date='2025-12-21' AND event_time='18:00'), (SELECT id FROM teams WHERE company='Team User-A'), (SELECT id FROM teams WHERE company='Team Other-A'), 1, 'A_VENIR'),
          ((SELECT id FROM events WHERE event_date='2025-12-21' AND event_time='18:00'), (SELECT id FROM teams WHERE company='Team Other-A'), (SELECT id FROM teams WHERE company='Team Stranger'), 2, 'A_VENIR'),
          ((SELECT id FROM events WHERE event_date='2025-12-22' AND event_time='20:00'), (SELECT id FROM teams WHERE company='Team Other-A'), (SELECT id FROM teams WHERE company='Team Stranger'), 1, 'A_VENIR'),
          ((SELECT id FROM events WHERE event_date='2025-12-22' AND event_time='20:00'), (SELECT id FROM teams WHERE company='Team Stranger'), (SELECT id FROM teams WHERE company='Team Other-A'), 2, 'A_VENIR')
    """))

    db_session.commit()


def test_events_and_my_events_viewmode(client, db_session, test_user):
    """Vérifie que /events renvoie tous les events et que /events/my-events renvoie uniquement
    les matchs du user lié via players.user_id.
    """
    insert_viewmode_data(db_session)

    # Lier le joueur principal au test_user
    db_session.execute(text("UPDATE players SET user_id = :uid WHERE license_number = 'L910020'"), {"uid": test_user.id})
    db_session.commit()

    # Authentifier
    login = client.post('/api/v1/auth/login', json={'email': 'test@example.com', 'password': 'ValidP@ssw0rd123'})
    assert login.status_code == 200
    token = login.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    # Demander la plage complète
    resp = client.get('/events?start=2025-12-20&end=2025-12-23', headers=headers)
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    # Doit contenir deux dates (21 et 22 déc) et matches
    dates = [e['event_date'] for e in data]
    assert '2025-12-21' in dates and '2025-12-22' in dates

    # Vérifier que dans les matches retournés au moins un contient user_in_team1 ou user_in_team2 true
    found_user_flag = False
    for e in data:
        for m in e.get('matches', []):
            if m.get('user_in_team1') or m.get('user_in_team2'):
                found_user_flag = True
                break
        if found_user_flag:
            break
    assert found_user_flag is True

    # Maintenant vérifier /events/my-events ne contient que les matchs du user
    resp2 = client.get('/events/my-events', headers=headers)
    assert resp2.status_code == status.HTTP_200_OK
    payload = resp2.json()
    assert 'matches' in payload
    # Doit n'y avoir qu'au moins 1 match et tous les matchs doivent avoir l'utilisateur dans une des équipes
    assert len(payload['matches']) >= 1
    for m in payload['matches']:
        # Vérifier qu'au moins une des équipes contient le player (via players list)
        players = m['team1']['players'] + m['team2']['players']
        # At least one player string should be present and match the User Player name
        assert any('User Player' in p for p in players)
