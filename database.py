"""
Database initialization and session management
"""

import logging
from typing import Generator
from sqlalchemy import create_engine, event, pool
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool, NullPool
from config import settings, is_development
from models import Base

logger = logging.getLogger(__name__)

# ============================================================================
# DATABASE ENGINE CREATION
# ============================================================================

def get_database_engine():
    """Create database engine based on settings"""
    
    database_url = settings.DATABASE_URL
    
    logger.info(f"📊 Creating database engine for: {database_url}")
    
    # Use appropriate connection pooling
    if "sqlite" in database_url:
        # SQLite doesn't support connection pooling well
        engine = create_engine(
            database_url,
            connect_args={"check_same_thread": False},
            poolclass=NullPool,
            echo=settings.DATABASE_ECHO
        )
    else:
        # Use QueuePool for production databases
        engine = create_engine(
            database_url,
            poolclass=QueuePool,
            pool_size=settings.DATABASE_POOL_SIZE,
            max_overflow=settings.DATABASE_MAX_OVERFLOW,
            pool_pre_ping=True,
            echo=settings.DATABASE_ECHO
        )
    
    # Add event listeners for SQLite
    if "sqlite" in database_url:
        @event.listens_for(engine, "connect")
        def set_sqlite_pragma(dbapi_conn, connection_record):
            cursor = dbapi_conn.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()
    
    logger.info("✅ Database engine created successfully")
    return engine

# ============================================================================
# SESSION FACTORY
# ============================================================================

engine = get_database_engine()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

def init_db():
    """Initialize database tables"""
    logger.info("🗂️  Initializing database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables initialized successfully")
    except Exception as e:
        logger.error(f"❌ Error initializing database: {str(e)}")
        raise

def drop_all_tables():
    """Drop all tables (development only)"""
    if not is_development():
        raise Exception("Cannot drop tables in production!")
    
    logger.warning("⚠️  Dropping all database tables...")
    Base.metadata.drop_all(bind=engine)
    logger.info("✅ All tables dropped")

# ============================================================================
# SESSION MANAGEMENT
# ============================================================================

def get_db() -> Generator[Session, None, None]:
    """
    Dependency for getting database session
    
    Usage in FastAPI routes:
    @app.get("/items")
    def get_items(db: Session = Depends(get_db)):
        return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"❌ Database session error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

def get_db_connection():
    """Get raw database connection"""
    return SessionLocal()

# ============================================================================
# HEALTH CHECK
# ============================================================================
def check_database_connection() -> bool:
    """Check if database is accessible"""
    try:
        db = SessionLocal()
        # Try to execute a simple query
        db.execute(text("SELECT 1"))  # ← ADD text() HERE
        db.close()
        logger.info("✅ Database connection OK")
        return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {str(e)}")
        return False
# ============================================================================
# CONTEXT MANAGERS
# ============================================================================

class DatabaseSession:
    """Context manager for database sessions"""
    
    def __init__(self):
        self.db = None
    
    def __enter__(self):
        self.db = SessionLocal()
        return self.db
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db:
            if exc_type is None:
                self.db.commit()
            else:
                self.db.rollback()
            self.db.close()

# ============================================================================
# CLEANUP
# ============================================================================

def cleanup_db():
    """Cleanup database connections"""
    logger.info("🔌 Closing database connections...")
    engine.dispose()
    logger.info("✅ Database connections closed")

# ============================================================================
# INITIALIZATION
# ============================================================================

# Initialize database on import
try:
    init_db()
except Exception as e:
    logger.error(f"Failed to initialize database: {str(e)}")
    if not is_development():
        raise
