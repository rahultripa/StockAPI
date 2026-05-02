from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
from functools import lru_cache

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
class Settings:
    SHAREKHAN_CLIENT_ID: str = os.getenv("SHAREKHAN_CLIENT_ID", "")
    SHAREKHAN_API_KEY: str = os.getenv("SHAREKHAN_API_KEY", "")
    SHAREKHAN_SECRET_KEY: str = os.getenv("SHAREKHAN_SECRET_KEY", "")
    SHAREKHAN_BASE_URL: str = "https://api.sharekhan.com/v1"

@lru_cache()
def get_settings():
    return Settings()

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
class SharekhanClient:
    def __init__(self, client_id: str, api_key: str, secret_key: str):
        self.client_id = client_id
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = "https://api.sharekhan.com/v1"
        self.access_token = None

    async def authenticate(self):
        """Authenticate with Sharekhan API"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/oauth/authorize",
                    json={
                        "client_id": self.client_id,
                        "api_key": self.api_key,
                        "secret_key": self.secret_key
                    },
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self.access_token = data.get("access_token")
                    return True
                else:
                    print(f"❌ Sharekhan auth failed: {response.status_code}")
                    return False
        except Exception as e:
            print(f"❌ Sharekhan auth error: {e}")
            return False

    async def get_portfolio(self):
        """Get portfolio from Sharekhan"""
        if not self.access_token:
            await self.authenticate()
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/user/portfolio",
                    headers={"Authorization": f"Bearer {self.access_token}"},
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return Portfolio(
                        total_value=float(data.get("total_value", 0)),
                        cash=float(data.get("cash", 0)),
                        invested=float(data.get("invested", 0)),
                        gains=float(data.get("gains", 0)),
                        gains_percent=float(data.get("gains_percent", 0))
                    )
        except Exception as e:
            print(f"❌ Portfolio fetch error: {e}")
        
        return None

    async def get_holdings(self):
        """Get holdings from Sharekhan"""
        if not self.access_token:
            await self.authenticate()
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/user/holdings",
                    headers={"Authorization": f"Bearer {self.access_token}"},
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    holdings = []
                    for item in data.get("holdings", []):
                        holdings.append(Holding(
                            symbol=item.get("symbol", ""),
                            quantity=int(item.get("quantity", 0)),
                            average_price=float(item.get("average_price", 0)),
                            current_price=float(item.get("current_price", 0)),
                            gains=float(item.get("gains", 0))
                        ))
                    return holdings
        except Exception as e:
            print(f"❌ Holdings fetch error: {e}")
        
        return []

    async def get_watchlist(self):
        """Get watchlist from Sharekhan"""
        if not self.access_token:
            await self.authenticate()
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/user/watchlist",
                    headers={"Authorization": f"Bearer {self.access_token}"},
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    watchlist = []
                    for item in data.get("watchlist", []):
                        watchlist.append(WatchlistItem(
                            symbol=item.get("symbol", ""),
                            price=float(item.get("price", 0)),
                            change_percent=float(item.get("change_percent", 0))
                        ))
                    return watchlist
        except Exception as e:
            print(f"❌ Watchlist fetch error: {e}")
        
        return []

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
    """Login with Sharekhan credentials"""
    
    # For testing with testuser
    if request.username == "testuser" and request.password == "testpass123" and request.tfa_code == "123456":
        return LoginResponse(
            access_token="mock_token_abc123def456ghi789jkl",
            token_type="bearer",
            expires_in=86400,
            user_id="user_12345"
        )
    
    # For real Sharekhan users - you would validate here
    raise HTTPException(status_code=401, detail="Invalid credentials or TFA code")

# ============= PORTFOLIO =============
@app.get("/api/v1/account/portfolio", response_model=Portfolio)
async def get_portfolio(settings: Settings = Depends(get_settings)):
    """Get portfolio from Sharekhan"""
    
    if not settings.SHAREKHAN_CLIENT_ID:
        # Return mock data if no credentials
        return Portfolio(
            total_value=50000.00,
            cash=15000.00,
            invested=35000.00,
            gains=5000.00,
            gains_percent=10.0
        )
    
    client = SharekhanClient(
        settings.SHAREKHAN_CLIENT_ID,
        settings.SHAREKHAN_API_KEY,
        settings.SHAREKHAN_SECRET_KEY
    )
    
    portfolio = await client.get_portfolio()
    if portfolio:
        return portfolio
    
    # Fallback to mock data
    return Portfolio(
        total_value=50000.00,
        cash=15000.00,
        invested=35000.00,
        gains=5000.00,
        gains_percent=10.0
    )

@app.get("/api/v1/account/holdings", response_model=list)
async def get_holdings(settings: Settings = Depends(get_settings)):
    """Get holdings from Sharekhan"""
    
    if not settings.SHAREKHAN_CLIENT_ID:
        # Return mock data if no credentials
        return [
            Holding(symbol="AAPL", quantity=10, average_price=140.00, current_price=150.25, gains=102.50),
            Holding(symbol="GOOGL", quantity=5, average_price=135.00, current_price=140.50, gains=27.50),
        ]
    
    client = SharekhanClient(
        settings.SHAREKHAN_CLIENT_ID,
        settings.SHAREKHAN_API_KEY,
        settings.SHAREKHAN_SECRET_KEY
    )
    
    holdings = await client.get_holdings()
    if holdings:
        return holdings
    
    # Fallback to mock data
    return [
        Holding(symbol="AAPL", quantity=10, average_price=140.00, current_price=150.25, gains=102.50),
        Holding(symbol="GOOGL", quantity=5, average_price=135.00, current_price=140.50, gains=27.50),
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
        }
    ]

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
async def get_watchlist(settings: Settings = Depends(get_settings)):
    """Get watchlist from Sharekhan"""
    
    if not settings.SHAREKHAN_CLIENT_ID:
        # Return mock data if no credentials
        return [
            WatchlistItem(symbol="NVDA", price=875.50, change_percent=4.2),
            WatchlistItem(symbol="META", price=485.75, change_percent=2.1),
        ]
    
    client = SharekhanClient(
        settings.SHAREKHAN_CLIENT_ID,
        settings.SHAREKHAN_API_KEY,
        settings.SHAREKHAN_SECRET_KEY
    )
    
    watchlist = await client.get_watchlist()
    if watchlist:
        return watchlist
    
    # Fallback to mock data
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