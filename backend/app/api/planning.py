# ============================================
# FICHIER : backend/app/api/planning.py
# ============================================

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.api.deps import get_current_user
from app.models.models import User

router = APIRouter(prefix="/events", tags=["events"])


def parse_date(s: str):
	try:
		return datetime.strptime(s, "%Y-%m-%d").date()
	except Exception:
		raise HTTPException(status_code=400, detail="Format de date attendu: YYYY-MM-DD")


@router.get("/")
def events_range(start: str = Query(..., description="YYYY-MM-DD"), end: str = Query(..., description="YYYY-MM-DD"), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
	"""Retourne les événements et matchs entre deux dates (inclusives).

	La réponse contient une liste d'objets { event_id, event_date, event_time, matches: [...] }
	"""
	start_date = parse_date(start)
	end_date = parse_date(end)

	# Inclure info sur joueurs pour calculer si l'utilisateur est dans une des équipes
	sql = text(
		"""
		SELECT e.id as event_id, e.event_date, e.event_time,
		       m.id as match_id, m.team1_id, m.team2_id, m.court_number, m.status, m.score_team1, m.score_team2,
		       CASE WHEN (p1.user_id = :uid OR p2.user_id = :uid) THEN 1 ELSE 0 END as user_in_team1,
		       CASE WHEN (p3.user_id = :uid OR p4.user_id = :uid) THEN 1 ELSE 0 END as user_in_team2
		FROM events e
		LEFT JOIN matches m ON m.event_id = e.id
		LEFT JOIN teams t1 ON t1.id = m.team1_id
		LEFT JOIN players p1 ON p1.id = t1.player1_id
		LEFT JOIN players p2 ON p2.id = t1.player2_id
		LEFT JOIN teams t2 ON t2.id = m.team2_id
		LEFT JOIN players p3 ON p3.id = t2.player1_id
		LEFT JOIN players p4 ON p4.id = t2.player2_id
		WHERE e.event_date BETWEEN :start_date AND :end_date
		ORDER BY e.event_date, e.event_time, m.court_number
		"""
	)

	res = db.execute(sql, {"start_date": start_date.isoformat(), "end_date": end_date.isoformat(), "uid": current_user.id}).fetchall()

	# Grouper par event
	events = {}
	for row in res:
		rec = row._mapping if hasattr(row, "_mapping") else row
		eid = rec["event_id"]
		if eid not in events:
			events[eid] = {
				"event_id": eid,
				"event_date": rec["event_date"].isoformat() if isinstance(rec["event_date"], datetime) else str(rec["event_date"]),
				"event_time": str(rec["event_time"]) if rec["event_time"] is not None else None,
				"matches": []
			}

		if rec["match_id"] is not None:
			events[eid]["matches"].append({
				"match_id": rec["match_id"],
				"team1_id": rec["team1_id"],
				"team2_id": rec["team2_id"],
				"court_number": rec["court_number"],
				"status": rec["status"],
				"score_team1": rec["score_team1"],
				"score_team2": rec["score_team2"],
				"user_in_team1": bool(rec["user_in_team1"]),
				"user_in_team2": bool(rec["user_in_team2"])
			})

	return list(events.values())


@router.get("/day/{day}")
def planning_day(day: str, db: Session = Depends(get_db)):
	"""Retourne les détails (événements + matchs + équipes) pour une date donnée (YYYY-MM-DD)."""
	target = parse_date(day)

	# Requête pour récupérer les matchs et enrichir avec les infos d'équipes et joueurs
	sql = text(
		"""
		SELECT m.id as match_id, m.court_number, m.status, m.score_team1, m.score_team2,
			   e.id as event_id, e.event_time,
			   t1.id as team1_id, t1.company as team1_company,
			   p1.first_name as t1_p1_first, p1.last_name as t1_p1_last,
			   p2.first_name as t1_p2_first, p2.last_name as t1_p2_last,
			   t2.id as team2_id, t2.company as team2_company,
			   p3.first_name as t2_p1_first, p3.last_name as t2_p1_last,
			   p4.first_name as t2_p2_first, p4.last_name as t2_p2_last
		FROM events e
		JOIN matches m ON m.event_id = e.id
		LEFT JOIN teams t1 ON t1.id = m.team1_id
		LEFT JOIN players p1 ON p1.id = t1.player1_id
		LEFT JOIN players p2 ON p2.id = t1.player2_id
		LEFT JOIN teams t2 ON t2.id = m.team2_id
		LEFT JOIN players p3 ON p3.id = t2.player1_id
		LEFT JOIN players p4 ON p4.id = t2.player2_id
		WHERE e.event_date = :target_date
		ORDER BY m.court_number
		"""
	)

	rows = db.execute(sql, {"target_date": target.isoformat()}).fetchall()

	matches = []
	for r in rows:
		rec = r._mapping if hasattr(r, "_mapping") else r
		team1_players = []
		if rec["t1_p1_first"]:
			team1_players.append(f"{rec['t1_p1_first']} {rec['t1_p1_last']}")
		if rec["t1_p2_first"]:
			team1_players.append(f"{rec['t1_p2_first']} {rec['t1_p2_last']}")

		team2_players = []
		if rec["t2_p1_first"]:
			team2_players.append(f"{rec['t2_p1_first']} {rec['t2_p1_last']}")
		if rec["t2_p2_first"]:
			team2_players.append(f"{rec['t2_p2_first']} {rec['t2_p2_last']}")

		matches.append({
			"match_id": rec["match_id"],
			"court_number": rec["court_number"],
			"status": rec["status"],
			"score_team1": rec["score_team1"],
			"score_team2": rec["score_team2"],
			"event_id": rec["event_id"],
			"event_time": str(rec["event_time"]) if rec["event_time"] is not None else None,
			"team1": {
				"id": rec["team1_id"],
				"company": rec["team1_company"],
				"players": team1_players
			},
			"team2": {
				"id": rec["team2_id"],
				"company": rec["team2_company"],
				"players": team2_players
			}
		})

	return {"date": target.isoformat(), "matches": matches}


@router.get("/my-events")
def my_events(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
	"""Retourne les matchs auxquels l'utilisateur connecté participe.

	La participation est déterminée par `players.user_id` (les players rattachés à l'utilisateur).
	Renvoie la liste des matchs avec info équipe, joueurs, date/heure d'événement, piste, statut et score.
	"""
	uid = current_user.id

	sql = text(
		"""
		SELECT m.id as match_id, m.court_number, m.status, m.score_team1, m.score_team2,
			   e.id as event_id, e.event_date, e.event_time,
			   t1.id as team1_id, t1.company as team1_company,
			   p1.first_name as t1_p1_first, p1.last_name as t1_p1_last,
			   p2.first_name as t1_p2_first, p2.last_name as t1_p2_last,
			   t2.id as team2_id, t2.company as team2_company,
			   p3.first_name as t2_p1_first, p3.last_name as t2_p1_last,
			   p4.first_name as t2_p2_first, p4.last_name as t2_p2_last
		FROM matches m
		JOIN events e ON e.id = m.event_id
		LEFT JOIN teams t1 ON t1.id = m.team1_id
		LEFT JOIN players p1 ON p1.id = t1.player1_id
		LEFT JOIN players p2 ON p2.id = t1.player2_id
		LEFT JOIN teams t2 ON t2.id = m.team2_id
		LEFT JOIN players p3 ON p3.id = t2.player1_id
		LEFT JOIN players p4 ON p4.id = t2.player2_id
		WHERE (p1.user_id = :uid OR p2.user_id = :uid OR p3.user_id = :uid OR p4.user_id = :uid)
		ORDER BY e.event_date, m.court_number
		"""
	)

	rows = db.execute(sql, {"uid": uid}).fetchall()

	matches = []
	for r in rows:
		rec = r._mapping if hasattr(r, "_mapping") else r
		team1_players = []
		if rec["t1_p1_first"]:
			team1_players.append(f"{rec['t1_p1_first']} {rec['t1_p1_last']}")
		if rec["t1_p2_first"]:
			team1_players.append(f"{rec['t1_p2_first']} {rec['t1_p2_last']}")

		team2_players = []
		if rec["t2_p1_first"]:
			team2_players.append(f"{rec['t2_p1_first']} {rec['t2_p1_last']}")
		if rec["t2_p2_first"]:
			team2_players.append(f"{rec['t2_p2_first']} {rec['t2_p2_last']}")

		matches.append({
			"match_id": rec["match_id"],
			"court_number": rec["court_number"],
			"status": rec["status"],
			"score_team1": rec["score_team1"],
			"score_team2": rec["score_team2"],
			"event_id": rec["event_id"],
			"event_date": rec["event_date"].isoformat() if isinstance(rec["event_date"], datetime) else str(rec["event_date"]),
			"event_time": str(rec["event_time"]) if rec["event_time"] is not None else None,
			"team1": {
				"id": rec["team1_id"],
				"company": rec["team1_company"],
				"players": team1_players
			},
			"team2": {
				"id": rec["team2_id"],
				"company": rec["team2_company"],
				"players": team2_players
			}
		})

	return {"matches": matches}