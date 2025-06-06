from typing import Dict, Any
from services import kis_api


def execute_condition_limit_buy(strategy: Dict[str, Any]) -> Dict[str, Any]:
    """
    현재가가 지정가 이하일 때 매수 실행
    """
    try:
        price = float(strategy["condition_value"].get("price", 0))
        current_price = float(kis_api.get_price(strategy["code"]))

        if current_price <= price:
            return kis_api.place_order(
                code=strategy["code"],
                price=price,
                qty=strategy["quantity"],
                side="buy"
            )
        else:
            return {"executed": False, "reason": "현재가가 지정가보다 높음"}
    except Exception as e:
        return {"executed": False, "error": str(e)}


def execute_condition_limit_sell(strategy: Dict[str, Any]) -> Dict[str, Any]:
    """
    현재가가 지정가 이상일 때 매도 실행
    """
    try:
        price = float(strategy["condition_value"].get("price", 0))
        current_price = float(kis_api.get_price(strategy["code"]))

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


def execute_condition_gain_ratio(strategy: Dict[str, Any]) -> Dict[str, Any]:
    """
    TODO: 수익률 조건 계산 및 보유일 조건 반영 필요
    """
    return {"executed": False, "reason": "수익률 조건 로직 미구현"}


# 조건 key → 실행 함수 매핑
CONDITION_EXECUTORS: Dict[str, Any] = {
    "limit_buy": execute_condition_limit_buy,
    "limit_sell": execute_condition_limit_sell,
    "gain_ratio": execute_condition_gain_ratio
}
