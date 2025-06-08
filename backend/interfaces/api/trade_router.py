from fastapi import APIRouter, Query, HTTPException, Depends
from pydantic import BaseModel
from infrastructure import kis_api
from sqlalchemy.orm import Session
from infrastructure.database import SessionLocal
from schemas.trade import TradeOut
from typing import List, Optional

router = APIRouter(prefix="/kis", tags=["KIS API"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/price")
def read_price(stock_code: str = Query(..., description="종목코드 (예: 005930)")):
    return kis_api.get_price(stock_code)

@router.get("/balance")
def read_balance():
    data = kis_api.get_balance()  # 기존 호출 함수
    return {
        "summary": data.get("output2", [{}])[0],
        "stocks": data.get("output1", [])
    }

class OrderRequest(BaseModel):
    code: str      # 종목코드 (숫자 or 영문)
    price: int     # 주문가
    qty: int       # 수량
    side: str      # 'buy' 또는 'sell'

@router.post("/order")
def place_stock_order(order: OrderRequest, db: Session = Depends(get_db)):
    try:
        result = kis_api.place_order(
            code=order.code,
            price=order.price,
            qty=order.qty,
            side=order.side.lower()
        )

        # 주문 성공 시 거래 내역 저장
        if result.get("rt_cd") == "0":
            trade_data = {
                "code": order.code,
                "side": order.side.lower(),
                "price": order.price,
                "qty": order.qty,
                "total_price": order.price * order.qty,
            }

            kis_api.save_trade(db, trade_data)

        return {
            "status": "ok",
            "message": result.get("msg1", "주문 완료"),
            "result": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ 주문 실패: {str(e)}")

@router.get("/market-status")
def check_market_status(code: str, market: str = Query(...)):
    try:
        result = kis_api.is_market_open_for_stock(code, market)
        return result
    except Exception as e:
        return {"market_open": False, "message": str(e)}

@router.get("/trade-history", response_model=List[TradeOut])
def read_trade_history(code: Optional[str] = Query(None), db: Session = Depends(get_db)):
    return kis_api.get_trade_history(db, code)

