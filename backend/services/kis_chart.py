# services/kis_chart.py
from utils import kis_domstk, kis_auth
import pandas as pd

def fetch_chart_data(code: str):
    try:
        kis_auth.auth()
        df = kis_domstk.get_inquire_daily_itemchartprice(output_dv="2", itm_no=code)

        df["Date"] = pd.to_datetime(df["stck_bsop_date"])
        df = df.sort_values("Date")

        df = df.rename(columns={
            "stck_oprc": "open",
            "stck_hgpr": "high",
            "stck_lwpr": "low",
            "stck_clpr": "close",
            "acml_vol": "volume"
        })[["Date", "open", "high", "low", "close", "volume"]]

        df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].apply(pd.to_numeric, errors="coerce")
        df.dropna(inplace=True)

        return {"status": "ok", "data": df.to_dict(orient="records")}

    except Exception as e:
        return {"status": "error", "message": str(e)}