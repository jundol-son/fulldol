from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class AutoBuyStrategyBase(BaseModel):
    code: str
    name: str
    condition_id: int
    condition_value: Dict[str, str]  # JSON 필드
    quantity: int
    unit_price: Optional[int] = None
    is_active: Optional[bool] = True
    side: Optional[str] = "buy"

class AutoBuyStrategyCreate(AutoBuyStrategyBase):
    pass

class AutoBuyStrategyUpdate(BaseModel):
    is_active: Optional[bool]

class AutoBuyStrategyOut(AutoBuyStrategyBase):
    id: int
    last_executed: Optional[datetime]
    created_at: datetime

    class Config:
        orm_mode = True
