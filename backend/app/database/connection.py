"""
Database connection and session management.
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.core.config import settings

logger = settings.logger

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
    if "sqlite" in settings.DATABASE_URL
    else {},
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


def get_db() -> Generator[Session]:
    """
    Get database session for dependency injection.

    Yields:
        Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize database by creating all tables.
    """

    Base.metadata.create_all(bind=engine)


def reset_db() -> None:
    """
    Reset database by dropping all tables and recreating them.
    WARNING: This will delete all data!
    """

    logger.warning("Resetting database - all data will be lost!")
    Base.metadata.drop_all(bind=engine)
    logger.info("All tables dropped")
    Base.metadata.create_all(bind=engine)
    logger.info("All tables recreated")
