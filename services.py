"""
Business logic services for Stock Prediction API
"""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import requests
from config import settings
from models import (
    StockPredictionModel,
    UserAccountModel,
    PortfolioModel,
    HoldingModel,
    OrderModel,
    TradeModel,
    NewsArticleModel,
    WatchlistItemModel
)
from schemas import (
    StockPrediction,
    PortfolioSchema,
    HoldingSchema,
    OrderSchema,
    TradeSchema,
    NewsArticleSchema
)
from utils import (
    hash_password,
    verify_password,
    calculate_profit_loss,
    validate_stock_symbol,
    validate_2fa_code
)

logger = logging.getLogger(__name__)

# ============================================================================
# PREDICTION SERVICE
# ============================================================================

class PredictionService:
    """Service for stock predictions"""
    
    @staticmethod
    def get_predictions(db: Session, timeframe: str = "1M") -> List[Dict[str, Any]]:
        """Get all predictions for timeframe"""
        logger.info(f"📡 Fetching predictions for {timeframe}")
        
        predictions = db.query(StockPredictionModel).filter(
            StockPredictionModel.timeframe == timeframe
        ).all()
        
        return [p.__dict__ for p in predictions]
    
    @staticmethod
    def get_prediction(db: Session, symbol: str, timeframe: str = "1M") -> Optional[StockPrediction]:
        """Get prediction for specific stock"""
        logger.info(f"📡 Fetching prediction for {symbol}")
        
        if not validate_stock_symbol(symbol):
            logger.warning(f"Invalid symbol: {symbol}")
            return None
        
        prediction = db.query(StockPredictionModel).filter(
            StockPredictionModel.symbol == symbol,
            StockPredictionModel.timeframe == timeframe
        ).first()
        
        return prediction
    
    @staticmethod
    def get_top_buys(db: Session, timeframe: str = "1M", limit: int = 5) -> List[Dict[str, Any]]:
        """Get top buy recommendations"""
        logger.info(f"📡 Fetching top buys for {timeframe}")
        
        predictions = db.query(StockPredictionModel).filter(
            StockPredictionModel.timeframe == timeframe,
            StockPredictionModel.prediction == "BUY"
        ).order_by(StockPredictionModel.confidence.desc()).limit(limit).all()
        
        return [
            {
                "symbol": p.symbol,
                "confidence": p.confidence,
                "target_price": p.target_price,
                "reason": p.reason or p.technical_reason
            }
            for p in predictions
        ]
    
    @staticmethod
    def create_prediction(db: Session, prediction_data: Dict[str, Any]) -> StockPredictionModel:
        """Create new prediction"""
        logger.info(f"✍️  Creating prediction for {prediction_data.get('symbol')}")
        
        db_prediction = StockPredictionModel(**prediction_data)
        db.add(db_prediction)
        db.commit()
        db.refresh(db_prediction)
        
        return db_prediction

# ============================================================================
# ACCOUNT SERVICE
# ============================================================================

class AccountService:
    """Service for user accounts and authentication"""
    
    # Mock data for demo
    mock_authenticated_users = {}
    
    @staticmethod
    def login(username: str, password: str, twofa: str) -> tuple:
        """Authenticate user"""
        logger.info(f"🔐 Login attempt for {username}")
        
        # Validate inputs
        if not username or not password or not twofa:
            logger.warning("Missing credentials")
            return False, "Missing credentials"
        
        if not validate_2fa_code(twofa):
            logger.warning(f"Invalid 2FA code: {twofa}")
            return False, "Invalid 2FA code"
        
        # Mock authentication (replace with real Sharekhan API)
        user_id = f"user_{username}"
        AccountService.mock_authenticated_users[user_id] = {
            "username": username,
            "authenticated": True,
            "timestamp": datetime.utcnow()
        }
        
        logger.info(f"✅ User {username} authenticated")
        return True, user_id
    
    @staticmethod
    def logout():
        """Logout user"""
        logger.info("🚪 User logout")
        AccountService.mock_authenticated_users.clear()
        return True
    
    @staticmethod
    def is_authenticated() -> bool:
        """Check if user is authenticated"""
        is_auth = len(AccountService.mock_authenticated_users) > 0
        logger.info(f"Authentication check: {is_auth}")
        return is_auth
    
    @staticmethod
    def get_authenticated_user() -> Optional[str]:
        """Get authenticated user ID"""
        if AccountService.mock_authenticated_users:
            return list(AccountService.mock_authenticated_users.keys())[0]
        return None

# ============================================================================
# PORTFOLIO SERVICE
# ============================================================================

class PortfolioService:
    """Service for portfolio management"""
    
    # Mock portfolio data
    mock_portfolio = {
        "account_balance": 500000.0,
        "portfolio_value": 750000.0,
        "total_profit": 150000.0,
        "profit_percent": 25.0,
        "cash_available": 200000.0,
        "margin_available": 100000.0,
        "holdings_count": 3
    }
    
    mock_holdings = [
        {
            "symbol": "TCS",
            "quantity": 10,
            "current_price": 3750.0,
            "buy_price": 3200.0,
            "profit": 5500.0,
            "profit_percent": 17.1,
            "value": 37500.0
        },
        {
            "symbol": "INFY",
            "quantity": 15,
            "current_price": 2340.0,
            "buy_price": 2000.0,
            "profit": 5100.0,
            "profit_percent": 17.0,
            "value": 35100.0
        },
        {
            "symbol": "RELIANCE",
            "quantity": 20,
            "current_price": 1380.0,
            "buy_price": 1310.0,
            "profit": 1400.0,
            "profit_percent": 5.3,
            "value": 27600.0
        }
    ]
    
    @staticmethod
    def get_portfolio() -> Dict[str, Any]:
        """Get portfolio summary"""
        logger.info("📊 Fetching portfolio")
        return PortfolioService.mock_portfolio
    
    @staticmethod
    def get_holdings() -> List[Dict[str, Any]]:
        """Get all holdings"""
        logger.info("📋 Fetching holdings")
        return PortfolioService.mock_holdings
    
    @staticmethod
    def get_holding(symbol: str) -> Optional[Dict[str, Any]]:
        """Get specific holding"""
        logger.info(f"📋 Fetching holding for {symbol}")
        
        for holding in PortfolioService.mock_holdings:
            if holding["symbol"] == symbol:
                return holding
        
        return None

# ============================================================================
# ORDER SERVICE
# ============================================================================

class OrderService:
    """Service for order management"""
    
    mock_orders = [
        {
            "order_id": "ORD001",
            "symbol": "WIPRO",
            "quantity": 50,
            "price": 380.0,
            "order_type": "BUY",
            "status": "OPEN",
            "created_at": "2026-04-30 10:30:00",
            "executed_quantity": 0
        },
        {
            "order_id": "ORD002",
            "symbol": "HDFC BANK",
            "quantity": 5,
            "price": 1820.0,
            "order_type": "BUY",
            "status": "OPEN",
            "created_at": "2026-04-30 11:00:00",
            "executed_quantity": 0
        }
    ]
    
    @staticmethod
    def get_orders(status: str = "open") -> List[Dict[str, Any]]:
        """Get orders by status"""
        logger.info(f"📋 Fetching orders with status: {status}")
        
        if status == "all":
            return OrderService.mock_orders
        
        return [o for o in OrderService.mock_orders if o["status"].lower() == status.lower()]
    
    @staticmethod
    def place_order(symbol: str, quantity: int, price: float, order_type: str = "BUY") -> Dict[str, Any]:
        """Place new order"""
        logger.info(f"📋 Placing order: {symbol} {quantity} @ ₹{price}")
        
        order_id = f"ORD{len(OrderService.mock_orders) + 1:03d}"
        
        new_order = {
            "order_id": order_id,
            "symbol": symbol,
            "quantity": quantity,
            "price": price,
            "order_type": order_type,
            "status": "OPEN",
            "created_at": datetime.now().isoformat(),
            "executed_quantity": 0
        }
        
        OrderService.mock_orders.append(new_order)
        logger.info(f"✅ Order placed: {order_id}")
        
        return {
            "success": True,
            "order_id": order_id,
            "message": "Order placed successfully"
        }
    
    @staticmethod
    def cancel_order(order_id: str) -> bool:
        """Cancel order"""
        logger.info(f"❌ Cancelling order: {order_id}")
        
        for order in OrderService.mock_orders:
            if order["order_id"] == order_id:
                order["status"] = "CANCELLED"
                logger.info(f"✅ Order {order_id} cancelled")
                return True
        
        return False

# ============================================================================
# TRADE SERVICE
# ============================================================================

class TradeService:
    """Service for trade history"""
    
    mock_trades = [
        {
            "trade_id": "TRD001",
            "symbol": "TCS",
            "quantity": 10,
            "price": 3200.0,
            "trade_type": "BUY",
            "timestamp": "2026-04-15 09:30:00",
            "exchange": "NSE"
        },
        {
            "trade_id": "TRD002",
            "symbol": "INFY",
            "quantity": 15,
            "price": 2000.0,
            "trade_type": "BUY",
            "timestamp": "2026-04-20 10:15:00",
            "exchange": "NSE"
        },
        {
            "trade_id": "TRD003",
            "symbol": "RELIANCE",
            "quantity": 20,
            "price": 1310.0,
            "trade_type": "BUY",
            "timestamp": "2026-04-25 14:45:00",
            "exchange": "NSE"
        }
    ]
    
    @staticmethod
    def get_trades(limit: int = 100) -> List[Dict[str, Any]]:
        """Get trade history"""
        logger.info(f"📋 Fetching {limit} trades")
        return TradeService.mock_trades[:limit]

# ============================================================================
# NEWS SERVICE
# ============================================================================

class NewsService:
    """Service for news aggregation"""
    
    @staticmethod
    def get_news(symbol: str, days: int = 7) -> List[Dict[str, Any]]:
        """Get news for stock"""
        logger.info(f"📰 Fetching news for {symbol}")
        
        mock_news = [
            {
                "headline": f"Positive analysis for {symbol}",
                "source": "Economic Times",
                "sentiment": "POSITIVE",
                "sentiment_score": 0.85,
                "impact_level": "HIGH",
                "published_at": "2026-04-30T10:00:00Z"
            },
            {
                "headline": f"{symbol} shows strong fundamentals",
                "source": "Moneycontrol",
                "sentiment": "POSITIVE",
                "sentiment_score": 0.80,
                "impact_level": "MEDIUM",
                "published_at": "2026-04-29T15:30:00Z"
            }
        ]
        
        return mock_news

# ============================================================================
# WATCHLIST SERVICE
# ============================================================================

class WatchlistService:
    """Service for watchlist management"""
    
    mock_watchlist = {
        "user1": [
            {"symbol": "TCS", "notes": "Strong performer"},
            {"symbol": "INFY", "notes": "Tech leader"}
        ]
    }
    
    @staticmethod
    def get_watchlist(user_id: str) -> List[Dict[str, Any]]:
        """Get user's watchlist"""
        logger.info(f"📋 Fetching watchlist for {user_id}")
        return WatchlistService.mock_watchlist.get(user_id, [])
    
    @staticmethod
    def add_to_watchlist(user_id: str, symbol: str, notes: str = None) -> bool:
        """Add stock to watchlist"""
        logger.info(f"➕ Adding {symbol} to watchlist for {user_id}")
        
        if user_id not in WatchlistService.mock_watchlist:
            WatchlistService.mock_watchlist[user_id] = []
        
        WatchlistService.mock_watchlist[user_id].append({
            "symbol": symbol,
            "notes": notes
        })
        
        return True
    
    @staticmethod
    def remove_from_watchlist(user_id: str, symbol: str) -> bool:
        """Remove stock from watchlist"""
        logger.info(f"➖ Removing {symbol} from watchlist for {user_id}")
        
        if user_id in WatchlistService.mock_watchlist:
            WatchlistService.mock_watchlist[user_id] = [
                w for w in WatchlistService.mock_watchlist[user_id]
                if w["symbol"] != symbol
            ]
            return True
        
        return False
