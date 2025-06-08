# routes/kis_chart.py
from fastapi import APIRouter, Query
from infrastructure.kis_chart import fetch_chart_data

router = APIRouter(prefix="/kis", tags=["KIS API"])

@router.get("/chart")
def get_chart(code: str = Query(..., description="종목 코드")):
    return fetch_chart_data(code)
