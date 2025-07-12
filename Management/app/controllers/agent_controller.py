import uuid
from typing import List

from darkscryc2server.utils.remote_manager import (
    remote_get_connection,
    remote_get_connections,
)
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database import get_db
from ..schemas.agent import AgentCreate, AgentRead, AgentUpdate, Deleted
from ..services.agent_service import AgentService


class AgentController:
    """Controller with common agent operations."""

    session: AsyncSession = Depends(get_db)
    service: AgentService = Depends(AgentService)

    async def _get_connections(self, agent_id: str | None = None) -> dict[str, dict]:
        """Return active connections from the C2 server."""
        try:
            if agent_id:
                data = await remote_get_connection(agent_id)
            else:
                data = await remote_get_connections()
        except Exception:  # pragma: no cover - network failures
            return {}

        if agent_id and data is not None:
            return {agent_id: data}

        if isinstance(data, dict):
            if "connections" in data:
                conns = data["connections"]
            else:
                conns = data
            if isinstance(conns, list):
                return {str(cid): {} for cid in conns}
            return conns
        if isinstance(data, list):
            return {str(cid): {} for cid in data}
        return {}

    def _agent_to_schema(self, agent, connections: dict[str, dict]) -> AgentRead:
        agent_id_str = str(agent.agent_id)
        schema = AgentRead.model_validate(agent)
        schema.is_active = agent_id_str in connections
        schema.address = connections.get(agent_id_str, {}).get("address", "Unknown")
        return schema

    async def create_agent(self, agent_in: AgentCreate) -> AgentRead:
        """Create a new agent."""
        agent = await self.service.create(self.session, agent_in)
        connections = await self._get_connections()
        return self._agent_to_schema(agent, connections)

    async def get_agent(self, agent_id: uuid.UUID) -> AgentRead:
        """Retrieve a single agent."""
        agent = await self.service.get(self.session, agent_id)
        if agent is None:
            raise HTTPException(status_code=404, detail="Agent not found")
        connections = await self._get_connections(str(agent_id))
        return self._agent_to_schema(agent, connections)

    async def list_agents(self) -> List[AgentRead]:
        """Return all agents."""
        agents = await self.service.list(self.session)
        connections = await self._get_connections()
        return [self._agent_to_schema(a, connections) for a in agents]

    async def update_agent(
        self, agent_id: uuid.UUID, agent_in: AgentUpdate
    ) -> AgentRead:
        """Update an agent's data."""
        agent = await self.service.get(self.session, agent_id)
        if agent is None:
            raise HTTPException(status_code=404, detail="Agent not found")
        agent = await self.service.update(self.session, agent, agent_in)
        connections = await self._get_connections()
        return self._agent_to_schema(agent, connections)

    async def delete_agent(self, agent_id: uuid.UUID) -> Deleted:
        """Delete an agent."""
        agent = await self.service.get(self.session, agent_id)
        if agent is None:
            raise HTTPException(status_code=404, detail="Agent not found")
        await self.service.delete(self.session, agent)
        return Deleted()
