"""
Pydantic schemas for request/response validation
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, validator

# ============================================================================
# PREDICTION SCHEMAS
# ============================================================================

class StockPredictionBase(BaseModel):
    symbol: str
    timeframe: str = "1M"
    technical_score: float
    news_sentiment_score: Optional[float] = None
    final_score: float
    prediction: str  # BUY, SELL, HOLD
    confidence: float
    target_price: float
    technical_reason: str
    reason: Optional[str] = None
    news_reason: Optional[str] = None
    articles_analyzed: int = 0

class StockPredictionCreate(StockPredictionBase):
    pass

class StockPrediction(StockPredictionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class TopBuy(BaseModel):
    symbol: str
    confidence: float
    target_price: float
    reason: str

# ============================================================================
# ACCOUNT SCHEMAS
# ============================================================================

class LoginRequest(BaseModel):
    username: str
    password: str
    twofa: str = Field(..., min_length=6, max_length=6)

class LoginResponse(BaseModel):
    success: bool
    message: str
    user_id: Optional[str] = None
    access_token: Optional[str] = None

class PortfolioSchema(BaseModel):
    account_balance: float = Field(default=0, ge=0)
    portfolio_value: float = Field(default=0, ge=0)
    total_profit: float
    profit_percent: float
    cash_available: float = Field(default=0, ge=0)
    margin_available: float = Field(default=0, ge=0)
    holdings_count: int = Field(default=0, ge=0)

class HoldingSchema(BaseModel):
    symbol: str
    quantity: int = Field(..., gt=0)
    current_price: float = Field(..., gt=0)
    buy_price: float = Field(..., gt=0)
    profit: float
    profit_percent: float
    value: float = Field(..., gt=0)

class OrderSchema(BaseModel):
    order_id: str
    symbol: str
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)
    order_type: str  # BUY, SELL
    status: str
    created_at: datetime
    executed_quantity: int = Field(default=0, ge=0)

class TradeSchema(BaseModel):
    trade_id: str
    symbol: str
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)
    trade_type: str  # BUY, SELL
    timestamp: datetime
    exchange: str

class PlaceOrderRequest(BaseModel):
    symbol: str
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)
    order_type: str = "BUY"
    product: str = "MIS"

class PlaceOrderResponse(BaseModel):
    success: bool
    order_id: str
    message: str

class UserAccountCreate(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserAccount(BaseModel):
    id: int
    user_id: str
    username: str
    email: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============================================================================
# NEWS SCHEMAS
# ============================================================================

class NewsArticleSchema(BaseModel):
    headline: str
    source: str
    sentiment: str  # POSITIVE, NEGATIVE, NEUTRAL
    sentiment_score: float = Field(..., ge=0, le=1)
    impact_level: str  # HIGH, MEDIUM, LOW
    url: Optional[str] = None
    published_at: datetime

class NewsResponse(BaseModel):
    symbol: str
    articles: List[NewsArticleSchema]
    total_articles: int
    average_sentiment: float

# ============================================================================
# WATCHLIST SCHEMAS
# ============================================================================

class WatchlistItemSchema(BaseModel):
    symbol: str
    notes: Optional[str] = None

class WatchlistItem(WatchlistItemSchema):
    id: int
    user_id: str
    added_at: datetime
    
    class Config:
        from_attributes = True

# ============================================================================
# ADMIN SCHEMAS
# ============================================================================

class FeatureFlag(BaseModel):
    feature_name: str
    enabled: bool
    description: str

class FeatureUpdate(BaseModel):
    enabled: bool

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    environment: str
    services: dict

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class SuccessResponse(BaseModel):
    success: bool = True
    message: str
    data: Optional[dict] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# ============================================================================
# PAGINATION SCHEMAS
# ============================================================================

class PaginationParams(BaseModel):
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=10, ge=1, le=100)

class PaginatedResponse(BaseModel):
    data: list
    total: int
    skip: int
    limit: int
    has_more: bool

# ============================================================================
# VALIDATION
# ============================================================================

class StockSymbolValidator(BaseModel):
    symbol: str
    
    @validator('symbol')
    def symbol_must_be_uppercase(cls, v):
        if not v.isupper():
            raise ValueError('Symbol must be uppercase')
        if len(v) < 1 or len(v) > 10:
            raise ValueError('Symbol must be 1-10 characters')
        return v

class TimeframeValidator(BaseModel):
    timeframe: str
    
    @validator('timeframe')
    def timeframe_must_be_valid(cls, v):
        valid_timeframes = ['1W', '1M', '3M', '1Y']
        if v not in valid_timeframes:
            raise ValueError(f'Timeframe must be one of {valid_timeframes}')
        return v

class QuantityValidator(BaseModel):
    quantity: int
    
    @validator('quantity')
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be positive')
        return v

class PriceValidator(BaseModel):
    price: float
    
    @validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return v
