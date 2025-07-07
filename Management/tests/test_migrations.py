import asyncio
import os

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.models.base import Base

pytestmark = pytest.mark.anyio


async def test_run_migrations(tmp_path):
    os.environ["MANAGEMENT_DATABASE_URL"] = os.environ["TEST_DATABASE_URL"]
    os.environ["MANAGEMENT_SECRET_KEY"] = "secret"

    cfg = Config("alembic.ini")
    cfg.set_main_option("script_location", "migrations")

    engine = create_async_engine(os.environ["TEST_DATABASE_URL"])
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.execute(text("DROP TABLE IF EXISTS alembic_version"))

    await asyncio.to_thread(command.upgrade, cfg, "head")

    async with engine.connect() as conn:
        res = await conn.execute(text("SELECT to_regclass('public.user')"))
        assert res.scalar() is not None
        res = await conn.execute(text("SELECT to_regclass('public.application_agent')"))
        assert res.scalar() is not None
    await engine.dispose()

    await asyncio.to_thread(command.downgrade, cfg, "base")
