"""
database.py
-----------
SQLAlchemy engine, session factory, and declarative base for EDWISERR.
Database file: edwiserr.db (SQLite)
"""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.pool import StaticPool
import logging

logger = logging.getLogger(__name__)

# ─── Database URL ─────────────────────────────────────────────────────────────
SQLITE_DATABASE_URL = "sqlite:///./edwiserr.db"

# ─── Engine ───────────────────────────────────────────────────────────────────
# connect_args: check_same_thread=False required for SQLite + FastAPI
# StaticPool ensures a single connection is reused safely in tests / MVP
engine = create_engine(
    SQLITE_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,          # safe for SQLite in single-process MVP
    echo=False,                    # set True for SQL query logging during dev
)

# Enable WAL mode + foreign keys on every new connection
@event.listens_for(engine, "connect")
def set_sqlite_pragmas(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")   # Write-Ahead Logging for concurrency
    cursor.execute("PRAGMA foreign_keys=ON;")    # Enforce FK constraints
    cursor.execute("PRAGMA synchronous=NORMAL;") # Good durability / speed balance
    cursor.close()

# ─── Session Factory ──────────────────────────────────────────────────────────
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# ─── Declarative Base ─────────────────────────────────────────────────────────
class Base(DeclarativeBase):
    pass

# ─── Table Initialization ─────────────────────────────────────────────────────
def init_db() -> None:
    """
    Create all tables derived from Base.metadata.
    Call once at application startup.
    """
    # Import models here so they register on Base.metadata before create_all
    from models import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    logger.info("✅  EDWISERR database initialized — edwiserr.db")