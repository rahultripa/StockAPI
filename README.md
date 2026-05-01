# Stock Prediction API - Railway Backend

Complete FastAPI backend for stock prediction with Sharekhan integration.

## 📋 Overview

This is a production-ready FastAPI application that provides:

- ✅ **Stock Predictions** - Technical analysis and predictions
- ✅ **Sharekhan Integration** - Login and view your portfolio
- ✅ **Portfolio Management** - View holdings, P&L, orders, trades
- ✅ **News Analysis** - Stock news aggregation
- ✅ **Admin Features** - Feature flags, data sync

## 📁 Project Structure

```
Railway-Backend/
├── main.py                 # FastAPI application (all in one)
├── requirements.txt        # Python dependencies
├── Dockerfile             # Railway deployment config
├── .env.example           # Environment variables template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🚀 Local Setup

### Prerequisites

- Python 3.11+
- pip
- Git

### Step 1: Clone/Download Project

```bash
git clone https://github.com/your-username/stock-prediction-api.git
cd stock-prediction-api
```

### Step 2: Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Create .env File

```bash
# Copy example
cp .env.example .env

# Edit .env with your values
# (Leave Sharekhan values empty for local testing)
```

### Step 5: Run Application

```bash
python main.py

# Or with uvicorn directly
uvicorn main:app --reload --port 8000
```

### Step 6: Test API

Open browser and go to:

```
http://localhost:8000/docs     # Swagger UI
http://localhost:8000/health   # Health check
```

## 🚀 Railway Deployment

### Prerequisites

- Railway.app account (free)
- GitHub account
- Git installed locally

### Step 1: Create GitHub Repository

```bash
# Initialize git
git init
git add .
git commit -m "Initial commit: Stock Prediction API"

# Create repo on GitHub and push
git remote add origin https://github.com/your-username/stock-prediction-api.git
git branch -M main
git push -u origin main
```

### Step 2: Connect to Railway

1. Go to: https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub"
4. Select your repository
5. Railway auto-detects Python and Dockerfile

### Step 3: Add Environment Variables

In Railway dashboard:

1. Go to project → Settings → Variables
2. Add these variables:

```
PORT = 8000
ENVIRONMENT = production
SHAREKHAN_CLIENT_ID = your_client_id
SHAREKHAN_API_KEY = your_api_key
SHAREKHAN_SECRET_KEY = your_secret_key
NEWSAPI_KEY = your_newsapi_key
CLAUDE_API_KEY = your_claude_key
```

### Step 4: Deploy

1. Click "Deploy"
2. Wait for build & deployment
3. Get your API URL from the dashboard
4. Your API is live! 🎉

Example URL: `https://stock-prediction-api-production-xxxx.up.railway.app`

## 📡 API Endpoints

### Health Check

```
GET /health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2026-04-30T11:30:00",
  "version": "1.0.0"
}
```

### Stock Predictions

```
GET /api/v1/stocks/top-buys/1M
GET /api/v1/stocks/predict/{symbol}/1M
GET /api/v1/stocks/predict-with-news/{symbol}/1M
GET /api/v1/stocks/top-sells/1M
```

### Account (Sharekhan)

```
POST /api/v1/account/login              # Login
POST /api/v1/account/logout             # Logout
GET  /api/v1/account/is-authenticated   # Check auth
GET  /api/v1/account/portfolio          # Account summary
GET  /api/v1/account/holdings           # Your stocks
GET  /api/v1/account/holdings/{symbol}  # Specific stock
GET  /api/v1/account/orders             # Your orders
POST /api/v1/account/place-order        # Place order
DELETE /api/v1/account/cancel-order/{id} # Cancel order
GET  /api/v1/account/trades             # Trade history
```

### News

```
GET /api/v1/news/{symbol}
```

### Admin

```
GET  /api/v1/admin/features
PATCH /api/v1/admin/features/{feature_name}
POST /api/v1/admin/sync-data
```

## 🧪 Testing with cURL

### Health Check

```bash
curl https://your-api-url/health
```

### Get Predictions

```bash
curl https://your-api-url/api/v1/stocks/top-buys/1M
```

### Login

```bash
curl -X POST https://your-api-url/api/v1/account/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password",
    "twofa": "123456"
  }'
```

### Get Portfolio

```bash
curl https://your-api-url/api/v1/account/portfolio
```

## 📊 Database (Optional)

To add PostgreSQL database:

1. In Railway dashboard: "New"
2. Select "PostgreSQL"
3. Add DATABASE_URL to environment variables
4. Update models.py to use database instead of mock data

## 🔐 Security

- ✅ CORS enabled
- ✅ Environment variables for secrets
- ✅ HTTPS on Railway
- ✅ 2FA required for login
- ✅ Input validation with Pydantic

## 📈 Monitoring

View logs in Railway dashboard:

```
Logs → View all logs
```

Check app health:

```
Deployments → Logs
```

Monitor metrics:

```
Metrics → View metrics
```

## 🐛 Troubleshooting

### App won't start

Check logs in Railway dashboard:
```
Railway → Project → Deployments → Logs
```

### API returns 500 error

1. Check environment variables are set
2. Check Sharekhan credentials
3. Check logs for error details

### Port already in use (local)

```bash
# Use different port
python main.py --port 8001

# Or kill process using port 8000
# On Windows: netstat -ano | findstr :8000
# On macOS/Linux: lsof -i :8000
```

## 📝 Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| PORT | Server port (default: 8000) | No |
| ENVIRONMENT | production/development | No |
| SHAREKHAN_CLIENT_ID | Sharekhan API client ID | Yes |
| SHAREKHAN_API_KEY | Sharekhan API key | Yes |
| SHAREKHAN_SECRET_KEY | Sharekhan secret key | Yes |
| NEWSAPI_KEY | NewsAPI key | No |
| CLAUDE_API_KEY | Claude API key | No |
| DATABASE_URL | PostgreSQL connection string | No |

## 🤝 Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature/my-feature`
5. Submit pull request

## 📄 License

MIT License - feel free to use this project!

## 📞 Support

- Check Railway documentation: https://docs.railway.app
- FastAPI docs: https://fastapi.tiangolo.com
- Issues: Create GitHub issue

## 🎯 Next Steps

1. Get Sharekhan API credentials
2. Deploy to Railway
3. Connect MAUI frontend
4. Add to mobile app stores
5. Scale with users!

---

**Happy predicting!** 🚀📈
