"""Database session and connection management."""
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL, MONGODB_URI, MONGODB_DB_NAME
import pymongo
from typing import Optional

# SQLAlchemy Engine & Session
is_sqlite = DATABASE_URL.startswith("sqlite")
connect_args = {"check_same_thread": False} if is_sqlite else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False
)

# Enforce foreign key constraints in SQLite
if is_sqlite:
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """FastAPI dependency for database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# MongoDB Atlas Integration
_mongo_client: Optional[pymongo.MongoClient] = None
_mongo_db = None

if MONGODB_URI:
    try:
        _mongo_client = pymongo.MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        _mongo_db = _mongo_client[MONGODB_DB_NAME]
    except Exception as e:
        print(f"[MongoDB] Atlas connection initialization error: {e}")
        _mongo_client = None
        _mongo_db = None

def get_mongo_db():
    """Retrieve MongoDB database instance if configured."""
    return _mongo_db

def init_db():
    """Initialize database tables and run lightweight migrations."""
    from app.db import models  # Ensure all models are imported
    Base.metadata.create_all(bind=engine)

    # Auto-migrate SQLite columns if missing
    if is_sqlite:
        try:
            with engine.connect() as conn:
                # Check documents columns
                doc_cols = [row[1] for row in conn.exec_driver_sql("PRAGMA table_info(documents)").fetchall()]
                if "contract_type" not in doc_cols:
                    conn.exec_driver_sql("ALTER TABLE documents ADD COLUMN contract_type VARCHAR(64) DEFAULT 'GENERAL'")
                if "currency" not in doc_cols:
                    conn.exec_driver_sql("ALTER TABLE documents ADD COLUMN currency VARCHAR(16) DEFAULT 'INR'")

                # Check findings columns
                fnd_cols = [row[1] for row in conn.exec_driver_sql("PRAGMA table_info(findings)").fetchall()]
                if "market_deviation" not in fnd_cols:
                    conn.exec_driver_sql("ALTER TABLE findings ADD COLUMN market_deviation BOOLEAN DEFAULT 0")
                if "suggested_counter" not in fnd_cols:
                    conn.exec_driver_sql("ALTER TABLE findings ADD COLUMN suggested_counter TEXT")
                conn.commit()
        except Exception as e:
            print(f"[ContractLens Engine] SQLite auto-migration notice: {e}")
