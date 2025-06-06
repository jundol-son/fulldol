# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, post, trade_router, price, kis_chart, stock, autobuy, autoconditions, autobuy_runner
from db.models import Base
from db.database import engine

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(trade_router.router)
app.include_router(price.router)
app.include_router(kis_chart.router)
app.include_router(stock.router)
app.include_router(autobuy.router)
app.include_router(autoconditions.router)
app.include_router(autobuy_runner.router)

# CORS 허용 설정 (★ 개발 중에는 allow_origins=["*"]로 열어두는 게 일반적)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 중엔 모든 출처 허용
    allow_credentials=True,
    allow_methods=["*"],  # POST, GET, OPTIONS 등 모두 허용
    allow_headers=["*"],
)
