# example: routers/stock.py
from fastapi import APIRouter
import FinanceDataReader as fdr
import pandas as pd

router = APIRouter(prefix="/stock", tags=["stock"])

# 전역 캐시
stock_df_cache = None

@router.get("/stock-list")
def get_stock_list():
    df = fdr.StockListing("KRX")
    df = df[["Name", "Code"]]
    df["display"] = df["Name"] + " (" + df["Code"] + ")"
    return df.to_dict(orient="records")

@router.get("/search")
def search_all_stocks(query: str):
    global stock_df_cache

    if stock_df_cache is None:
        # 한국 주식
        krx = fdr.StockListing('KRX')[['Name', 'Code', 'Market']]
        krx['Nation'] = 'KR'

        # 미국 주식
        us_markets = {
            "NASDAQ": fdr.StockListing("NASDAQ"),
            "NYSE": fdr.StockListing("NYSE"),
            "AMEX": fdr.StockListing("AMEX"),
        }

        us_dfs = []
        for market_name, df in us_markets.items():
            df = df[['Name', 'Symbol']].rename(columns={'Symbol': 'Code'})
            df['Nation'] = 'US'
            df['Market'] = market_name
            us_dfs.append(df)

        all_df = pd.concat([krx] + us_dfs, ignore_index=True)
        all_df.dropna(subset=['Name', 'Code'], inplace=True)

        stock_df_cache = all_df  # ✅ 캐싱

    df = stock_df_cache
    q = query.lower()
    filtered = df[df['Name'].str.lower().str.contains(q) | df['Code'].str.lower().str.contains(q)]

    return filtered.head(30).to_dict(orient='records')