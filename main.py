"""
StockAPI - Stock Trading API with Sharekhan Integration
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import Sharekhan SDK (may not be available)
try:
    from SharekhanApi.sharekhanConnect import SharekhanConnect
    SHAREKHAN_AVAILABLE = True
    logger.info("✅ Sharekhan SDK imported successfully")
except ImportError:
    SHAREKHAN_AVAILABLE = False
    logger.warning("⚠️ Sharekhan SDK not available, using mock data")

# ============= FastAPI Setup =============
app = FastAPI(title="StockAPI", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============= Environment Variables =============
SHAREKHAN_API_KEY = os.getenv("SHAREKHAN_API_KEY", "")
SHAREKHAN_SECRET_KEY = os.getenv("SHAREKHAN_SECRET_KEY", "")
SHAREKHAN_REQUEST_TOKEN = os.getenv("SHAREKHAN_REQUEST_TOKEN", "")

logger.info(f"📋 Config Loaded:")
logger.info(f"  API Key: {'✅ Set' if SHAREKHAN_API_KEY else '❌ Not Set'}")
logger.info(f"  Secret Key: {'✅ Set' if SHAREKHAN_SECRET_KEY else '❌ Not Set'}")
logger.info(f"  Request Token: {'✅ Set' if SHAREKHAN_REQUEST_TOKEN else '❌ Not Set'}")

# ============= Pydantic Models =============
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
    data_source: str = "mock"  # Track if real or mock

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

# ============= Sharekhan Client =============
class SharekhanClient:
    """Client to interact with Sharekhan API"""
    
    def __init__(self, api_key: str, secret_key: str, request_token: str):
        self.api_key = api_key
        self.secret_key = secret_key
        self.request_token = request_token
        self.access_token = None
        self.session_data = None
    
    async def authenticate(self) -> bool:
        """Authenticate with Sharekhan and get access token"""
        try:
            if not SHAREKHAN_AVAILABLE:
                logger.warning("⚠️ Sharekhan SDK not available")
                return False
            
            logger.info("🔐 Authenticating with Sharekhan...")
            
            # Create connection
            login = SharekhanConnect(self.api_key)
            
            # Generate session using request token
            session_response = login.generate_session(
                self.request_token,
                self.secret_key
            )
            
            logger.info(f"📋 Session Response: {session_response}")
            
            if session_response and isinstance(session_response, dict):
                self.access_token = session_response.get('access_token')
                self.session_data = session_response
                
                if self.access_token:
                    logger.info("✅ Sharekhan authentication successful!")
                    return True
                else:
                    logger.error("❌ No access token in response")
                    return False
            else:
                logger.error(f"❌ Invalid session response: {session_response}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Sharekhan authentication error: {str(e)}")
            logger.exception(e)
            return False
    
    async def get_portfolio(self):
        """Get portfolio from Sharekhan"""
        try:
            if not self.access_token:
                logger.warning("⚠️ No access token available")
                return None
            
            logger.info("📊 Fetching portfolio from Sharekhan...")
            
            # TODO: Call actual Sharekhan API method
            # For now, return None to use mock data
            return None
            
        except Exception as e:
            logger.error(f"❌ Portfolio fetch error: {e}")
            return None
    
    async def get_holdings(self):
        """Get holdings from Sharekhan"""
        try:
            if not self.access_token:
                logger.warning("⚠️ No access token available")
                return None
            
            logger.info("📈 Fetching holdings from Sharekhan...")
            
            # TODO: Call actual Sharekhan API method
            # For now, return None to use mock data
            return None
            
        except Exception as e:
            logger.error(f"❌ Holdings fetch error: {e}")
            return None

# ============= Mock Data Functions =============
def get_mock_portfolio() -> Portfolio:
    """Return mock portfolio data"""
    return Portfolio(
        total_value=50000.00,
        cash=15000.00,
        invested=35000.00,
        gains=5000.00,
        gains_percent=10.0,
        data_source="mock"
    )

def get_mock_holdings() -> list:
    """Return mock holdings data"""
    return [
        Holding(
            symbol="AAPL",
            quantity=10,
            average_price=140.00,
            current_price=150.25,
            gains=102.50
        ),
        Holding(
            symbol="GOOGL",
            quantity=5,
            average_price=135.00,
            current_price=140.50,
            gains=27.50
        ),
        Holding(
            symbol="MSFT",
            quantity=8,
            average_price=370.00,
            current_price=380.75,
            gains=86.00
        ),
    ]

# ============= Health Check =============
@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "sharekhan_sdk_available": SHAREKHAN_AVAILABLE,
        "credentials_configured": bool(SHAREKHAN_API_KEY and SHAREKHAN_SECRET_KEY and SHAREKHAN_REQUEST_TOKEN)
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "StockAPI is running"}

# ============= Debug Endpoint =============
@app.get("/debug/variables")
async def debug_variables():
    """DEBUG ONLY - Show environment variables status"""
    logger.info("🔍 DEBUG: Checking variables...")
    
    return {
        "sharekhan_sdk": "available" if SHAREKHAN_AVAILABLE else "not_available",
        "api_key_set": bool(SHAREKHAN_API_KEY),
        "api_key_length": len(SHAREKHAN_API_KEY) if SHAREKHAN_API_KEY else 0,
        "secret_key_set": bool(SHAREKHAN_SECRET_KEY),
        "secret_key_length": len(SHAREKHAN_SECRET_KEY) if SHAREKHAN_SECRET_KEY else 0,
        "request_token_set": bool(SHAREKHAN_REQUEST_TOKEN),
        "request_token_length": len(SHAREKHAN_REQUEST_TOKEN) if SHAREKHAN_REQUEST_TOKEN else 0,
        "all_credentials_set": bool(SHAREKHAN_API_KEY and SHAREKHAN_SECRET_KEY and SHAREKHAN_REQUEST_TOKEN),
        "message": "All credentials set ✅" if all([SHAREKHAN_API_KEY, SHAREKHAN_SECRET_KEY, SHAREKHAN_REQUEST_TOKEN]) else "Missing credentials ❌"
    }

@app.get("/debug/test-sharekhan")
async def debug_test_sharekhan():
    """DEBUG ONLY - Test Sharekhan authentication"""
    
    if not SHAREKHAN_AVAILABLE:
        return {"error": "Sharekhan SDK not available"}
    
    if not all([SHAREKHAN_API_KEY, SHAREKHAN_SECRET_KEY, SHAREKHAN_REQUEST_TOKEN]):
        return {"error": "Missing credentials"}
    
    logger.info("🧪 Testing Sharekhan authentication...")
    
    client = SharekhanClient(
        SHAREKHAN_API_KEY,
        SHAREKHAN_SECRET_KEY,
        SHAREKHAN_REQUEST_TOKEN
    )
    
    success = await client.authenticate()
    
    return {
        "authentication_success": success,
        "access_token_obtained": bool(client.access_token),
        "session_data": client.session_data if success else None,
        "message": "✅ Authentication successful!" if success else "❌ Authentication failed"
    }

# ============= Authentication =============
@app.post("/api/v1/account/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """Login endpoint - test user or real Sharekhan user"""
    
    logger.info(f"🔐 Login attempt: {request.username}")
    
    # Test credentials
    if (request.username == "testuser" and 
        request.password == "testpass123" and 
        request.tfa_code == "123456"):
        
        logger.info("✅ Test user login successful")
        
        return LoginResponse(
            access_token="mock_token_abc123def456ghi789jkl",
            token_type="bearer",
            expires_in=86400,
            user_id="user_12345"
        )
    
    # For real users, validate against Sharekhan
    logger.warning(f"❌ Invalid credentials for: {request.username}")
    raise HTTPException(status_code=401, detail="Invalid credentials or TFA code")

# ============= Portfolio =============
@app.get("/api/v1/account/portfolio", response_model=Portfolio)
async def get_portfolio():
    """Get portfolio - from Sharekhan or mock data"""
    
    logger.info("📊 Portfolio request")
    
    # If no credentials, return mock
    if not all([SHAREKHAN_API_KEY, SHAREKHAN_SECRET_KEY, SHAREKHAN_REQUEST_TOKEN]):
        logger.warning("⚠️ No Sharekhan credentials, returning mock portfolio")
        return get_mock_portfolio()
    
    # Try to get from Sharekhan
    if SHAREKHAN_AVAILABLE:
        client = SharekhanClient(
            SHAREKHAN_API_KEY,
            SHAREKHAN_SECRET_KEY,
            SHAREKHAN_REQUEST_TOKEN
        )
        
        auth_success = await client.authenticate()
        
        if auth_success:
            portfolio = await client.get_portfolio()
            if portfolio:
                logger.info("✅ Got real portfolio from Sharekhan")
                return portfolio
    
    # Fallback to mock
    logger.warning("⚠️ Using mock portfolio as fallback")
    return get_mock_portfolio()

@app.get("/api/v1/account/holdings", response_model=list)
async def get_holdings():
    """Get holdings - from Sharekhan or mock data"""
    
    logger.info("📈 Holdings request")
    
    # If no credentials, return mock
    if not all([SHAREKHAN_API_KEY, SHAREKHAN_SECRET_KEY, SHAREKHAN_REQUEST_TOKEN]):
        logger.warning("⚠️ No Sharekhan credentials, returning mock holdings")
        return get_mock_holdings()
    
    # Try to get from Sharekhan
    if SHAREKHAN_AVAILABLE:
        client = SharekhanClient(
            SHAREKHAN_API_KEY,
            SHAREKHAN_SECRET_KEY,
            SHAREKHAN_REQUEST_TOKEN
        )
        
        auth_success = await client.authenticate()
        
        if auth_success:
            holdings = await client.get_holdings()
            if holdings:
                logger.info("✅ Got real holdings from Sharekhan")
                return holdings
    
    # Fallback to mock
    logger.warning("⚠️ Using mock holdings as fallback")
    return get_mock_holdings()

@app.get("/api/v1/account/orders")
async def get_orders():
    """Get order history"""
    return []

# ============= Stocks =============
@app.get("/api/v1/stocks/top-buys/{timeframe}")
async def get_top_buys(timeframe: str = "1d"):
    """Get top buys"""
    return [
        Stock(symbol="AAPL", name="Apple", price=150.25, change_percent=2.5),
        Stock(symbol="GOOGL", name="Google", price=140.50, change_percent=1.8),
        Stock(symbol="MSFT", name="Microsoft", price=380.75, change_percent=3.2),
        Stock(symbol="AMZN", name="Amazon", price=175.90, change_percent=-0.5),
        Stock(symbol="TSLA", name="Tesla", price=245.30, change_percent=5.1),
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

# ============= Watchlist =============
@app.get("/api/v1/watchlist")
async def get_watchlist():
    """Get watchlist"""
    return [
        WatchlistItem(symbol="NVDA", price=875.50, change_percent=4.2),
        WatchlistItem(symbol="META", price=485.75, change_percent=2.1),
        WatchlistItem(symbol="NFLX", price=425.30, change_percent=1.5),
    ]

@app.post("/api/v1/watchlist/{symbol}")
async def add_to_watchlist(symbol: str):
    """Add to watchlist"""
    logger.info(f"➕ Adding {symbol} to watchlist")
    return {"message": f"{symbol} added to watchlist"}

@app.delete("/api/v1/watchlist/{symbol}")
async def remove_from_watchlist(symbol: str):
    """Remove from watchlist"""
    logger.info(f"➖ Removing {symbol} from watchlist")
    return {"message": f"{symbol} removed from watchlist"}

# ============= Main =============
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)