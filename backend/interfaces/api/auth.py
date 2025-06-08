# backend/routes/auth.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from infrastructure.database import SessionLocal
from domain.models import User
from schemas.auth import RegisterRequest, LoginRequest
from utils.hash import hash_password, verify_password

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register_user(req: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == req.username).first()
    if existing:
        raise HTTPException(status_code=409, detail="이미 존재하는 아이디입니다.")

    user = User(
        username=req.username,
        password_hash=hash_password(req.password),
        email=req.email
    )
    db.add(user)
    db.commit()
    return {"msg": "회원가입 성공"}

@router.post("/login")
def login_user(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req.username).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 일치하지 않습니다.")
    
    return {
        "msg": "로그인 성공",
        "username": user.username,  # ✅ Vue가 받을 수 있도록 key 추가!
        # "token": ...,  # 나중에 JWT 쓸 경우 여기에 토큰도 넣으면 됨
    }
