"""
Database models for Stock Prediction API
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum

Base = declarative_base()

# ============================================================================
# PREDICTION MODELS
# ============================================================================

class StockPredictionModel(Base):
    """Stock prediction database model"""
    
    __tablename__ = "stock_predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    timeframe = Column(String)
    technical_score = Column(Float)
    news_sentiment_score = Column(Float, nullable=True)
    final_score = Column(Float)
    prediction = Column(String)  # BUY, SELL, HOLD
    confidence = Column(Float)
    target_price = Column(Float)
    technical_reason = Column(String)
    reason = Column(String, nullable=True)
    news_reason = Column(String, nullable=True)
    articles_analyzed = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# ============================================================================
# ACCOUNT MODELS
# ============================================================================

class UserAccountModel(Base):
    """User account database model"""
    
    __tablename__ = "user_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    sharekhan_user_id = Column(String, nullable=True)
    access_token = Column(String, nullable=True)
    is_authenticated = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

class PortfolioModel(Base):
    """Portfolio database model"""
    
    __tablename__ = "portfolios"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    account_balance = Column(Float, default=0)
    portfolio_value = Column(Float, default=0)
    total_profit = Column(Float, default=0)
    profit_percent = Column(Float, default=0)
    cash_available = Column(Float, default=0)
    margin_available = Column(Float, default=0)
    holdings_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class HoldingModel(Base):
    """Holding database model"""
    
    __tablename__ = "holdings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    symbol = Column(String, index=True)
    quantity = Column(Integer)
    current_price = Column(Float)
    buy_price = Column(Float)
    profit = Column(Float)
    profit_percent = Column(Float)
    value = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class OrderModel(Base):
    """Order database model"""
    
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    order_id = Column(String, unique=True, index=True)
    symbol = Column(String, index=True)
    quantity = Column(Integer)
    price = Column(Float)
    order_type = Column(String)  # BUY, SELL
    status = Column(String)  # OPEN, EXECUTED, CANCELLED
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    executed_quantity = Column(Integer, default=0)

class TradeModel(Base):
    """Trade database model"""
    
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    trade_id = Column(String, unique=True, index=True)
    symbol = Column(String, index=True)
    quantity = Column(Integer)
    price = Column(Float)
    trade_type = Column(String)  # BUY, SELL
    timestamp = Column(DateTime, default=datetime.utcnow)
    exchange = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# ============================================================================
# NEWS MODELS
# ============================================================================

class NewsArticleModel(Base):
    """News article database model"""
    
    __tablename__ = "news_articles"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    headline = Column(String)
    source = Column(String)
    sentiment = Column(String)  # POSITIVE, NEGATIVE, NEUTRAL
    sentiment_score = Column(Float)
    impact_level = Column(String)  # HIGH, MEDIUM, LOW
    url = Column(String, nullable=True)
    published_at = Column(DateTime)
    fetched_at = Column(DateTime, default=datetime.utcnow)

# ============================================================================
# WATCHLIST MODELS
# ============================================================================

class WatchlistItemModel(Base):
    """Watchlist item database model"""
    
    __tablename__ = "watchlist_items"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    symbol = Column(String, index=True)
    added_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(String, nullable=True)

# ============================================================================
# AUDIT MODELS
# ============================================================================

class AuditLogModel(Base):
    """Audit log database model"""
    
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=True)
    action = Column(String)
    resource = Column(String)
    details = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

# ============================================================================
# ENUMS
# ============================================================================

class PredictionTypeEnum(str, PyEnum):
    """Prediction types"""
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"

class OrderTypeEnum(str, PyEnum):
    """Order types"""
    BUY = "BUY"
    SELL = "SELL"

class OrderStatusEnum(str, PyEnum):
    """Order statuses"""
    OPEN = "OPEN"
    EXECUTED = "EXECUTED"
    CANCELLED = "CANCELLED"
    PENDING = "PENDING"

class SentimentEnum(str, PyEnum):
    """Sentiment types"""
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"
    NEUTRAL = "NEUTRAL"

class ImpactLevelEnum(str, PyEnum):
    """Impact levels"""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
