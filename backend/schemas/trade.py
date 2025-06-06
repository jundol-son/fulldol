from pydantic import BaseModel
from datetime import datetime

class TradeCreate(BaseModel):
    code: str
    side: str
    price: float
    qty: int

class TradeOut(TradeCreate):
    id: int
    total_price: float
    trade_time: datetime

    class Config:
        orm_mode = True
