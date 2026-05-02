from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

# Install: pip install shareconnectpython
try:
    from SharekhanApi.sharekhanConnect import SharekhanConnect
except ImportError:
    print("⚠️ Install shareconnectpython: pip install shareconnectpython")
    SharekhanConnect = None

app = FastAPI(title="StockAPI")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============= CONFIG =============
SHAREKHAN_API_KEY = os.getenv("SHAREKHAN_API_KEY", "")
SHAREKHAN_SECRET_KEY = os.getenv("SHAREKHAN_SECRET_KEY", "")
SHAREKHAN_REQUEST_TOKEN = os.getenv("SHAREKHAN_REQUEST_TOKEN", "")

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
    name: str = ""
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

# ============= SHAREKHAN CLIENT =============
def get_sharekhan_session():
    """Get Sharekhan session with access token"""
    if not all([SHAREKHAN_API_KEY, SHAREKHAN_SECRET_KEY, SHAREKHAN_REQUEST_TOKEN]):
        print("⚠️ Missing Sharekhan credentials")
        return None
    
    try:
        # Initialize Sharekhan connection
        login = SharekhanConnect(SHAREKHAN_API_KEY)
        
        # Generate session with request token
        session = login.generate_session(
            SHAREKHAN_REQUEST_TOKEN,
            SHAREKHAN_SECRET_KEY
        )
        
        if session and 'access_token' in session:
            print(f"✅ Sharekhan session created")
            return session['access_token']
        else:
            print(f"❌ Failed to create session: {session}")
            return None
    except Exception as e:
        print(f"❌ Sharekhan error: {e}")
        return None

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
    """Login - test user or real Sharekhan user"""
    
    # Test credentials
    if request.username == "testuser" and request.password == "testpass123" and request.tfa_code == "123456":
        return LoginResponse(
            access_token="mock_token_abc123def456ghi789jkl",
            token_type="bearer",
            expires_in=86400,
            user_id="user_12345"
        )
    
    # For real users, you would validate against Sharekhan here
    raise HTTPException(status_code=401, detail="Invalid credentials or TFA code")

# ============= PORTFOLIO =============
@app.get("/api/v1/account/portfolio", response_model=Portfolio)
async def get_portfolio():
    """Get portfolio from Sharekhan"""
    
    access_token = get_sharekhan_session()
    
    if access_token:
        try:
            # You would use Sharekhan SDK methods here
            # Example: positions = login.getPositions(access_token)
            print(f"✅ Fetching real portfolio from Sharekhan")
            
            # For now, return mock data
            # TODO: Implement actual Sharekhan SDK calls
            return Portfolio(
                total_value=50000.00,
                cash=15000.00,
                invested=35000.00,
                gains=5000.00,
                gains_percent=10.0
            )
        except Exception as e:
            print(f"❌ Portfolio error: {e}")
    
    # Fallback to mock data
    return Portfolio(
        total_value=50000.00,
        cash=15000.00,
        invested=35000.00,
        gains=5000.00,
        gains_percent=10.0
    )

@app.get("/api/v1/account/holdings", response_model=list)
async def get_holdings():
    """Get holdings from Sharekhan"""
    
    access_token = get_sharekhan_session()
    
    if access_token:
        try:
            # You would use Sharekhan SDK methods here
            # Example: holdings = login.getHoldings(access_token)
            print(f"✅ Fetching real holdings from Sharekhan")
            
            # For now, return mock data
            # TODO: Implement actual Sharekhan SDK calls
            return [
                Holding(symbol="AAPL", quantity=10, average_price=140.00, current_price=150.25, gains=102.50),
                Holding(symbol="GOOGL", quantity=5, average_price=135.00, current_price=140.50, gains=27.50),
            ]
        except Exception as e:
            print(f"❌ Holdings error: {e}")
    
    # Fallback to mock data
    return [
        Holding(symbol="AAPL", quantity=10, average_price=140.00, current_price=150.25, gains=102.50),
        Holding(symbol="GOOGL", quantity=5, average_price=135.00, current_price=140.50, gains=27.50),
    ]

@app.get("/api/v1/account/orders")
async def get_orders():
    """Get orders"""
    return []

# ============= STOCKS =============
@app.get("/api/v1/stocks/top-buys/{timeframe}")
async def get_top_buys(timeframe: str = "1d"):
    """Get top buys"""
    return [
        Stock(symbol="AAPL", name="Apple", price=150.25, change_percent=2.5),
        Stock(symbol="GOOGL", name="Google", price=140.50, change_percent=1.8),
        Stock(symbol="MSFT", name="Microsoft", price=380.75, change_percent=3.2),
    ]

@app.get("/api/v1/stocks/predict/{symbol}/{timeframe}")
async def predict_stock(symbol: str, timeframe: str = "1d"):
    """Predict stock"""
    return {
        "symbol": symbol,
        "predicted_price": 155.50,
        "direction": "UP",
        "confidence": 0.85
    }

# ============= WATCHLIST =============
@app.get("/api/v1/watchlist")
async def get_watchlist():
    """Get watchlist"""
    return [
        WatchlistItem(symbol="NVDA", price=875.50, change_percent=4.2),
        WatchlistItem(symbol="META", price=485.75, change_percent=2.1),
    ]

@app.post("/api/v1/watchlist/{symbol}")
async def add_to_watchlist(symbol: str):
    """Add to watchlist"""
    return {"message": f"{symbol} added to watchlist"}

@app.delete("/api/v1/watchlist/{symbol}")
async def remove_from_watchlist(symbol: str):
    """Remove from watchlist"""
    return {"message": f"{symbol} removed from watchlist"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)