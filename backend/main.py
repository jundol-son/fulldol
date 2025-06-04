# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, post
from db.models import Base
from db.database import engine

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(post.router)

# CORS 허용 설정 (★ 개발 중에는 allow_origins=["*"]로 열어두는 게 일반적)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 중엔 모든 출처 허용
    allow_credentials=True,
    allow_methods=["*"],  # POST, GET, OPTIONS 등 모두 허용
    allow_headers=["*"],
)
