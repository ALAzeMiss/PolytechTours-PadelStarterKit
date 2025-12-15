# ============================================
# FICHIER : backend/app/models/models.py
# ============================================

from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Date, Time
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship
import enum

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)  # JOUEUR ou ADMINISTRATEUR
    is_active = Column(Boolean, default=True)
    must_change_password = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class LoginAttempt(Base):
    __tablename__ = "login_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, nullable=False)
    attempts_count = Column(Integer, default=0)
    last_attempt = Column(DateTime(timezone=True))
    locked_until = Column(DateTime(timezone=True), nullable=True)


class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    company = Column(String, nullable=False)
    license_number = Column(String, unique=True, nullable=False)
    birth_date = Column(Date, nullable=True)
    photo_url = Column(String, nullable=True)
    # email = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    user = relationship("User", backref="player", uselist=False)


class Pool(Base):
    __tablename__ = "pools"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    teams = relationship("Team", back_populates="pools")


class Team(Base):
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False)
    player1_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    player2_id = Column(Integer, ForeignKey("players.id"), nullable=False)

    pool_id = Column(Integer, ForeignKey("pools.id"), nullable=True)

    player1 = relationship("Player", foreign_keys=[player1_id])
    player2 = relationship("Player", foreign_keys=[player2_id])
    pools = relationship("Pool", back_populates="teams")
    matches_as_team1 = relationship("Match", back_populates="team1", foreign_keys='Match.team1_id')
    matches_as_team2 = relationship("Match", back_populates="team2", foreign_keys='Match.team2_id')


class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    event_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    matches = relationship("Match", back_populates="event")


class MatchStatus(str, enum.Enum):
    A_VENIR = "A_VENIR"
    ANNULE = "ANNULE"
    TERMINE = "TERMINE"


class Match(Base):
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True, index=True)
    team1_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    team2_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    match_date = Column(Date, nullable=False)
    match_time = Column(Time, nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=True)
    court_number = Column(Integer, nullable=False)
    status = Column(String, default=MatchStatus.A_VENIR, nullable=False)
    score_team1 = Column(Integer, nullable=True)
    score_team2 = Column(Integer, nullable=True)

    team1 = relationship("Team", back_populates="matches_as_team1", foreign_keys=[team1_id])
    team2 = relationship("Team", back_populates="matches_as_team2", foreign_keys=[team2_id])
    event = relationship("Event", back_populates="matches")