from typing import AsyncGenerator
from functools import cached_property, lru_cache
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from ..models.base import Base
from .settings import get_app_settings, AppSettings

class DatabaseConfig:
    def __init__(self):
        self.settings = get_app_settings()

    @cached_property
    def engine(self):
        return create_async_engine(self.settings.database_url)

    @cached_property
    def sessionmaker(self):
        return async_sessionmaker(self.engine, expire_on_commit=False)

@lru_cache()
def get_db_config() -> DatabaseConfig:
    return DatabaseConfig()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db_config = get_db_config()
    async with db_config.sessionmaker() as session:
        yield session

async def init_db() -> None:
    db_config = get_db_config()
    async with db_config.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
