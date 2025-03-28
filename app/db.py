from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from app import settings

async_engine = create_async_engine(settings.SQLALCHEMY_URI, echo=True)
async_sessionmaker = sessionmaker(bind=async_engine, class_=AsyncSession)  # noqa
Base = declarative_base()


async def get_async_session() -> AsyncGenerator:
    async with async_sessionmaker() as session:
        yield session
