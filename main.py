from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

app = FastAPI(title="StockAPI")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============= MODELS =============
class LoginRequest(BaseModel):
    username: str
    password: str
    tfa_code: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user_id: str

class Stock(BaseModel):
    symbol: str
    name: str
    price: float
    change_percent: float

class Portfolio(BaseModel):
    total_value: float
    cash: float
    invested: float
    gains: float
    gains_percent: float

class Holding(BaseModel):
    symbol: str
    quantity: int
    average_price: float
    current_price: float
    gains: float

class WatchlistItem(BaseModel):
    symbol: str
    price: float
    change_percent: float

# ============= HEALTH CHECK =============
@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "StockAPI is running"}

# ============= AUTHENTICATION =============
@app.post("/api/v1/account/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """Mock login endpoint for testing"""
    
    # Test credentials
    if request.username == "testuser" and request.password == "testpass123" and request.tfa_code == "123456":
        return LoginResponse(
            access_token="mock_token_abc123def456ghi789jkl",
            token_type="bearer",
            expires_in=86400,
            user_id="user_12345"
        )
    
    raise HTTPException(status_code=401, detail="Invalid credentials or TFA code")

# ============= STOCKS =============
@app.get("/api/v1/stocks/top-buys/{timeframe}", response_model=list[Stock])
async def get_top_buys(timeframe: str = "1d"):
    """Get top buying stocks"""
    return [
        Stock(symbol="AAPL", name="Apple Inc.", price=150.25, change_percent=2.5),
        Stock(symbol="GOOGL", name="Alphabet Inc.", price=140.50, change_percent=1.8),
        Stock(symbol="MSFT", name="Microsoft Corp.", price=380.75, change_percent=3.2),
        Stock(symbol="AMZN", name="Amazon.com Inc.", price=175.90, change_percent=-0.5),
        Stock(symbol="TSLA", name="Tesla Inc.", price=245.30, change_percent=5.1),
    ]

@app.get("/api/v1/stocks/predict/{symbol}/{timeframe}")
async def predict_stock(symbol: str, timeframe: str = "1d"):
    """Predict stock price"""
    return {
        "symbol": symbol,
        "predicted_price": 155.50,
        "direction": "UP",
        "confidence": 0.85
    }

# ============= PORTFOLIO =============
@app.get("/api/v1/account/portfolio", response_model=Portfolio)
async def get_portfolio():
    """Get portfolio summary"""
    return Portfolio(
        total_value=50000.00,
        cash=15000.00,
        invested=35000.00,
        gains=5000.00,
        gains_percent=10.0
    )

@app.get("/api/v1/account/holdings", response_model=list[Holding])
async def get_holdings():
    """Get portfolio holdings"""
    return [
        Holding(symbol="AAPL", quantity=10, average_price=140.00, current_price=150.25, gains=102.50),
        Holding(symbol="GOOGL", quantity=5, average_price=135.00, current_price=140.50, gains=27.50),
        Holding(symbol="MSFT", quantity=8, average_price=370.00, current_price=380.75, gains=86.00),
    ]

@app.get("/api/v1/account/orders")
async def get_orders():
    """Get order history"""
    return [
        {
            "order_id": "ORD001",
            "symbol": "AAPL",
            "order_type": "BUY",
            "quantity": 10,
            "price": 140.00,
            "status": "FILLED",
            "created_at": "2026-01-15T10:30:00Z"
        },
        {
            "order_id": "ORD002",
            "symbol": "GOOGL",
            "order_type": "BUY",
            "quantity": 5,
            "price": 135.00,
            "status": "FILLED",
            "created_at": "2026-01-16T14:45:00Z"
        }
    ]

# ============= WATCHLIST =============
@app.get("/api/v1/watchlist", response_model=list[WatchlistItem])
async def get_watchlist():
    """Get watchlist"""
    return [
        WatchlistItem(symbol="NVDA", price=875.50, change_percent=4.2),
        WatchlistItem(symbol="META", price=485.75, change_percent=2.1),
    ]

@app.post("/api/v1/watchlist/{symbol}")
async def add_to_watchlist(symbol: str):
    """Add stock to watchlist"""
    return {"message": f"{symbol} added to watchlist"}

@app.delete("/api/v1/watchlist/{symbol}")
async def remove_from_watchlist(symbol: str):
    """Remove stock from watchlist"""
    return {"message": f"{symbol} removed from watchlist"}

# ============= ROOT =============
@app.get("/api/v1/docs")
async def docs():
    """API documentation"""
    return {
        "endpoints": {
            "health": "GET /health",
            "login": "POST /api/v1/account/login",
            "portfolio": "GET /api/v1/account/portfolio",
            "holdings": "GET /api/v1/account/holdings",
            "orders": "GET /api/v1/account/orders",
            "top_buys": "GET /api/v1/stocks/top-buys/{timeframe}",
            "predict": "GET /api/v1/stocks/predict/{symbol}/{timeframe}",
            "watchlist": "GET /api/v1/watchlist",
            "add_watchlist": "POST /api/v1/watchlist/{symbol}",
            "remove_watchlist": "DELETE /api/v1/watchlist/{symbol}"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)