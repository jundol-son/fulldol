"""
KIS OpenAPI 직접 연동 모듈 (모의투자 기준)
- 종목 시세 조회
- 잔고 조회
- 지정가 주문
"""

import os
import requests
from dotenv import load_dotenv
import datetime
from sqlalchemy.orm import Session
from domain.models import TradeHistory
from datetime import datetime, date
from typing import List
from schemas.price import PricePoint

load_dotenv()

APP_KEY = os.getenv("APP_KEY")
APP_SECRET = os.getenv("APP_SECRET")
ACC_NO = os.getenv("ACCOUNT_NO")  # 예: "12345678-01"

BASE_URL = "https://openapivts.koreainvestment.com:29443"  # 모의투자용

def get_access_token() -> str:
    """한투 API 토큰 발급"""
    url = f"{BASE_URL}/oauth2/token"
    data = {
        "grant_type": "client_credentials",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    res = requests.post(url, data=data, headers=headers)
    res.raise_for_status()
    return res.json()["access_token"]


def get_price(stock_code: str) -> dict:
    """종목 시세 조회"""
    token = get_access_token()
    url = f"{BASE_URL}/uapi/domestic-stock/v1/quotations/inquire-price"
    headers = {
        "authorization": f"Bearer {token}",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET,
        "tr_id": "FHKST01010100",  # 실시간 시세 조회
        "custtype": "P"
    }
    params = {
        "fid_cond_mrkt_div_code": "J",
        "fid_input_iscd": stock_code
    }
    res = requests.get(url, headers=headers, params=params)
    res.raise_for_status()
    return res.json()


def get_balance() -> dict:
    """잔고 조회 (모의투자 기준)"""
    token = get_access_token()
    url = f"{BASE_URL}/uapi/domestic-stock/v1/trading/inquire-balance"
    headers = {
        "authorization": f"Bearer {token}",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET,
        "tr_id": "VTTC8434R",
        "custtype": "P"
    }
    params = {
        "CANO": ACC_NO.split('-')[0],
        "ACNT_PRDT_CD": ACC_NO.split('-')[1],
        "AFHR_FLPR_YN": "N",
        "OFL_YN": "",
        "INQR_DVSN": "02",
        "UNPR_DVSN": "01",
        "FUND_STTL_ICLD_YN": "N",
        "FNCG_AMT_AUTO_RDPT_YN": "N",
        "PRCS_DVSN": "01",
        "CTX_AREA_FK100": "",
        "CTX_AREA_NK100": ""
    }
    res = requests.get(url, headers=headers, params=params)
    res.raise_for_status()
    return res.json()


def place_order(code: str, price: int, qty: int, side: str = "buy") -> dict:
    """
    지정가 주문 실행 (모의투자)
    :param stock_code: 종목코드 (예: "005930")
    :param price: 주문가
    :param qty: 수량
    :param side: 'buy' 또는 'sell'
    """
    token = get_access_token()
    is_domestic = code.isdigit()
    is_buy = side == "buy"

    if is_domestic:
        # ✅ 국내주식 주문
        url = f"{BASE_URL}/uapi/domestic-stock/v1/trading/order-cash"
        headers = {
            "authorization": f"Bearer {token}",
            "appkey": APP_KEY,
            "appsecret": APP_SECRET,
            "tr_id": "VTTC0802U" if is_buy else "VTTC0801U",
            "custtype": "P"
        }
        data = {
            "CANO": ACC_NO.split('-')[0],
            "ACNT_PRDT_CD": ACC_NO.split('-')[1],
            "PDNO": code,
            "ORD_DVSN": "00",  # 지정가
            "ORD_QTY": str(qty),
            "ORD_UNPR": str(price),
            "CTAC_TLNO": "",
            "MGCO_APTM_ODNO": "",
            "ORD_DVSN_CCST_ID": "",
            "ORD_DVSN_CCST_VL": ""
        }

    else:
        # ✅ 미국주식 주문
        url = f"{BASE_URL}/uapi/overseas-stock/v1/trading/order"
        headers = {
            "authorization": f"Bearer {token}",
            "appkey": APP_KEY,
            "appsecret": APP_SECRET,
            "tr_id": "VTTT1002U" if is_buy else "VTTT1001U",  # 모의투자용 트랜잭션 ID
            "custtype": "P"
        }
        data = {
            "CANO": ACC_NO.split('-')[0],
            "ACNT_PRDT_CD": ACC_NO.split('-')[1],
            "OVRS_EXCG_CD": "NASD",    # 나스닥 기준, 필요시 동적으로 변경 가능
            "PDNO": code,              # 예: "AAPL"
            "ORD_DVSN": "00",          # 지정가
            "ORD_QTY": str(qty),
            "ORD_UNPR": str(price)
        }

    res = requests.post(url, headers=headers, json=data)
    res.raise_for_status()
    return res.json()

def get_excd_from_market(market: str) -> str:
    mapping = {
        "NASDAQ": "NASD",
        "NYSE": "NYSE",
        "AMEX": "AMEX"
    }
    return mapping.get(market.upper(), "NASD")

def is_market_open_for_stock(code: str, market: str):
    token = get_access_token()

    if market in ["KOSPI", "KOSDAQ", "KRX"]:
        # 🇰🇷 국내 주식 처리
        url = f"{BASE_URL}/uapi/domestic-stock/v1/quotations/inquire-asking-price-exp-ccn"
        headers = {
            "Content-Type": "application/json",
            "authorization": f"Bearer {token}",
            "appkey": APP_KEY,
            "appsecret": APP_SECRET,
            "tr_id": "FHKST01010200",
            "custtype": "P"
        }
        params = {
            "fid_cond_mrkt_div_code": "J",
            "fid_input_iscd": code
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        print("📦 Raw output(KR):", data)

        price = data.get("output2", {}).get("stck_prpr", "")
        market_open = data.get("output1", {}).get("new_mkop_cls_code", "") == "20"
        msg = data.get("msg1", "처리결과 없음")

        return {
            "market_open": market_open,
            "current_price": price,
            "message": "장 운영 중" if market_open else "장 마감",
            "status": msg
        }

    elif market in ["NASDAQ", "NYSE", "AMEX"]:
        # 🇺🇸 미국 주식 처리
        url = f"{BASE_URL}/uapi/overseas-price/v1/quotations/dailyprice"
        today = datetime.today().strftime("%Y%m%d")
        headers = {
            "authorization": f"Bearer {token}",
            "appkey": APP_KEY,
            "appsecret": APP_SECRET,
            "tr_id": "HHDFS76240000",
            "custtype": "P"
        }
        params = {
            "GUBN": "0",
            "EXCD": get_excd_from_market(market),
            "SYMB": code,
            "BYMD": today,
            "MODP": "0"
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        print("📦 Raw output(US):", data)

        prices = data.get("output", [])

        if prices:
            today_price = prices[0]
            return {
                "market_open": True,
                "date": today_price.get("bas_dt"),
                "open_price": today_price.get("stck_oprc"),
                "high_price": today_price.get("stck_hgpr"),
                "low_price": today_price.get("stck_lwpr"),
                "close_price": today_price.get("stck_clpr"),
                "message": "장 운영 중",
                "status": data.get("msg1", "")
            }
        else:
            return {
                "market_open": False,
                "message": "장 마감 또는 데이터가 없음",
                "date": today,
                "close_price": "-",
                "status": data.get("msg1", "")
            }

    else:
        return {
            "market_open": False,
            "message": f"알 수 없는 시장 구분: {market}",
            "status": "market_error"
        }



def order_stock(code: str, price: int, qty: int, side: str = "buy") -> dict:
    """
    장 상태에 따라 주문 또는 예약주문 수행
    :param code: 종목코드 (국내 6자리, 해외 티커)
    :param price: 지정가
    :param qty: 수량
    :param side: 'buy' or 'sell'
    :return: 주문 결과 dict
    """
    market_info = is_market_open_for_stock(code)

    if market_info["market_open"]:
        result = place_order(code, price, qty, side)
        return {
            "success": True,
            "message": "정상 주문 완료",
            "order_result": result
        }
    else:
        # 예약 주문 로직을 구현하려면 DB 저장 또는 별도 큐 관리 필요
        return {
            "success": False,
            "message": f"{market_info['message']} - 장이 열리지 않아 예약주문이 필요합니다.",
            "order_result": None
        }
    
def save_trade(db: Session, trade_data: dict):
    from domain.models import TradeHistory
    trade = TradeHistory(**trade_data)
    db.add(trade)
    db.commit()
    db.refresh(trade)
    return trade

def get_trade_history(db: Session, code: str = None) -> List[TradeHistory]:
    query = db.query(TradeHistory).order_by(TradeHistory.trade_time.desc())
    if code:
        query = query.filter(TradeHistory.code == code)
    return query.all()

def get_price_history(code: str):
    # KIS의 일봉 데이터 요청 (예: 1일 간의 시세 히스토리)
    ACCESS_TOKEN = get_access_token()
    BASE_URL = "https://openapivts.koreainvestment.com:29443"  # 모의투자 기준
    endpoint = "/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"

    headers = {
        "authorization": f"Bearer {ACCESS_TOKEN}",
        "appkey": os.getenv("APP_KEY"),
        "appsecret": os.getenv("APP_SECRET"),
        "tr_id": "FHKST03010100"  # 실전: FHKST03010100 / 모의: VT로 시작
    }

    params = {
        "fid_cond_mrkt_div_code": "J",       # 주식: 'J'
        "fid_input_iscd": code,              # 종목코드
        "fid_org_adj_prc": "1",
        "fid_period_div_code": "D",          # 일간 데이터
        "fid_chart_prc": "1"
    }

    response = requests.get(BASE_URL + endpoint, headers=headers, params=params)
    data = response.json()

    price_data = []
    for item in data.get("output2", []):
        # 날짜 + 종가 데이터만 추출
        date_str = item["stck_bsop_date"]  # '20240604'
        price = float(item["stck_clpr"])
        date_obj = datetime.strptime(date_str, "%Y%m%d")
        price_data.append({"time": date_obj, "price": price})

    return price_data

def get_price_history_service(code: str) -> List[PricePoint]:
    raw_data = get_price_history(code)
    return [PricePoint(time=item["time"], price=item["price"]) for item in raw_data]