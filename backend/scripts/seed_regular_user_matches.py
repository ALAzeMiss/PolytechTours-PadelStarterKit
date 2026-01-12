"""
Script de peuplement pour ajouter un utilisateur classique et des matchs.
Usage (depuis le dossier racine du repo):
  python -c "import sys; sys.path.insert(0, 'backend'); from scripts.seed_regular_user_matches import main; main()"

Ce script:
- s'assure que la DB est initialisée (`init_db()` crée l'admin si nécessaire)
- crée un utilisateur non-admin `user@padel.com` (mot de passe: `User@2025!`) si absent
- crée des players/teams
- crée plusieurs événements et matchs; certains matchs impliquent le joueur créé, d'autres non

Le script est idempotent (utilise `INSERT OR IGNORE` et `WHERE NOT EXISTS`).
"""

from sqlalchemy import text
from app.database import init_db, SessionLocal
from app.models.models import User
from app.core.security import get_password_hash


def main():
    init_db()

    session = SessionLocal()
    try:
        # Créer l'utilisateur classique s'il n'existe pas
        user = session.query(User).filter(User.email == 'user@padel.com').first()
        if not user:
            user = User(
                email='user@padel.com',
                password_hash=get_password_hash('User@2025!'),
                role='JOUEUR',
                is_active=True
            )
            session.add(user)
            session.commit()
            print('✅ Utilisateur créé : user@padel.com / User@2025!')
        else:
            print('ℹ️  Utilisateur existe déjà : user@padel.com')

        uid = user.id

        # Paramètres d'événements et horaires
        ev1_date = '2025-12-21'
        ev1_time = '18:00'
        ev2_date = '2025-12-22'
        ev2_time = '20:00'

        # Insérer players (certains liés à l'utilisateur, d'autres non)
        session.execute(text("""
            INSERT OR IGNORE INTO players (first_name, last_name, company, license_number, birth_date, user_id)
            VALUES
              ('User','Player','Club User','L900020','1995-05-05', NULL),
              ('Partner','User','Club User','L900021','1994-06-06', NULL),
              ('Other','One','Club X','L900022','1990-07-07', NULL),
              ('Other','Two','Club Y','L900023','1991-08-08', NULL),
              ('Stranger','A','Club Z','L900024','1988-09-09', NULL)
        """))

        # Lier le joueur principal à l'utilisateur si pas encore lié
        existing = session.execute(text("SELECT id FROM players WHERE user_id = :uid"), {'uid': uid}).fetchone()
        if not existing:
            session.execute(text("UPDATE players SET user_id = :uid WHERE license_number = 'L900020'"), {'uid': uid})

        # Créer des teams: une équipe contenant l'utilisateur, et d'autres équipes sans lui
        session.execute(text("""
            INSERT OR IGNORE INTO teams (id, company, player1_id, player2_id)
            SELECT NULL, 'Team User-A',
              (SELECT id FROM players WHERE license_number='L900020'),
              (SELECT id FROM players WHERE license_number='L900021')
            WHERE NOT EXISTS (SELECT 1 FROM teams WHERE company='Team User-A');
        """))

        session.execute(text("""
            INSERT OR IGNORE INTO teams (id, company, player1_id, player2_id)
            SELECT NULL, 'Team Other-A',
              (SELECT id FROM players WHERE license_number='L900022'),
              (SELECT id FROM players WHERE license_number='L900023')
            WHERE NOT EXISTS (SELECT 1 FROM teams WHERE company='Team Other-A');
        """))

        session.execute(text("""
            INSERT OR IGNORE INTO teams (id, company, player1_id, player2_id)
            SELECT NULL, 'Team Stranger',
              (SELECT id FROM players WHERE license_number='L900024'),
              (SELECT id FROM players WHERE license_number='L900023')
            WHERE NOT EXISTS (SELECT 1 FROM teams WHERE company='Team Stranger');
        """))

        # Créer deux événements pour deux dates
        session.execute(text("""
            INSERT OR IGNORE INTO events (id, event_date, event_time)
            SELECT NULL, :d1, :t1
            WHERE NOT EXISTS (SELECT 1 FROM events WHERE event_date = :d1 AND event_time = :t1);
        """), {'d1': ev1_date, 't1': ev1_time})

        session.execute(text("""
            INSERT OR IGNORE INTO events (id, event_date, event_time)
            SELECT NULL, :d2, :t2
            WHERE NOT EXISTS (SELECT 1 FROM events WHERE event_date = :d2 AND event_time = :t2);
        """), {'d2': ev2_date, 't2': ev2_time})

        # Créer matchs :
        # - Pour ev1 : un match impliquant l'utilisateur (court 1) et un match sans lui (court 2)
        session.execute(text("""
            INSERT OR IGNORE INTO matches (id, event_id, team1_id, team2_id, court_number, status)
            SELECT NULL,
              (SELECT id FROM events WHERE event_date=:d1 AND event_time=:t1 LIMIT 1),
              (SELECT id FROM teams WHERE company='Team User-A'),
              (SELECT id FROM teams WHERE company='Team Other-A'), 1, 'A_VENIR'
            WHERE NOT EXISTS (
              SELECT 1 FROM matches m JOIN events e ON e.id = m.event_id WHERE e.event_date = :d1 AND e.event_time = :t1 AND m.court_number = 1
            );
        """), {'d1': ev1_date, 't1': ev1_time})

        session.execute(text("""
            INSERT OR IGNORE INTO matches (id, event_id, team1_id, team2_id, court_number, status)
            SELECT NULL,
              (SELECT id FROM events WHERE event_date=:d1 AND event_time=:t1 LIMIT 1),
              (SELECT id FROM teams WHERE company='Team Other-A'),
              (SELECT id FROM teams WHERE company='Team Stranger'), 2, 'A_VENIR'
            WHERE NOT EXISTS (
              SELECT 1 FROM matches m JOIN events e ON e.id = m.event_id WHERE e.event_date = :d1 AND e.event_time = :t1 AND m.court_number = 2
            );
        """), {'d1': ev1_date, 't1': ev1_time})

        # - Pour ev2 : deux matchs sans l'utilisateur
        session.execute(text("""
            INSERT OR IGNORE INTO matches (id, event_id, team1_id, team2_id, court_number, status)
            SELECT NULL,
              (SELECT id FROM events WHERE event_date=:d2 AND event_time=:t2 LIMIT 1),
              (SELECT id FROM teams WHERE company='Team Other-A'),
              (SELECT id FROM teams WHERE company='Team Stranger'), 1, 'A_VENIR'
            WHERE NOT EXISTS (
              SELECT 1 FROM matches m JOIN events e ON e.id = m.event_id WHERE e.event_date = :d2 AND e.event_time = :t2 AND m.court_number = 1
            );
        """), {'d2': ev2_date, 't2': ev2_time})

        session.execute(text("""
            INSERT OR IGNORE INTO matches (id, event_id, team1_id, team2_id, court_number, status)
            SELECT NULL,
              (SELECT id FROM events WHERE event_date=:d2 AND event_time=:t2 LIMIT 1),
              (SELECT id FROM teams WHERE company='Team Stranger'),
              (SELECT id FROM teams WHERE company='Team Other-A'), 2, 'A_VENIR'
            WHERE NOT EXISTS (
              SELECT 1 FROM matches m JOIN events e ON e.id = m.event_id WHERE e.event_date = :d2 AND e.event_time = :t2 AND m.court_number = 2
            );
        """), {'d2': ev2_date, 't2': ev2_time})

        session.commit()

        # Afficher résultats : tous les matchs pour ev1 et ev2, et ceux impliquant l'utilisateur
        print('\n✅ Matchs insérés/référencés :')
        rows = session.execute(text("SELECT m.id, e.event_date, e.event_time, m.court_number FROM matches m JOIN events e ON e.id = m.event_id WHERE e.event_date IN (:d1, :d2) ORDER BY e.event_date, m.court_number"), {'d1': ev1_date, 'd2': ev2_date}).fetchall()
        for r in rows:
            print(dict(r._mapping))

        print('\n🔎 Matchs impliquant user@padel.com :')
        user_rows = session.execute(text("""
            SELECT m.id, e.event_date, e.event_time, m.court_number
            FROM matches m
            JOIN events e ON e.id = m.event_id
            JOIN teams t1 ON t1.id = m.team1_id
            JOIN players p ON (p.id = t1.player1_id OR p.id = t1.player2_id)
            WHERE p.user_id = :uid
            UNION
            SELECT m.id, e.event_date, e.event_time, m.court_number
            FROM matches m
            JOIN events e ON e.id = m.event_id
            JOIN teams t2 ON t2.id = m.team2_id
            JOIN players p2 ON (p2.id = t2.player1_id OR p2.id = t2.player2_id)
            WHERE p2.user_id = :uid
            ORDER BY event_date, court_number
        """), {'uid': uid}).fetchall()
        for r in user_rows:
            print(dict(r._mapping))

    finally:
        session.close()


if __name__ == '__main__':
    main()
