from typing import List, Optional
from pydantic import BaseModel

class InputField(BaseModel):
    key: str
    label: str
    type: str
    required: bool

class AutoConditionBase(BaseModel):
    name: str
    key: str  # ✅ 여기에 key 필드 추가
    description: Optional[str] = None
    side: str
    inputs: Optional[List[InputField]] = []

class AutoConditionCreate(AutoConditionBase):
    pass

class AutoConditionOut(AutoConditionBase):
    id: int

    class Config:
        orm_mode = True