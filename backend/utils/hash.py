# backend/utils/hash.py

from passlib.context import CryptContext

# bcrypt 알고리즘 사용 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 비밀번호 해시 함수
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# 비밀번호 검증 함수
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
