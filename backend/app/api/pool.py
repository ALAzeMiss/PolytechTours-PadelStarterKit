# ============================================
# FICHIER : backend/app/api/pool.py
# ============================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.models import Pool, Team
from app.schemas.pool import PoolCreate, PoolResponse
from app.api.deps import get_current_admin

router = APIRouter(prefix="/pools", tags=["pools"])

@router.post("/", response_model=PoolResponse)
def create_pool(pool_data: PoolCreate, db: Session = Depends(get_db), current_admin = Depends(get_current_admin)):
    # Vérifier qu'une poule avec ce nom n'existe pas déjà
    existing_pool = db.query(Pool).filter(Pool.name == pool_data.name).first()
    if existing_pool:
        raise HTTPException(status_code=409, detail="Une poule avec ce nom existe déjà")
    
    # Vérifier que les équipes existent et ne sont pas déjà dans une autre poule
    teams = []
    for team_id in pool_data.team_ids:
        team = db.query(Team).filter(Team.id == team_id).first()
        if not team:
            raise HTTPException(status_code=404, detail=f"Équipe {team_id} introuvable")
        if team.pool_id is not None:
            raise HTTPException(status_code=400, detail=f"Équipe {team_id} est déjà dans une poule")
        teams.append(team)
    
    db_pool = Pool(name=pool_data.name)
    db.add(db_pool)
    db.commit()
    db.refresh(db_pool)
    
    # Assigner les équipes à la poule
    for team in teams:
        team.pool_id = db_pool.id
    db.commit()
    
    return db_pool

@router.get("/", response_model=List[PoolResponse])
def get_pools(db: Session = Depends(get_db)):
    pools = db.query(Pool).all()
    return pools

@router.get("/{pool_id}", response_model=PoolResponse)
def get_pool(pool_id: int, db: Session = Depends(get_db)):
    pool = db.query(Pool).filter(Pool.id == pool_id).first()
    if not pool:
        raise HTTPException(status_code=404, detail="Poule introuvable")
    return pool

@router.put("/{pool_id}", response_model=PoolResponse)
def update_pool(pool_id: int, pool_data: PoolCreate, db: Session = Depends(get_db), current_admin = Depends(get_current_admin)):
    pool = db.query(Pool).filter(Pool.id == pool_id).first()
    if not pool:
        raise HTTPException(status_code=404, detail="Poule introuvable")
    
    # Vérifier qu'une autre poule n'a pas ce nom
    existing_pool = db.query(Pool).filter(Pool.name == pool_data.name, Pool.id != pool_id).first()
    if existing_pool:
        raise HTTPException(status_code=409, detail="Une poule avec ce nom existe déjà")
    
    pool.name = pool_data.name
    db.commit()
    db.refresh(pool)
    return pool

@router.delete("/{pool_id}")
def delete_pool(pool_id: int, db: Session = Depends(get_db), current_admin = Depends(get_current_admin)):
    pool = db.query(Pool).filter(Pool.id == pool_id).first()
    if not pool:
        raise HTTPException(status_code=404, detail="Poule introuvable")
    
    # Retirer les équipes de la poule
    db.query(Team).filter(Team.pool_id == pool_id).update({Team.pool_id: None})
    
    db.delete(pool)
    db.commit()
    return {"message": "Poule supprimée"}