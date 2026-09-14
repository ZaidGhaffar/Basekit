import uuid
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Numeric, Integer, Text, Float, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship,declarative_base
from datetime import datetime, timezone
from .conifg import settings
from fastapi import Depends
from typing import Annotated


url = settings.DATABASE_URL.replace("postgresql://","postgresql+asyncpg://")
database_url = url.split("?")[0]
engine = create_async_engine(database_url,connect_args={"ssl": True})
AsyncSessionLocal = async_sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)
Base = declarative_base()


    
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


db_dependency = Annotated[AsyncSession, Depends(get_db)]
