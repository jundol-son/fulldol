from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from infrastructure.database import SessionLocal
from domain.models import AutoCondition
from schemas.autobuycondition import AutoConditionCreate, AutoConditionOut

router = APIRouter(prefix="/conditions", tags=["조건"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=AutoConditionOut)
def create_condition(data: AutoConditionCreate, db: Session = Depends(get_db)):
    condition = AutoCondition(**data.dict())
    db.add(condition)
    db.commit()
    db.refresh(condition)
    return condition

@router.get("/", response_model=list[AutoConditionOut])
def get_conditions(db: Session = Depends(get_db)):
    return db.query(AutoCondition).order_by(AutoCondition.id.desc()).all()

@router.delete("/{condition_id}")
def delete_condition(condition_id: int, db: Session = Depends(get_db)):
    cond = db.query(AutoCondition).filter(AutoCondition.id == condition_id).first()
    if not cond:
        raise HTTPException(status_code=404, detail="조건 없음")
    db.delete(cond)
    db.commit()
    return {"message": "삭제 완료"}

@router.put("/{condition_id}", response_model=AutoConditionOut)
def update_condition(condition_id: int, data: AutoConditionCreate, db: Session = Depends(get_db)):
    cond = db.query(AutoCondition).filter(AutoCondition.id == condition_id).first()
    if not cond:
        raise HTTPException(status_code=404, detail="조건 없음")
    for key, value in data.dict().items():
        setattr(cond, key, value)
    db.commit()
    db.refresh(cond)
    return cond
