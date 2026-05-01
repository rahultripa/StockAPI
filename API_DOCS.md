# Stock Prediction API - Complete Documentation

## 📌 Base URL

```
https://stock-prediction-api-production-xxxx.up.railway.app
```

## 📡 Authentication

Most endpoints require authentication via login.

```bash
# Login first
curl -X POST https://api/account/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password",
    "twofa": "123456"
  }'

# Check authentication status
curl https://api/account/is-authenticated
```

## 🏥 Health Check

### `GET /health`

Check API status

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-04-30T11:30:00.000Z",
  "version": "1.0.0"
}
```

## 📊 Stock Predictions

### `GET /api/v1/stocks/top-buys/{timeframe}`

Get top buy recommendations

**Parameters:**
- `timeframe` (path): `1W`, `1M`, `3M`, `1Y`

**Response:**
```json
[
  {
    "symbol": "TCS",
    "confidence": 78.5,
    "target_price": 3750.0,
    "reason": "Strong uptrend"
  },
  {
    "symbol": "INFY",
    "confidence": 72.0,
    "target_price": 2340.0,
    "reason": "MA positive"
  }
]
```

### `GET /api/v1/stocks/predict/{symbol}/{timeframe}`

Get prediction for specific stock

**Parameters:**
- `symbol` (path): Stock symbol (e.g., TCS)
- `timeframe` (path): `1W`, `1M`, `3M`, `1Y`

**Response:**
```json
{
  "symbol": "TCS",
  "timeframe": "1M",
  "technical_score": 72.5,
  "news_sentiment_score": null,
  "final_score": 72.5,
  "prediction": "BUY",
  "confidence": 78.5,
  "target_price": 3750.0,
  "technical_reason": "MA trend positive, RSI 58, Volume +15%",
  "reason": "Strong uptrend",
  "articles_analyzed": 0
}
```

### `GET /api/v1/stocks/top-sells/{timeframe}`

Get top sell recommendations

**Parameters:**
- `timeframe` (path): `1W`, `1M`, `3M`, `1Y`

## 🔐 Account Management

### `POST /api/v1/account/login`

Login to Sharekhan account

**Request:**
```json
{
  "username": "your_username",
  "password": "your_password",
  "twofa": "123456"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully logged in",
  "user_id": "user_your_username"
}
```

### `POST /api/v1/account/logout`

Logout from account

**Response:**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

### `GET /api/v1/account/is-authenticated`

Check authentication status

**Response:**
```json
{
  "authenticated": true,
  "user_id": "user_your_username"
}
```

## 💰 Portfolio Management

### `GET /api/v1/account/portfolio`

Get portfolio summary (requires authentication)

**Response:**
```json
{
  "account_balance": 500000.0,
  "portfolio_value": 750000.0,
  "total_profit": 150000.0,
  "profit_percent": 25.0,
  "cash_available": 200000.0,
  "margin_available": 100000.0,
  "holdings_count": 3
}
```

### `GET /api/v1/account/holdings`

Get all holdings (requires authentication)

**Response:**
```json
[
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
  }
]
```

### `GET /api/v1/account/holdings/{symbol}`

Get specific holding (requires authentication)

**Parameters:**
- `symbol` (path): Stock symbol (e.g., TCS)

**Response:**
```json
{
  "symbol": "TCS",
  "quantity": 10,
  "current_price": 3750.0,
  "buy_price": 3200.0,
  "profit": 5500.0,
  "profit_percent": 17.1,
  "value": 37500.0
}
```

## 📋 Orders

### `GET /api/v1/account/orders`

Get orders (requires authentication)

**Parameters:**
- `status` (query): `open`, `closed`, `all` (default: `open`)

**Response:**
```json
[
  {
    "order_id": "ORD001",
    "symbol": "WIPRO",
    "quantity": 50,
    "price": 380.0,
    "order_type": "BUY",
    "status": "OPEN",
    "created_at": "2026-04-30T10:30:00",
    "executed_quantity": 0
  }
]
```

### `POST /api/v1/account/place-order`

Place a new order (requires authentication)

**Request:**
```json
{
  "symbol": "WIPRO",
  "quantity": 50,
  "price": 380.0,
  "order_type": "BUY",
  "product": "MIS"
}
```

**Response:**
```json
{
  "success": true,
  "order_id": "ORD003",
  "message": "Order placed successfully"
}
```

### `DELETE /api/v1/account/cancel-order/{order_id}`

Cancel an order (requires authentication)

**Parameters:**
- `order_id` (path): Order ID to cancel

**Response:**
```json
{
  "success": true,
  "message": "Order ORD001 cancelled"
}
```

## 📈 Trades

### `GET /api/v1/account/trades`

Get trade history (requires authentication)

**Parameters:**
- `limit` (query): Number of trades to fetch (default: 100)

**Response:**
```json
[
  {
    "trade_id": "TRD001",
    "symbol": "TCS",
    "quantity": 10,
    "price": 3200.0,
    "trade_type": "BUY",
    "timestamp": "2026-04-15T09:30:00",
    "exchange": "NSE"
  }
]
```

## 📰 News

### `GET /api/v1/news/{symbol}`

Get news for a stock

**Parameters:**
- `symbol` (path): Stock symbol (e.g., TCS)
- `days` (query): Days of news to fetch (default: 7)

**Response:**
```json
{
  "symbol": "TCS",
  "articles": [
    {
      "headline": "Positive analysis for TCS",
      "source": "Economic Times",
      "sentiment": "POSITIVE",
      "sentiment_score": 0.85,
      "impact_level": "HIGH",
      "published_at": "2026-04-30T10:00:00Z"
    }
  ],
  "total_articles": 2
}
```

## ⭐ Watchlist

### `GET /api/v1/watchlist`

Get user's watchlist (requires authentication)

**Response:**
```json
{
  "watchlist": [
    {"symbol": "TCS", "notes": "Strong performer"},
    {"symbol": "INFY", "notes": "Tech leader"}
  ],
  "count": 2
}
```

### `POST /api/v1/watchlist/{symbol}`

Add to watchlist (requires authentication)

**Parameters:**
- `symbol` (path): Stock symbol
- `notes` (query): Optional notes

**Response:**
```json
{
  "success": true,
  "message": "TCS added to watchlist"
}
```

### `DELETE /api/v1/watchlist/{symbol}`

Remove from watchlist (requires authentication)

**Parameters:**
- `symbol` (path): Stock symbol

**Response:**
```json
{
  "success": true,
  "message": "TCS removed from watchlist"
}
```

## ⚙️ Admin

### `GET /api/v1/admin/features`

Get feature flags

**Response:**
```json
[
  {
    "feature_name": "technical_analysis",
    "enabled": true,
    "description": "Technical analysis and predictions"
  },
  {
    "feature_name": "news_analysis",
    "enabled": false,
    "description": "News sentiment analysis"
  }
]
```

### `PATCH /api/v1/admin/features/{feature_name}`

Update feature flag

**Parameters:**
- `feature_name` (path): Feature name
- `enabled` (query): true/false

**Response:**
```json
{
  "success": true,
  "feature_name": "news_analysis",
  "enabled": true,
  "message": "Feature news_analysis updated"
}
```

### `POST /api/v1/admin/sync-data`

Sync data from Sharekhan

**Response:**
```json
{
  "success": true,
  "message": "Data synced successfully",
  "synced_at": "2026-04-30T11:30:00.000Z"
}
```

## 🔄 Example Workflows

### Workflow 1: Login and View Portfolio

```bash
# 1. Login
curl -X POST https://api/account/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "rahul",
    "password": "password123",
    "twofa": "123456"
  }'

# 2. Get Portfolio
curl https://api/account/portfolio

# 3. Get Holdings
curl https://api/account/holdings

# 4. Get Specific Holding
curl https://api/account/holdings/TCS
```

### Workflow 2: Get Predictions and Place Order

```bash
# 1. Get Top Buys
curl https://api/stocks/top-buys/1M

# 2. Get Specific Prediction
curl https://api/stocks/predict/TCS/1M

# 3. Login (if not already)
curl -X POST https://api/account/login ...

# 4. Place Order
curl -X POST https://api/account/place-order \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "TCS",
    "quantity": 10,
    "price": 3750.0,
    "order_type": "BUY"
  }'

# 5. Get Order Status
curl https://api/account/orders
```

### Workflow 3: Manage Watchlist

```bash
# 1. Add to Watchlist
curl -X POST https://api/watchlist/TCS?notes="Strong+performer"

# 2. Add Another
curl -X POST https://api/watchlist/INFY?notes="Tech+leader"

# 3. View Watchlist
curl https://api/watchlist

# 4. Remove from Watchlist
curl -X DELETE https://api/watchlist/INFY
```

## ⚠️ Error Responses

### 401 Unauthorized
```json
{
  "success": false,
  "error": "Not authenticated",
  "status_code": 401
}
```

### 404 Not Found
```json
{
  "success": false,
  "error": "No prediction for XYZ",
  "status_code": 404
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "error": "Internal server error",
  "message": "Detailed error message",
  "status_code": 500
}
```

## 📚 Data Types

### Stock Symbol
- Type: String
- Format: Uppercase (e.g., TCS, INFY)
- Length: 1-10 characters

### Timeframe
- Type: String
- Valid Values: `1W`, `1M`, `3M`, `1Y`

### Order Type
- Type: String
- Valid Values: `BUY`, `SELL`

### Order Status
- Type: String
- Valid Values: `OPEN`, `EXECUTED`, `CANCELLED`

### Sentiment
- Type: String
- Valid Values: `POSITIVE`, `NEGATIVE`, `NEUTRAL`

## 🔗 Related Resources

- API Documentation: `/docs`
- ReDoc Documentation: `/redoc`
- OpenAPI Schema: `/openapi.json`
- GitHub Repository: https://github.com/rahultripa/stock-prediction-api
- Railway App: https://railway.app

## 💡 Tips

1. **Always authenticate first** before accessing account endpoints
2. **Store user_id** after login for later reference
3. **Check feature flags** to see what's enabled
4. **Use 2FA codes** that are exactly 6 digits
5. **Handle rate limits** gracefully (coming soon)
6. **Cache predictions** to reduce API calls
7. **Subscribe to webhooks** for real-time updates (coming soon)

## 🆘 Support

For issues, bugs, or feature requests:
1. Check API logs: Railway Dashboard → Logs
2. Verify environment variables are set correctly
3. Test endpoints using Swagger UI: `/docs`
4. Open issue on GitHub

---

**Last Updated:** April 30, 2026  
**Version:** 1.0.0  
**Status:** Production Ready
