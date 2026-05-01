# 🚀 Quick Deploy Guide

Deploy to Railway in 5 minutes!

## Option 1: GitHub → Railway (Recommended)

### Step 1: Prepare Code

```bash
# Clone this repo or create your own with these files:
# - main.py
# - requirements.txt
# - Dockerfile
# - .env.example
# - .gitignore

git init
git add .
git commit -m "Stock Prediction API"
```

### Step 2: Push to GitHub

```bash
# Create repo on GitHub
git remote add origin https://github.com/YOUR_USERNAME/stock-prediction-api.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Railway

1. Go to https://railway.app
2. Login with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub"
5. Select your repository
6. Click "Deploy"

### Step 4: Add Environment Variables

In Railway dashboard:

1. Project → Settings → Variables
2. Click "Add Variable"
3. Add these (or leave blank to use defaults):

```
SHAREKHAN_CLIENT_ID = your_id
SHAREKHAN_API_KEY = your_key
SHAREKHAN_SECRET_KEY = your_secret
```

### Step 5: Get Your URL

1. Go to Deployments
2. Copy the URL under "Public URL"
3. Share with your MAUI app!

Example: `https://stock-prediction-api-production-xxxx.up.railway.app`

## Option 2: Direct Railway CLI

### Step 1: Install Railway CLI

```bash
npm install -g @railway/cli
```

### Step 2: Login

```bash
railway login
```

### Step 3: Initialize Project

```bash
railway init
# Select "Create New Project"
# Enter project name
```

### Step 4: Deploy

```bash
railway up
```

### Step 5: View Deployment

```bash
railway logs
```

## Option 3: Railway Website (No Code)

1. Go to railway.app
2. Create new project
3. Upload all files as ZIP
4. Set environment variables
5. Deploy

## ✅ Verify Deployment

```bash
# Health check
curl https://your-api-url/health

# Get predictions
curl https://your-api-url/api/v1/stocks/top-buys/1M

# Expected response:
# [
#   {"symbol": "TCS", "confidence": 78.5, ...},
#   {"symbol": "INFY", "confidence": 72.0, ...},
#   ...
# ]
```

## 📊 Troubleshooting

### Build fails

Check logs:
```bash
railway logs
```

Common issues:
- Python version (need 3.11+)
- Missing requirements.txt
- Invalid Dockerfile

### App crashes on startup

1. Check environment variables
2. Check PORT=8000 is set
3. View logs: `railway logs`

### Can't connect from MAUI

- Check API URL is correct (with https://)
- Check API is running (visit /health)
- Check CORS is enabled in main.py

## 🎯 Update Deployment

### Edit Code Locally

```bash
# Make changes to main.py

# Commit and push
git add .
git commit -m "Update: Add feature X"
git push origin main
```

Railway auto-redeploys on push!

### Monitor Deployment

```bash
# View logs
railway logs -f  # Follow logs

# Check status
railway status

# Restart app
railway redeploy
```

## 📈 Scale Your App

### Add Database

```bash
# In Railway dashboard:
# 1. New → PostgreSQL
# 2. Set DATABASE_URL environment variable
# 3. Update main.py to use database
```

### Add Caching

```bash
# In Railway dashboard:
# 1. New → Redis
# 2. Use for caching predictions
```

### Custom Domain

```bash
# In Railway dashboard:
# Project Settings → Custom Domain
# Add your domain
```

## 🔧 Environment Variables

Set in Railway dashboard:

```
PORT = 8000                          # Server port
ENVIRONMENT = production             # production/development
SHAREKHAN_CLIENT_ID = your_id        # Sharekhan API
SHAREKHAN_API_KEY = your_key         # Sharekhan API
SHAREKHAN_SECRET_KEY = your_secret   # Sharekhan API
NEWSAPI_KEY = your_key               # NewsAPI (optional)
CLAUDE_API_KEY = sk-ant-xxxxx        # Claude API (optional)
DATABASE_URL = postgresql://...      # PostgreSQL (optional)
```

## 📞 Support

- Railway Docs: https://docs.railway.app
- FastAPI Docs: https://fastapi.tiangolo.com
- Issues: Create GitHub issue

## 🎉 You're Done!

Your API is now live! 🚀

Share the URL with your MAUI app and start trading! 📈
