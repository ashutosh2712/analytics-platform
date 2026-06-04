from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


SYNC_DATABASE_URL = settings.DATABASE_URL.replace(
    "+asyncpg",
    ""
)

engine = create_engine(
    SYNC_DATABASE_URL
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)