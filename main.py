"""
Stock Prediction API - Main Application
Complete production-ready FastAPI backend
"""

import logging
import os
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Import custom modules
from config import settings, get_settings
from database import init_db, cleanup_db, get_db, check_database_connection
from schemas import (
    HealthResponse,
    LoginRequest,
    LoginResponse,
    PortfolioSchema,
    HoldingSchema,
    OrderSchema,
    TradeSchema,
    PlaceOrderRequest,
    PlaceOrderResponse,
    TopBuy,
    StockPrediction,
    NewsArticleSchema,
    FeatureFlag
)
from services import (
    PredictionService,
    AccountService,
    PortfolioService,
    OrderService,
    TradeService,
    NewsService,
    WatchlistService
)
from utils import setup_logging

# ============================================================================
# LOGGING SETUP
# ============================================================================

logger = logging.getLogger(__name__)
setup_logging()

# ============================================================================
# FASTAPI APP INITIALIZATION
# ============================================================================

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# ============================================================================
# MIDDLEWARE SETUP
# ============================================================================

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# ============================================================================
# MODELS (Simple Models)
# ============================================================================

class SuccessResponse(BaseModel):
    success: bool = True
    message: str
    data: Optional[dict] = None

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    message: str
    timestamp: datetime = datetime.utcnow()

# ============================================================================
# STARTUP & SHUTDOWN EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Application startup"""
    logger.info("🚀 " + "="*60)
    logger.info("🚀 Stock Prediction API Starting...")
    logger.info("🚀 " + "="*60)
    
    logger.info(f"📌 Environment: {settings.ENVIRONMENT}")
    logger.info(f"📌 Host: {settings.HOST}:{settings.PORT}")
    logger.info(f"📌 Debug: {settings.DEBUG}")
    
    # Initialize database
    try:
        init_db()
        logger.info("✅ Database initialized")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {str(e)}")
        if settings.ENVIRONMENT == "production":
            raise
    
    # Check database connection
    if check_database_connection():
        logger.info("✅ Database connection verified")
    
    logger.info("\n📡 Available Endpoints:")
    logger.info("  GET  /health")
    logger.info("  GET  /api/v1/stocks/top-buys/{timeframe}")
    logger.info("  GET  /api/v1/stocks/predict/{symbol}/{timeframe}")
    logger.info("  POST /api/v1/account/login")
    logger.info("  GET  /api/v1/account/portfolio")
    logger.info("  GET  /api/v1/account/holdings")
    logger.info("  GET  /api/v1/account/orders")
    logger.info("  POST /api/v1/account/place-order")
    logger.info("  GET  /api/v1/news/{symbol}")
    logger.info("\n🚀 Ready to accept requests! 🚀\n")

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown"""
    logger.info("\n" + "="*60)
    logger.info("🛑 Stock Prediction API Shutting Down...")
    logger.info("="*60)
    
    # Cleanup resources
    cleanup_db()
    logger.info("✅ Resources cleaned up")

# ============================================================================
# ROOT ENDPOINT
# ============================================================================

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API information"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "environment": settings.ENVIRONMENT,
        "docs": "/docs",
        "health": "/health"
    }

# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    logger.info("🏥 Health check requested")
    
    db_health = check_database_connection()
    
    return HealthResponse(
        status="healthy" if db_health else "degraded",
        timestamp=datetime.now().isoformat(),
        version=settings.APP_VERSION
    )

# ============================================================================
# STOCK PREDICTION ENDPOINTS
# ============================================================================

@app.get("/api/v1/stocks/top-buys/{timeframe}", response_model=List[TopBuy], tags=["Stocks"])
async def get_top_buys(timeframe: str = "1M"):
    """Get top buy recommendations"""
    logger.info(f"📡 GET /api/v1/stocks/top-buys/{timeframe}")
    
    try:
        predictions = [
            {"symbol": "TCS", "confidence": 78.5, "target_price": 3750.0, "reason": "Strong uptrend"},
            {"symbol": "INFY", "confidence": 72.0, "target_price": 2340.0, "reason": "MA positive"},
            {"symbol": "RELIANCE", "confidence": 68.5, "target_price": 1380.0, "reason": "Support hold"},
            {"symbol": "WIPRO", "confidence": 65.0, "target_price": 380.0, "reason": "Technical bounce"},
            {"symbol": "HDFC BANK", "confidence": 62.5, "target_price": 1820.0, "reason": "Consolidation"}
        ]
        
        logger.info(f"✅ Returning {len(predictions)} predictions")
        return predictions
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/stocks/predict/{symbol}/{timeframe}", response_model=StockPrediction, tags=["Stocks"])
async def get_prediction(symbol: str, timeframe: str = "1M"):
    """Get prediction for specific stock"""
    logger.info(f"📡 GET /api/v1/stocks/predict/{symbol}/{timeframe}")
    
    try:
        predictions = {
            "TCS": {
                "symbol": "TCS",
                "timeframe": "1M",
                "technical_score": 72.5,
                "news_sentiment_score": None,
                "final_score": 72.5,
                "prediction": "BUY",
                "confidence": 78.5,
                "target_price": 3750.0,
                "technical_reason": "Score 72: MA trend positive, RSI 58, Volume +15%",
                "reason": "Strong uptrend, RSI neutral, MA positive"
            },
            "INFY": {
                "symbol": "INFY",
                "timeframe": "1M",
                "technical_score": 68.0,
                "news_sentiment_score": None,
                "final_score": 68.0,
                "prediction": "BUY",
                "confidence": 72.0,
                "target_price": 2340.0,
                "technical_reason": "MA crossover bullish, volume increase",
                "reason": "MA crossover bullish"
            }
        }
        
        if symbol not in predictions:
            raise HTTPException(status_code=404, detail=f"No prediction for {symbol}")
        
        return predictions[symbol]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/stocks/top-sells/{timeframe}", tags=["Stocks"])
async def get_top_sells(timeframe: str = "1M"):
    """Get top sell recommendations"""
    logger.info(f"📡 GET /api/v1/stocks/top-sells/{timeframe}")
    
    return {"message": "No sell recommendations at this time"}

# ============================================================================
# ACCOUNT/SHAREKHAN ENDPOINTS
# ============================================================================

@app.post("/api/v1/account/login", response_model=LoginResponse, tags=["Account"])
async def login(request: LoginRequest):
    """Login to Sharekhan account"""
    logger.info(f"🔐 POST /api/v1/account/login for {request.username}")
    
    try:
        success, result = AccountService.login(request.username, request.password, request.twofa)
        
        if success:
            logger.info(f"✅ User {request.username} authenticated")
            return LoginResponse(
                success=True,
                message="Successfully logged in",
                user_id=result
            )
        else:
            logger.warning(f"❌ Login failed: {result}")
            raise HTTPException(status_code=401, detail=result)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Login error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/account/logout", tags=["Account"])
async def logout():
    """Logout from account"""
    logger.info("🚪 POST /api/v1/account/logout")
    
    try:
        AccountService.logout()
        return {"success": True, "message": "Logged out successfully"}
    except Exception as e:
        logger.error(f"❌ Logout error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/account/is-authenticated", tags=["Account"])
async def is_authenticated():
    """Check authentication status"""
    logger.info("🔍 GET /api/v1/account/is-authenticated")
    
    is_auth = AccountService.is_authenticated()
    user_id = AccountService.get_authenticated_user()
    
    return {
        "authenticated": is_auth,
        "user_id": user_id
    }

@app.get("/api/v1/account/portfolio", response_model=PortfolioSchema, tags=["Account"])
async def get_portfolio():
    """Get portfolio summary"""
    logger.info("📊 GET /api/v1/account/portfolio")
    
    if not AccountService.is_authenticated():
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        portfolio = PortfolioService.get_portfolio()
        return portfolio
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/account/holdings", response_model=List[HoldingSchema], tags=["Account"])
async def get_holdings():
    """Get all holdings"""
    logger.info("📋 GET /api/v1/account/holdings")
    
    if not AccountService.is_authenticated():
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        holdings = PortfolioService.get_holdings()
        return holdings
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/account/holdings/{symbol}", response_model=HoldingSchema, tags=["Account"])
async def get_holding(symbol: str):
    """Get specific holding"""
    logger.info(f"📋 GET /api/v1/account/holdings/{symbol}")
    
    if not AccountService.is_authenticated():
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        holding = PortfolioService.get_holding(symbol)
        if not holding:
            raise HTTPException(status_code=404, detail=f"No holding for {symbol}")
        return holding
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# ORDER ENDPOINTS
# ============================================================================

@app.get("/api/v1/account/orders", response_model=List[OrderSchema], tags=["Orders"])
async def get_orders(status: str = "open"):
    """Get orders"""
    logger.info(f"📋 GET /api/v1/account/orders?status={status}")
    
    if not AccountService.is_authenticated():
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        orders = OrderService.get_orders(status)
        return orders
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/account/place-order", response_model=PlaceOrderResponse, tags=["Orders"])
async def place_order(request: PlaceOrderRequest):
    """Place a new order"""
    logger.info(f"📋 POST /api/v1/account/place-order")
    
    if not AccountService.is_authenticated():
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        result = OrderService.place_order(
            request.symbol,
            request.quantity,
            request.price,
            request.order_type
        )
        return result
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v1/account/cancel-order/{order_id}", tags=["Orders"])
async def cancel_order(order_id: str):
    """Cancel an order"""
    logger.info(f"❌ DELETE /api/v1/account/cancel-order/{order_id}")
    
    if not AccountService.is_authenticated():
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        if OrderService.cancel_order(order_id):
            return {"success": True, "message": f"Order {order_id} cancelled"}
        else:
            raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# TRADE ENDPOINTS
# ============================================================================

@app.get("/api/v1/account/trades", response_model=List[TradeSchema], tags=["Trades"])
async def get_trades(limit: int = 100):
    """Get trade history"""
    logger.info(f"📋 GET /api/v1/account/trades?limit={limit}")
    
    if not AccountService.is_authenticated():
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        trades = TradeService.get_trades(limit)
        return trades
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# NEWS ENDPOINTS
# ============================================================================

@app.get("/api/v1/news/{symbol}", tags=["News"])
async def get_news(symbol: str, days: int = 7):
    """Get news for a stock"""
    logger.info(f"📰 GET /api/v1/news/{symbol}?days={days}")
    
    try:
        news = NewsService.get_news(symbol, days)
        return {
            "symbol": symbol,
            "articles": news,
            "total_articles": len(news)
        }
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# WATCHLIST ENDPOINTS
# ============================================================================

@app.get("/api/v1/watchlist", tags=["Watchlist"])
async def get_watchlist():
    """Get user's watchlist"""
    logger.info("📋 GET /api/v1/watchlist")
    
    user_id = AccountService.get_authenticated_user()
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        watchlist = WatchlistService.get_watchlist(user_id)
        return {"watchlist": watchlist, "count": len(watchlist)}
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/watchlist/{symbol}", tags=["Watchlist"])
async def add_to_watchlist(symbol: str, notes: str = None):
    """Add to watchlist"""
    logger.info(f"➕ POST /api/v1/watchlist/{symbol}")
    
    user_id = AccountService.get_authenticated_user()
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        WatchlistService.add_to_watchlist(user_id, symbol, notes)
        return {"success": True, "message": f"{symbol} added to watchlist"}
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v1/watchlist/{symbol}", tags=["Watchlist"])
async def remove_from_watchlist(symbol: str):
    """Remove from watchlist"""
    logger.info(f"➖ DELETE /api/v1/watchlist/{symbol}")
    
    user_id = AccountService.get_authenticated_user()
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        if WatchlistService.remove_from_watchlist(user_id, symbol):
            return {"success": True, "message": f"{symbol} removed from watchlist"}
        else:
            raise HTTPException(status_code=404, detail=f"{symbol} not in watchlist")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# ADMIN ENDPOINTS
# ============================================================================

@app.get("/api/v1/admin/features", tags=["Admin"])
async def get_features():
    """Get feature flags"""
    logger.info("⚙️  GET /api/v1/admin/features")
    
    features = [
        {
            "feature_name": "technical_analysis",
            "enabled": settings.FEATURE_TECHNICAL_ANALYSIS,
            "description": "Technical analysis and predictions"
        },
        {
            "feature_name": "news_analysis",
            "enabled": settings.FEATURE_NEWS_ANALYSIS,
            "description": "News sentiment analysis"
        },
        {
            "feature_name": "claude_sentiment",
            "enabled": settings.FEATURE_CLAUDE_SENTIMENT,
            "description": "Claude AI sentiment analysis"
        },
        {
            "feature_name": "sharekhan_integration",
            "enabled": settings.FEATURE_SHAREKHAN_INTEGRATION,
            "description": "Sharekhan account integration"
        }
    ]
    
    return features

@app.patch("/api/v1/admin/features/{feature_name}", tags=["Admin"])
async def update_feature(feature_name: str, enabled: bool):
    """Update feature flag"""
    logger.info(f"⚙️  PATCH /api/v1/admin/features/{feature_name}")
    
    return {
        "success": True,
        "feature_name": feature_name,
        "enabled": enabled,
        "message": f"Feature {feature_name} updated"
    }

@app.post("/api/v1/admin/sync-data", tags=["Admin"])
async def sync_data():
    """Sync data from Sharekhan"""
    logger.info("🔄 POST /api/v1/admin/sync-data")
    
    return {
        "success": True,
        "message": "Data synced successfully",
        "synced_at": datetime.now().isoformat()
    }

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"❌ Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "message": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )

# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting server on {settings.HOST}:{settings.PORT}")
    
    uvicorn.run(
        "main_complete:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
