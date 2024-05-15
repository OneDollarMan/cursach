import os
from typing import AsyncGenerator
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from models import User, Base


DATABASE_URL = f'postgresql+asyncpg://{os.getenv("POSTGRES_USER", default="postgres")}:{os.getenv("POSTGRES_PASSWORD", default="postgres")}@{os.getenv("POSTGRES_HOST", default="127.0.0.1")}:{os.getenv("POSTGRES_PORT", default=5432)}/{os.getenv("POSTGRES_DB", default="boosty")}'
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
