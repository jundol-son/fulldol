from fastapi import APIRouter, Query
from typing import List
from schemas.price import PricePoint
from services.kis_api import get_price_history_service

router = APIRouter(prefix="/kis", tags=["KIS API"])

@router.get("/price-history", response_model=List[PricePoint])
def price_history(code: str = Query(...)):
    return get_price_history_service(code)