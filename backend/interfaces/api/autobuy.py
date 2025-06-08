from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from infrastructure.database import SessionLocal
from domain.models import AutoBuyStrategy
from schemas.autobuy import AutoBuyStrategyCreate, AutoBuyStrategyUpdate

router = APIRouter(prefix="/auto-buy", tags=["AutoBuy"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_all_strategies(db: Session = Depends(get_db)):
    return db.query(AutoBuyStrategy).order_by(AutoBuyStrategy.id.desc()).all()

@router.post("/")
def create_strategy(strategy: AutoBuyStrategyCreate, db: Session = Depends(get_db)):
    new_strategy = AutoBuyStrategy(**strategy.dict())
    db.add(new_strategy)
    db.commit()
    db.refresh(new_strategy)
    return new_strategy

@router.put("/{strategy_id}")
def update_strategy(strategy_id: int, update_data: AutoBuyStrategyUpdate, db: Session = Depends(get_db)):
    strategy = db.query(AutoBuyStrategy).filter_by(id=strategy_id).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(strategy, key, value)
    db.commit()
    return {"message": "Updated"}

@router.delete("/{strategy_id}")
def delete_strategy(strategy_id: int, db: Session = Depends(get_db)):
    strategy = db.query(AutoBuyStrategy).filter_by(id=strategy_id).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    db.delete(strategy)
    db.commit()
    return {"message": "Deleted"}
