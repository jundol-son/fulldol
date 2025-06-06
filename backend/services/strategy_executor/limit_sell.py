from typing import Dict, Any
from services import kis_api

def extract_float(value: Any) -> float:
    """중첩 dict 또는 문자열로 된 수치 값을 float으로 변환"""
    if isinstance(value, dict):
        return float(value.get("value", 0))
    return float(value)

def execute_condition_limit_sell(strategy: Dict[str, Any]) -> Dict[str, Any]:
    """
    현재가가 지정가 이상일 때 매도 실행
    """
    try:
        cond = strategy["condition_value"]
        price = extract_float(cond.get("price"))
        price_data = kis_api.get_price(strategy["code"])
        current_price = float(price_data["output"]["stck_prpr"].replace(",", ""))

        if current_price >= price:
            return kis_api.place_order(
                code=strategy["code"],
                price=price,
                qty=strategy["quantity"],
                side="sell"
            )
        else:
            return {"executed": False, "reason": "현재가가 지정가보다 낮음"}
    except Exception as e:
        return {"executed": False, "error": str(e)}