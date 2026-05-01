#!/bin/bash

# Stock Prediction API - Local Development Script

set -e

echo "=========================================="
echo "Stock Prediction API - Development Setup"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${BLUE}Checking Python version...${NC}"
python --version || { echo -e "${RED}Python not found${NC}"; exit 1; }

# Create virtual environment
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Creating virtual environment...${NC}"
    python -m venv venv
    echo -e "${GREEN}Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate

# Upgrade pip
echo -e "${BLUE}Upgrading pip...${NC}"
pip install --upgrade pip setuptools wheel

# Install dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
pip install -r requirements.txt

# Create .env if not exists
if [ ! -f ".env" ]; then
    echo -e "${BLUE}Creating .env file...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Update .env with your credentials${NC}"
fi

# Initialize database
echo -e "${BLUE}Initializing database...${NC}"
python -c "from database import init_db; init_db()" 2>/dev/null || echo -e "${YELLOW}Database already initialized${NC}"

# Start application
echo -e "${GREEN}=========================================="
echo "Starting Stock Prediction API"
echo "==========================================${NC}"
echo -e "${BLUE}API URL: http://localhost:8000${NC}"
echo -e "${BLUE}API Docs: http://localhost:8000/docs${NC}"
echo -e "${BLUE}ReDoc: http://localhost:8000/redoc${NC}"
echo -e "${GREEN}=========================================${NC}\n"

# Run the application
python -m uvicorn main_complete:app --host 0.0.0.0 --port 8000 --reload

# Cleanup on exit
echo -e "\n${YELLOW}Cleaning up...${NC}"
deactivate 2>/dev/null || true

echo -e "${GREEN}Goodbye!${NC}"
