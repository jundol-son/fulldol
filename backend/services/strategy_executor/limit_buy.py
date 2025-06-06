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