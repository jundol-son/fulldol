import kis_auth as ka
import kis_domstk as kb

import pandas as pd

import sys

# 토큰 발급
ka.auth()


# import matplotlib.pyplot as plt

# df = kb.get_inquire_daily_itemchartprice(output_dv="2", itm_no="005930")
# df["stck_bsop_date"] = pd.to_datetime(df["stck_bsop_date"])
# df = df.sort_values("stck_bsop_date")

# plt.plot(df["stck_bsop_date"], df["stck_clpr"], label="종가")
# plt.title("삼성전자 일별 종가 추이")
# plt.xlabel("날짜")
# plt.ylabel("종가")
# plt.grid(True)
# plt.legend()
# plt.tight_layout()
# plt.show()

# import mplfinance as mpf

# df = kb.get_inquire_daily_itemchartprice(output_dv="2", itm_no="005930")
# df["Date"] = pd.to_datetime(df["stck_bsop_date"])
# df = df.sort_values("Date")

# # 컬럼 정리
# ohlc_df = df.rename(columns={
#     "stck_oprc": "Open",
#     "stck_hgpr": "High",
#     "stck_lwpr": "Low",
#     "stck_clpr": "Close",
#     "acml_vol": "Volume"
# })[["Date", "Open", "High", "Low", "Close", "Volume"]]

# # ✅ 숫자형 변환
# ohlc_df[["Open", "High", "Low", "Close", "Volume"]] = ohlc_df[["Open", "High", "Low", "Close", "Volume"]].apply(pd.to_numeric, errors='coerce')

# # ✅ NaN 제거 또는 대체
# ohlc_df.dropna(inplace=True)  # 또는 .fillna(0)

# # ✅ 인덱스 설정
# ohlc_df.set_index("Date", inplace=True)

# # 차트 그리기
# mpf.plot(ohlc_df, type='candle', style='charles', volume=True, title="삼성전자 캔들차트")