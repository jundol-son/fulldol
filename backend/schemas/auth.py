# backend/schemas/auth.py

from pydantic import BaseModel

class RegisterRequest(BaseModel):
    username: str
    password: str
    email: str | None = None

class LoginRequest(BaseModel):
    username: str
    password: str
