# 🚀 Complete Setup Guide - Railway Backend

## 📋 Overview

This is a **production-ready FastAPI backend** for the Stock Prediction API with:
- ✅ Full stock prediction system
- ✅ Sharekhan account integration
- ✅ Portfolio & holdings management
- ✅ Orders & trades tracking
- ✅ News aggregation
- ✅ Admin features
- ✅ Docker support
- ✅ Railway.app deployment ready

## 📁 Project Structure

```
Railway-Backend/
├── main_complete.py          # Main FastAPI application
├── config.py                 # Configuration management
├── models.py                 # Database models
├── schemas.py                # Pydantic schemas
├── database.py               # Database setup
├── services.py               # Business logic
├── utils.py                  # Utility functions
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker configuration
├── docker-compose.yml        # Local development setup
├── railway.json              # Railway.app config
├── run.sh                    # Unix startup script
├── run.bat                   # Windows startup script
├── .env.example              # Environment variables template
├── .gitignore               # Git ignore rules
├── README.md                # Project README
├── DEPLOY.md                # Deployment guide
├── API_DOCS.md              # Complete API documentation
├── SETUP_GUIDE.md           # This file
└── ...other files
```

## 🎯 Quick Start

### Option 1: Local Development (No Docker)

#### Step 1: Prerequisites
```bash
# Required
- Python 3.11+
- pip
- Git

# Optional
- PostgreSQL (for production database)
- Redis (for caching)
```

#### Step 2: Clone/Download
```bash
git clone https://github.com/your-username/stock-prediction-api.git
cd Railway-Backend
```

#### Step 3: Setup Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate.bat
```

#### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 5: Create .env File
```bash
cp .env.example .env

# Edit .env with your credentials:
# SHAREKHAN_CLIENT_ID=...
# SHAREKHAN_API_KEY=...
# SHAREKHAN_SECRET_KEY=...
```

#### Step 6: Run Application

**Using the startup script:**
```bash
# macOS/Linux
chmod +x run.sh
./run.sh

# Windows
run.bat
```

**Or manually:**
```bash
python -m uvicorn main_complete:app --host 0.0.0.0 --port 8000 --reload
```

#### Step 7: Access API
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

### Option 2: Local Development (With Docker)

#### Step 1: Prerequisites
```bash
- Docker
- Docker Compose
- Git
```

#### Step 2: Clone/Download
```bash
git clone https://github.com/your-username/stock-prediction-api.git
cd Railway-Backend
```

#### Step 3: Create .env
```bash
cp .env.example .env
# Edit with your credentials
```

#### Step 4: Start Services
```bash
# Start all services (API, PostgreSQL, Redis, pgAdmin)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

#### Step 5: Access Services
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- pgAdmin: http://localhost:5050 (admin@example.com / admin)

---

### Option 3: Deploy to Railway.app

#### Step 1: Prepare Repository

```bash
# Initialize git
git init
git add .
git commit -m "Initial commit: Stock Prediction API"

# Create repo on GitHub
# https://github.com/new

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/stock-prediction-api.git
git branch -M main
git push -u origin main
```

#### Step 2: Create Railway Project

1. Go to: https://railway.app
2. Login with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub"
5. Select your repository
6. Railway auto-detects Python and Dockerfile

#### Step 3: Add Environment Variables

In Railway dashboard:
1. Go to your project
2. Settings → Variables
3. Add all variables from .env.example

```
SHAREKHAN_CLIENT_ID = your_client_id
SHAREKHAN_API_KEY = your_api_key
SHAREKHAN_SECRET_KEY = your_secret_key
NEWSAPI_KEY = your_newsapi_key (optional)
CLAUDE_API_KEY = your_claude_key (optional)
ENVIRONMENT = production
DEBUG = false
```

#### Step 4: Deploy

1. Click "Deploy"
2. Wait for build & deployment
3. Get public URL from dashboard
4. Your API is live! 🎉

Example URL: `https://stock-prediction-api-production-xxxx.up.railway.app`

#### Step 5: Add Database (Optional)

For production PostgreSQL:

1. In Railway dashboard: New → PostgreSQL
2. Railway auto-sets DATABASE_URL variable
3. Update code to use database instead of mock data

For caching with Redis:

1. In Railway dashboard: New → Redis
2. Railway auto-sets REDIS_URL variable

---

## 🔐 Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| ENVIRONMENT | No | App environment | production |
| DEBUG | No | Enable debug mode | false |
| PORT | No | Server port | 8000 |
| SHAREKHAN_CLIENT_ID | Yes | Sharekhan API | abc123 |
| SHAREKHAN_API_KEY | Yes | Sharekhan API | xyz789 |
| SHAREKHAN_SECRET_KEY | Yes | Sharekhan API | secret |
| NEWSAPI_KEY | No | NewsAPI key | newskey |
| CLAUDE_API_KEY | No | Claude API key | sk-ant-xxx |
| DATABASE_URL | No | PostgreSQL URL | postgresql://... |
| REDIS_URL | No | Redis URL | redis://... |

---

## 📝 Configuration Files

### main_complete.py
- **Purpose:** Main FastAPI application
- **Contains:** All routes and endpoints
- **Lines:** 500+
- **Functions:** 30+ endpoints

### config.py
- **Purpose:** Configuration management
- **Contains:** Settings class, environment loading
- **Features:** Type-safe settings, defaults

### models.py
- **Purpose:** Database models
- **Contains:** SQLAlchemy models for all tables
- **Models:** 10+ data models

### schemas.py
- **Purpose:** Request/response validation
- **Contains:** Pydantic schemas
- **Schemas:** 15+ validation models

### database.py
- **Purpose:** Database configuration
- **Contains:** Connection pooling, sessions
- **Features:** Health checks, context managers

### services.py
- **Purpose:** Business logic
- **Contains:** PredictionService, AccountService, PortfolioService, etc.
- **Services:** 7+ service classes

### utils.py
- **Purpose:** Utility functions
- **Contains:** Password hashing, JWT tokens, validation, logging
- **Functions:** 30+ utility functions

---

## 🔄 Deployment Workflow

```
Local Development → Git Push → GitHub → Railway Auto-Deploy → Live API
```

**Step-by-step:**

1. **Develop locally** with docker-compose or venv
2. **Test thoroughly** using Swagger UI or cURL
3. **Commit changes** to git
4. **Push to GitHub** (main branch)
5. **Railway auto-deploys** on push
6. **Monitor deployment** in Railway dashboard
7. **Test live API** with your MAUI app

---

## 🧪 Testing

### Manual Testing with cURL

```bash
# Health check
curl https://your-api/health

# Get predictions
curl https://your-api/api/v1/stocks/top-buys/1M

# Login
curl -X POST https://your-api/api/v1/account/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test",
    "password": "test123",
    "twofa": "123456"
  }'

# Get portfolio
curl https://your-api/api/v1/account/portfolio

# Place order
curl -X POST https://your-api/api/v1/account/place-order \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "TCS",
    "quantity": 10,
    "price": 3750.0,
    "order_type": "BUY"
  }'
```

### Automated Testing

```bash
# Using pytest (coming soon)
pytest tests/

# With coverage
pytest --cov=app tests/
```

---

## 📊 Monitoring

### Railway Dashboard

1. **Logs:** Deployments → Logs → View all logs
2. **Metrics:** Metrics → CPU, Memory, Requests
3. **Deployment:** Deployments → History & Status
4. **Environment:** Settings → Variables

### Local Logs

```bash
# View logs while running
docker-compose logs -f api

# Or from stdout in terminal
# You'll see all logs in real-time
```

---

## 🔧 Troubleshooting

### API won't start

**Check logs:**
```bash
railway logs  # Railway app
# or
docker-compose logs api  # Local docker
```

**Common issues:**
- Missing Python 3.11+
- Invalid requirements.txt
- Missing .env variables
- Port 8000 already in use

### Database connection failed

```bash
# Check PostgreSQL
psql postgresql://user:password@localhost:5432/stock_prediction

# Check if Docker container is running
docker ps | grep postgres
```

### Import errors

```bash
# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall

# Clear cache
pip cache purge
```

---

## 📈 Performance Tips

1. **Enable caching** - Redis for frequently accessed data
2. **Use connection pooling** - Already configured in database.py
3. **Add indexes** - On symbol, user_id, created_at columns
4. **Paginate results** - Limit database queries
5. **Monitor resource usage** - Railway provides metrics

---

## 🔐 Security Checklist

- [x] CORS configured
- [x] Environment variables for secrets
- [x] HTTPS on Railway
- [x] 2FA required for login
- [x] Input validation with Pydantic
- [x] Password hashing with bcrypt
- [x] JWT token support
- [x] Rate limiting (coming soon)

---

## 📚 Additional Resources

- **FastAPI Docs:** https://fastapi.tiangolo.com
- **SQLAlchemy Docs:** https://docs.sqlalchemy.org
- **Railway Docs:** https://docs.railway.app
- **Pydantic Docs:** https://docs.pydantic.dev
- **Python Docs:** https://docs.python.org/3

---

## 🤝 Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/amazing`
3. Commit changes: `git commit -am 'Add amazing feature'`
4. Push branch: `git push origin feature/amazing`
5. Submit pull request

---

## 📄 License

MIT License - See LICENSE file

---

## 🎉 You're All Set!

Your Stock Prediction API is ready to go!

Next steps:
1. ✅ Deploy backend to Railway
2. ✅ Connect MAUI frontend
3. ✅ Test with your credentials
4. ✅ Share with users
5. ✅ Monitor & improve

---

**Questions?** Check API_DOCS.md or open an issue on GitHub!
