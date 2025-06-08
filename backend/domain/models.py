# backend/db/models.py

from sqlalchemy import Column, Integer, String, DateTime, Text, func, Float, Boolean, JSON, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    email = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    writer = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class TradeHistory(Base):
    __tablename__ = "trade_history"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, index=True)
    side = Column(String)  # 'buy' or 'sell'
    price = Column(Float)
    qty = Column(Integer)
    total_price = Column(Float)
    trade_time = Column(DateTime, default=datetime.utcnow)


class AutoCondition(Base):
    __tablename__ = "auto_condition"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    key = Column(String, nullable=False)
    description = Column(Text)
    side = Column(String, nullable=False)  # "buy" or "sell"
    inputs = Column(JSONB, nullable=True)

class AutoBuyStrategy(Base):
    __tablename__ = "auto_buy_strategy"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(Text, nullable=False)
    name = Column(Text)
    side = Column(Text, nullable=False)
    condition_id = Column(Integer, ForeignKey("auto_condition.id"), nullable=False)  # ✅ 이 줄이 중요!
    condition_value = Column(JSON, nullable=False, default={})
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Integer)
    is_active = Column(Boolean, default=True)
    last_executed = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP)

    condition = relationship("AutoCondition")  # class명이 AutoCondition일 경우

