import uuid
from typing import List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.agent import Agent
from ..schemas.agent import AgentCreate, AgentUpdate


class AgentService:
    """Service object for agent-related operations."""

    async def create(self, db: AsyncSession, agent_in: AgentCreate) -> Agent:
        agent = Agent(host_name=agent_in.host_name, os=agent_in.os)
        db.add(agent)
        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            raise
        await db.refresh(agent)
        return agent

    async def get(self, db: AsyncSession, agent_id: uuid.UUID) -> Agent | None:
        result = await db.execute(select(Agent).where(Agent.agent_id == agent_id))
        return result.scalar_one_or_none()

    async def list(self, db: AsyncSession) -> List[Agent]:
        result = await db.execute(select(Agent).order_by(Agent.onboarded_time.desc()))
        return list(result.scalars())

    async def update(
        self, db: AsyncSession, agent: Agent, agent_in: AgentUpdate
    ) -> Agent:
        if agent_in.host_name is not None:
            agent.host_name = agent_in.host_name
        if agent_in.os is not None:
            agent.os = agent_in.os
        await db.commit()
        await db.refresh(agent)
        return agent

    async def delete(self, db: AsyncSession, agent: Agent) -> None:
        await db.delete(agent)
        await db.commit()
