import uuid
from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database import get_db
from ..schemas.agent import AgentCreate, AgentRead, AgentUpdate, Deleted
from ..services.agent_service import AgentService


class AgentController:
    """Controller with common agent operations."""

    session: AsyncSession = Depends(get_db)
    service: AgentService = Depends(AgentService)

    async def create_agent(self, agent_in: AgentCreate) -> AgentRead:
        agent = await self.service.create(self.session, agent_in)
        return AgentRead.model_validate(agent)

    async def get_agent(self, agent_id: uuid.UUID) -> AgentRead:
        agent = await self.service.get(self.session, agent_id)
        if agent is None:
            raise HTTPException(status_code=404, detail="Agent not found")
        return AgentRead.model_validate(agent)

    async def list_agents(self) -> List[AgentRead]:
        agents = await self.service.list(self.session)
        return [AgentRead.model_validate(a) for a in agents]

    async def update_agent(
        self, agent_id: uuid.UUID, agent_in: AgentUpdate
    ) -> AgentRead:
        agent = await self.service.get(self.session, agent_id)
        if agent is None:
            raise HTTPException(status_code=404, detail="Agent not found")
        agent = await self.service.update(self.session, agent, agent_in)
        return AgentRead.model_validate(agent)

    async def delete_agent(self, agent_id: uuid.UUID) -> Deleted:
        agent = await self.service.get(self.session, agent_id)
        if agent is None:
            raise HTTPException(status_code=404, detail="Agent not found")
        await self.service.delete(self.session, agent)
        return Deleted()
