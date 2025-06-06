from pydantic import BaseModel
from datetime import datetime

class PricePoint(BaseModel):
    time: datetime  # 예: 2025-06-05T09:00:00
    price: float    # 예: 71400.0
