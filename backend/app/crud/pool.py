from sqlalchemy.orm import Session
from app.models.models import Pool
from app.schemas.pool import PoolCreate

def get_pool(db: Session, pool_id: str):
    return db.query(Pool).filter(Pool.id == pool_id).first()

def create_pool(db: Session, pool: PoolCreate):
    db_pool = Pool(id=pool.id)
    db.add(db_pool)
    db.commit()
    db.refresh(db_pool)
    return db_pool

def get_pools(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Pool).offset(skip).limit(limit).all()
