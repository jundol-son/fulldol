from pydantic import BaseModel
from datetime import datetime

class PostCreate(BaseModel):
    title: str
    content: str
    writer: str

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    writer: str
    created_at: datetime

    class Config:
        orm_mode = True  # SQLAlchemy 객체를 JSON으로 자동 변환

class DeleteRequest(BaseModel):
    writer: str