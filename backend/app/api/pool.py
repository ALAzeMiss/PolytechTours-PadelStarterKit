from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.pool import PoolCreate, PoolResponse
from app.crud import pool as crud_pool
from app.api.deps import get_current_admin

router = APIRouter()

@router.post("/", response_model=PoolResponse)
def create_pool(pool: PoolCreate, db: Session = Depends(get_db), current_admin = Depends(get_current_admin)):
    db_pool = crud_pool.get_pool(db, pool_id=pool.id)
    if db_pool:
        raise HTTPException(status_code=400, detail="Pool already exists")
    return crud_pool.create_pool(db=db, pool=pool)

@router.get("/", response_model=List[PoolResponse])
def read_pools(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pools = crud_pool.get_pools(db, skip=skip, limit=limit)
    return pools
