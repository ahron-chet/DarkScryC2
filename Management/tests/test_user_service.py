import os

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from Management.app.models.base import Base
from Management.app.models.user import UserRole
from Management.app.schemas.user import UserCreate, UserUpdate
from Management.app.services.user_service import UserService


@pytest.mark.anyio
async def test_create_user_weak_password(anyio_backend):
    engine = create_async_engine(os.environ["TEST_DATABASE_URL"])
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    service = UserService()
    async with async_session() as session:
        user_in = UserCreate(
            username="weak",
            password="short",
            email="weak@example.com",
            role=UserRole.READER,
        )
        with pytest.raises(ValueError):
            await service.create(session, user_in)

    await engine.dispose()


@pytest.mark.anyio
async def test_update_user_weak_password(anyio_backend):
    engine = create_async_engine(os.environ["TEST_DATABASE_URL"])
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    service = UserService()
    async with async_session() as session:
        strong_user = await service.create(
            session,
            UserCreate(
                username="good",
                password="Str0ng!Pass",
                email="good@example.com",
                role=UserRole.READER,
            ),
        )
        with pytest.raises(ValueError):
            await service.update(
                session,
                strong_user,
                UserUpdate(password="weak"),
            )

    await engine.dispose()
