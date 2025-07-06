import os

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from Management.app.models.agent import Agent
from Management.app.models.base import Base
from Management.app.schemas.agent import AgentCreate
from Management.app.services.agent_service import AgentService


@pytest.mark.anyio
async def test_create_and_get_agent(anyio_backend):
    engine = create_async_engine(os.environ["TEST_DATABASE_URL"])
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    service = AgentService()
    async with async_session() as session:
        created = await service.create(
            session, AgentCreate(host_name="test", os="linux")
        )
        assert created.host_name == "test"
        fetched = await service.get(session, created.agent_id)
        assert fetched is not None
        assert fetched.agent_id == created.agent_id

    await engine.dispose()
