"""
Utility functions and helpers
"""

import logging
import hashlib
import secrets
import re
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from functools import wraps
from fastapi import HTTPException, status
import jwt
from passlib.context import CryptContext
from config import settings

logger = logging.getLogger(__name__)

# ============================================================================
# PASSWORD SECURITY
# ============================================================================

# Password hashing context
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against hash"""
    return pwd_context.verify(plain_password, hashed_password)

def generate_random_string(length: int = 32) -> str:
    """Generate random string"""
    return secrets.token_urlsafe(length)

# ============================================================================
# JWT TOKENS
# ============================================================================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decode JWT access token"""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("Token has expired")
        return None
    except jwt.InvalidTokenError:
        logger.warning("Invalid token")
        return None

def verify_token(token: str) -> bool:
    """Verify token is valid"""
    return decode_access_token(token) is not None

# ============================================================================
# VALIDATION
# ============================================================================

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_username(username: str) -> bool:
    """Validate username format"""
    if len(username) < 3 or len(username) > 50:
        return False
    pattern = r'^[a-zA-Z0-9_-]+$'
    return re.match(pattern, username) is not None

def validate_stock_symbol(symbol: str) -> bool:
    """Validate stock symbol format"""
    if len(symbol) < 1 or len(symbol) > 10:
        return False
    return symbol.isupper()

def validate_2fa_code(code: str) -> bool:
    """Validate 2FA code format"""
    if len(code) != 6:
        return False
    return code.isdigit()

# ============================================================================
# DATA FORMATTING
# ============================================================================

def format_currency(value: float, currency: str = "₹") -> str:
    """Format value as currency"""
    return f"{currency}{value:,.2f}"

def format_percentage(value: float, decimals: int = 2) -> str:
    """Format value as percentage"""
    return f"{value:.{decimals}f}%"

def format_datetime(dt: datetime, format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime"""
    return dt.strftime(format)

def get_timeframe_days(timeframe: str) -> int:
    """Get number of days for timeframe"""
    timeframes = {
        "1W": 7,
        "1M": 30,
        "3M": 90,
        "1Y": 365
    }
    return timeframes.get(timeframe, 30)

def get_timeframe_hours(timeframe: str) -> int:
    """Get number of hours for timeframe"""
    return get_timeframe_days(timeframe) * 24

# ============================================================================
# CACHING
# ============================================================================

class CacheKey:
    """Cache key builders"""
    
    @staticmethod
    def prediction(symbol: str, timeframe: str) -> str:
        return f"prediction:{symbol}:{timeframe}"
    
    @staticmethod
    def top_buys(timeframe: str) -> str:
        return f"top_buys:{timeframe}"
    
    @staticmethod
    def top_sells(timeframe: str) -> str:
        return f"top_sells:{timeframe}"
    
    @staticmethod
    def news(symbol: str) -> str:
        return f"news:{symbol}"
    
    @staticmethod
    def portfolio(user_id: str) -> str:
        return f"portfolio:{user_id}"
    
    @staticmethod
    def holdings(user_id: str) -> str:
        return f"holdings:{user_id}"

# ============================================================================
# ERROR HANDLING
# ============================================================================

def raise_http_exception(
    status_code: int,
    detail: str,
    headers: Optional[Dict[str, str]] = None
):
    """Raise HTTP exception"""
    raise HTTPException(
        status_code=status_code,
        detail=detail,
        headers=headers
    )

def raise_unauthorized(detail: str = "Not authenticated"):
    """Raise 401 Unauthorized"""
    raise_http_exception(
        status.HTTP_401_UNAUTHORIZED,
        detail,
        {"WWW-Authenticate": "Bearer"}
    )

def raise_forbidden(detail: str = "Access forbidden"):
    """Raise 403 Forbidden"""
    raise_http_exception(status.HTTP_403_FORBIDDEN, detail)

def raise_not_found(detail: str = "Not found"):
    """Raise 404 Not Found"""
    raise_http_exception(status.HTTP_404_NOT_FOUND, detail)

def raise_bad_request(detail: str = "Bad request"):
    """Raise 400 Bad Request"""
    raise_http_exception(status.HTTP_400_BAD_REQUEST, detail)

def raise_conflict(detail: str = "Conflict"):
    """Raise 409 Conflict"""
    raise_http_exception(status.HTTP_409_CONFLICT, detail)

def raise_server_error(detail: str = "Internal server error"):
    """Raise 500 Internal Server Error"""
    raise_http_exception(status.HTTP_500_INTERNAL_SERVER_ERROR, detail)

# ============================================================================
# DECORATORS
# ============================================================================

def timing_decorator(func):
    """Decorator to log function execution time"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = datetime.utcnow()
        try:
            result = await func(*args, **kwargs)
            elapsed = (datetime.utcnow() - start_time).total_seconds()
            logger.info(f"✅ {func.__name__} completed in {elapsed:.2f}s")
            return result
        except Exception as e:
            elapsed = (datetime.utcnow() - start_time).total_seconds()
            logger.error(f"❌ {func.__name__} failed after {elapsed:.2f}s: {str(e)}")
            raise
    
    return wrapper

def log_decorator(func):
    """Decorator to log function calls"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        logger.debug(f"📍 Calling {func.__name__}")
        try:
            result = await func(*args, **kwargs)
            logger.debug(f"✅ {func.__name__} succeeded")
            return result
        except Exception as e:
            logger.error(f"❌ {func.__name__} failed: {str(e)}")
            raise
    
    return wrapper

# ============================================================================
# LOGGING
# ============================================================================

def setup_logging():
    """Setup application logging"""
    
    # Create logger
    logger = logging.getLogger("stock_prediction_api")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Create formatter
    formatter = logging.Formatter(settings.LOG_FORMAT)
    
    # Create and add handlers
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

# ============================================================================
# STATISTICS
# ============================================================================

def calculate_profit_loss(buy_price: float, current_price: float, quantity: int) -> tuple:
    """Calculate profit/loss"""
    profit = (current_price - buy_price) * quantity
    profit_percent = ((current_price - buy_price) / buy_price) * 100
    return profit, profit_percent

def calculate_portfolio_stats(holdings: list) -> dict:
    """Calculate portfolio statistics"""
    total_value = sum(h["value"] for h in holdings)
    total_profit = sum(h["profit"] for h in holdings)
    
    if total_value > 0:
        profit_percent = (total_profit / (total_value - total_profit)) * 100
    else:
        profit_percent = 0
    
    return {
        "total_value": total_value,
        "total_profit": total_profit,
        "profit_percent": profit_percent,
        "holdings_count": len(holdings)
    }

# ============================================================================
# API UTILITIES
# ============================================================================

def get_client_ip(request) -> str:
    """Get client IP from request"""
    if request.headers.get("x-forwarded-for"):
        return request.headers.get("x-forwarded-for").split(",")[0]
    return request.client.host if request.client else "unknown"

def get_user_agent(request) -> str:
    """Get user agent from request"""
    return request.headers.get("user-agent", "unknown")
