"""
Script de peuplement pour ajouter des matchs pour l'utilisateur admin@padel.com.
Usage: python backend/scripts/seed_admin_matches.py

Ce script:
- s'assure que l'admin existe (utilise `init_db()` qui crée l'admin si absent)
- crée des players/teams
- crée un événement (date + heure)
- crée deux matchs le même jour et à la même heure (pistes différentes)

Les insertions utilisent des requêtes SQL brutes afin de rester compatibles avec la structure actuelle.
"""

from sqlalchemy import text
from app.database import init_db, SessionLocal
from app.models.models import User


def main():
    # Initialise la DB et crée admin si nécessaire
    init_db()

    session = SessionLocal()
    try:
        admin = session.query(User).filter(User.email == 'admin@padel.com').first()
        if not admin:
            print('Impossible de retrouver admin@padel.com après init_db(). Abandon.')
            return

        uid = admin.id
        print(f'Admin trouvé id={uid}')

        # Paramètres: date et heure des matchs
        event_date = '2025-12-20'
        event_time = '19:00'

        # Insérer 4 joueurs (deux équipes) sans lier immédiatement à l'utilisateur
        session.execute(text("""
            INSERT OR IGNORE INTO players (first_name, last_name, company, license_number, birth_date, user_id)
            VALUES
              ('Admin','Player1','Club Admin','L900010','1985-01-01', NULL),
              ('Partner','One','Club A','L900011','1990-02-02', NULL),
              ('Admin','Player2','Club Admin','L900012','1986-03-03', NULL),
              ('Partner','Two','Club B','L900013','1992-04-04', NULL)
        """))

        # Si aucun joueur n'est encore lié à l'admin, lier le premier joueur inséré
        existing = session.execute(text("SELECT id FROM players WHERE user_id = :uid"), {'uid': uid}).fetchone()
        if not existing:
            session.execute(text("UPDATE players SET user_id = :uid WHERE license_number = 'L900010'"), {'uid': uid})

        # Créer deux équipes si elles n'existent pas
        session.execute(text("""
            INSERT OR IGNORE INTO teams (id, company, player1_id, player2_id)
            SELECT NULL, 'Team Admin-A', (SELECT id FROM players WHERE license_number='L900010'), (SELECT id FROM players WHERE license_number='L900011')
            WHERE NOT EXISTS (SELECT 1 FROM teams WHERE company='Team Admin-A');
        """))
        session.execute(text("""
            INSERT OR IGNORE INTO teams (id, company, player1_id, player2_id)
            SELECT NULL, 'Team Admin-B', (SELECT id FROM players WHERE license_number='L900012'), (SELECT id FROM players WHERE license_number='L900013')
            WHERE NOT EXISTS (SELECT 1 FROM teams WHERE company='Team Admin-B');
        """))

        # Créer l'événement s'il n'existe pas
        session.execute(text("""
            INSERT OR IGNORE INTO events (id, event_date, event_time)
            SELECT NULL, :ev_date, :ev_time
            WHERE NOT EXISTS (SELECT 1 FROM events WHERE event_date = :ev_date AND event_time = :ev_time);
        """), {'ev_date': event_date, 'ev_time': event_time})

        # Créer deux matchs pour le même event (même jour/heure), sur deux pistes
        session.execute(text("""
            INSERT OR IGNORE INTO matches (id, event_id, team1_id, team2_id, court_number, status)
            SELECT NULL,
              (SELECT id FROM events WHERE event_date=:ev_date AND event_time=:ev_time LIMIT 1),
              (SELECT id FROM teams WHERE company='Team Admin-A'),
              (SELECT id FROM teams WHERE company='Team Admin-B'), 1, 'A_VENIR'
            WHERE NOT EXISTS (
              SELECT 1 FROM matches m JOIN events e ON e.id = m.event_id WHERE e.event_date = :ev_date AND e.event_time = :ev_time AND m.court_number = 1
            );
        """), {'ev_date': event_date, 'ev_time': event_time})

        session.execute(text("""
            INSERT OR IGNORE INTO matches (id, event_id, team1_id, team2_id, court_number, status)
            SELECT NULL,
              (SELECT id FROM events WHERE event_date=:ev_date AND event_time=:ev_time LIMIT 1),
              (SELECT id FROM teams WHERE company='Team Admin-B'),
              (SELECT id FROM teams WHERE company='Team Admin-A'), 2, 'A_VENIR'
            WHERE NOT EXISTS (
              SELECT 1 FROM matches m JOIN events e ON e.id = m.event_id WHERE e.event_date = :ev_date AND e.event_time = :ev_time AND m.court_number = 2
            );
        """), {'ev_date': event_date, 'ev_time': event_time})

        session.commit()

        print('Matchs créés pour admin@padel.com :')
        # Afficher les matchs créés
        rows = session.execute(text("SELECT m.id, e.event_date, e.event_time, m.court_number FROM matches m JOIN events e ON e.id = m.event_id WHERE e.event_date = :ev_date"), {'ev_date': event_date}).fetchall()
        for r in rows:
            print(dict(r._mapping))

    finally:
        session.close()


if __name__ == '__main__':
    main()
