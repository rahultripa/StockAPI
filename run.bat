@echo off
REM Stock Prediction API - Windows Development Script

setlocal enabledelayedexpansion

echo.
echo ==========================================
echo Stock Prediction API - Development Setup
echo ==========================================
echo.

REM Check Python
echo Checking Python version...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found
    echo Please install Python 3.11+ from https://www.python.org
    exit /b 1
)

REM Create virtual environment
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env if not exists
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo WARNING: Update .env with your credentials
)

REM Initialize database
echo Initializing database...
python -c "from database import init_db; init_db()" 2>nul || echo Database already initialized

REM Start application
echo.
echo ==========================================
echo Starting Stock Prediction API
echo ==========================================
echo.
echo API URL: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo ReDoc: http://localhost:8000/redoc
echo.
echo ==========================================
echo.

python -m uvicorn main_complete:app --host 0.0.0.0 --port 8000 --reload

echo.
echo Cleaning up...
call venv\Scripts\deactivate.bat 2>nul

echo Goodbye!
endlocal
