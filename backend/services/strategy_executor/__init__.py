from .limit_buy import execute_condition_limit_buy
from .limit_sell import execute_condition_limit_sell
from .gain_ratio import execute_condition_gain_ratio

CONDITION_EXECUTORS = {
    "limit_buy": execute_condition_limit_buy,
    "limit_sell": execute_condition_limit_sell,
    "gain_ratio": execute_condition_gain_ratio,
}
