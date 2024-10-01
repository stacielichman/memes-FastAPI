from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL)
async_session = sessionmaker(engine, autocommit=False, autoflush=False, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()
