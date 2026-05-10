"""
deps.py
-------
Reusable FastAPI dependency that yields a SQLAlchemy session
and guarantees the session is closed after every request.
"""

from typing import Generator
from sqlalchemy.orm import Session
from .database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Dependency injected into route handlers.

    Usage:
        @router.get("/example")
        def example(db: Session = Depends(get_db)):
            ...
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()