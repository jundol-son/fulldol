from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from infrastructure.database import SessionLocal
from domain import models
from datetime import datetime
from usecases.strategy_executor import CONDITION_EXECUTORS
import json

router = APIRouter(prefix="/auto-buy", tags=["AutoBuy Runner"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/run")
def run_auto_strategies(db: Session = Depends(get_db)):
    # 활성화된 전략 조회
    strategies = (
        db.query(models.AutoBuyStrategy)
        .filter(models.AutoBuyStrategy.is_active == True)
        .all()
    )

    results = []

    for strategy in strategies:
        # 조건 객체 접근
        condition = strategy.condition
        if not condition:
            results.append({
                "strategy_id": strategy.id,
                "executed": False,
                "error": "❌ 조건 정보 없음"
            })
            continue

        executor = CONDITION_EXECUTORS.get(condition.key)

        if not executor:
            results.append({
                "strategy_id": strategy.id,
                "executed": False,
                "error": f"❌ 지원되지 않는 조건 key: {condition.key}"
            })
            continue

        # 전략 dict 변환 후 실행
        strategy_dict = {
            "id": strategy.id,
            "code": strategy.code,
            "name": strategy.name,
            "side": strategy.side,
            "condition_value": json.loads(strategy.condition_value) if isinstance(strategy.condition_value, str) else strategy.condition_value,
            "quantity": strategy.quantity,
            "unit_price": strategy.unit_price,
        }

        result = executor(strategy_dict)

        # 실행 성공 시 last_executed 업데이트
        if result.get("executed"):
            strategy.last_executed = datetime.utcnow()
            db.commit()

        results.append({
            "strategy_id": strategy.id,
            "condition_key": condition.key,
            **result
        })

    return results
