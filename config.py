"""
Configuration management for Stock Prediction API
"""

import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = "Stock Prediction API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "AI-powered stock prediction with Sharekhan integration"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = int(os.getenv("PORT", 8000))
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]
    
    # Sharekhan API
    SHAREKHAN_CLIENT_ID: str = os.getenv("SHAREKHAN_CLIENT_ID", "")
    SHAREKHAN_API_KEY: str = os.getenv("SHAREKHAN_API_KEY", "")
    SHAREKHAN_SECRET_KEY: str = os.getenv("SHAREKHAN_SECRET_KEY", "")
    SHAREKHAN_BASE_URL: str = "https://api.sharekhan.com"
    SHAREKHAN_TIMEOUT: int = 30
    
    # NewsAPI
    NEWSAPI_KEY: str = os.getenv("NEWSAPI_KEY", "")
    NEWSAPI_BASE_URL: str = "https://newsapi.org/v2"
    
    # Claude API
    CLAUDE_API_KEY: str = os.getenv("CLAUDE_API_KEY", "")
    CLAUDE_API_URL: str = "https://api.anthropic.com/v1"
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./test.db"
    )
    DATABASE_ECHO: bool = DEBUG
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    
    # Cache
    CACHE_ENABLED: bool = True
    CACHE_TTL: int = 3600  # 1 hour
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Features
    FEATURE_TECHNICAL_ANALYSIS: bool = True
    FEATURE_NEWS_ANALYSIS: bool = False
    FEATURE_CLAUDE_SENTIMENT: bool = False
    FEATURE_SHAREKHAN_INTEGRATION: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create global settings instance
settings = Settings()

def get_settings() -> Settings:
    """Get application settings"""
    return settings

def is_production() -> bool:
    """Check if running in production"""
    return settings.ENVIRONMENT.lower() == "production"

def is_development() -> bool:
    """Check if running in development"""
    return settings.ENVIRONMENT.lower() == "development"

def is_testing() -> bool:
    """Check if running in testing"""
    return settings.ENVIRONMENT.lower() == "testing"
