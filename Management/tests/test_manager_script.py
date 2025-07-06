import os
import argparse

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from Management.app.models.base import Base
from Management.app.models.user import User
from Management.scripts import manager


@pytest.mark.anyio
async def test_create_user_cli(anyio_backend):
    engine = create_async_engine(os.environ["TEST_DATABASE_URL"])
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    parser = manager.build_parser()
    args = parser.parse_args(
        [
            "create_user",
            "--username",
            "cliuser",
            "--password",
            "secret",
            "--email",
            "cli@example.com",
            "--role",
            "reader",
        ]
    )
    await args.func(args)

    async with async_session() as session:
        result = await session.execute(select(User).where(User.username == "cliuser"))
        user = result.scalar_one_or_none()
        assert user is not None
        assert user.username == "cliuser"

    await engine.dispose()
