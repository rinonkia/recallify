"""Database connection management."""

import xid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.database.models import Base


def generate_xid() -> str:
    """Generate a new xid as a string."""
    return xid.new().string()


class Database:
    """Database connection manager."""

    def __init__(self, database_path: str = "./data/recallify.db"):
        """Initialize database connection.

        Args:
            database_path: Path to SQLite database file
        """
        self.engine = create_engine(f"sqlite:///{database_path}")
        self.SessionLocal = sessionmaker(bind=self.engine)

    def init_db(self):
        """Initialize database tables."""
        Base.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        """Get a new database session."""
        return self.SessionLocal()
