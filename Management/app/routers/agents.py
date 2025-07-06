from __future__ import annotations

import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi_utils.cbv import cbv

from ..controllers.agent_controller import AgentController
from ..core.security import get_current_user, required_role
from ..models.user import UserRole
from ..schemas.agent import AgentCreate, AgentRead, AgentUpdate, Deleted

router = APIRouter(prefix="/agents", tags=["agents"])


@cbv(router)
class AgentRoutes(AgentController):
    """CRUD routes for managing agents."""

    @router.post(
        "/",
        response_model=AgentRead,
        status_code=status.HTTP_201_CREATED,
        dependencies=[Depends(required_role(UserRole.OPERATOR))],
    )
    async def create(self, agent_in: AgentCreate) -> AgentRead:
        return await self.create_agent(agent_in)

    @router.get(
        "/",
        response_model=List[AgentRead],
        dependencies=[Depends(get_current_user)],
    )
    async def list(self) -> List[AgentRead]:
        return await self.list_agents()

    @router.get(
        "/{agent_id}",
        response_model=AgentRead,
        dependencies=[Depends(get_current_user)],
    )
    async def read(self, agent_id: uuid.UUID) -> AgentRead:
        return await self.get_agent(agent_id)

    @router.put(
        "/{agent_id}",
        response_model=AgentRead,
        dependencies=[Depends(required_role(UserRole.OPERATOR))],
    )
    async def update(self, agent_id: uuid.UUID, agent_in: AgentUpdate) -> AgentRead:
        return await self.update_agent(agent_id, agent_in)

    @router.delete(
        "/{agent_id}",
        response_model=Deleted,
        dependencies=[Depends(required_role(UserRole.ADMIN))],
    )
    async def delete(self, agent_id: uuid.UUID) -> Deleted:
        return await self.delete_agent(agent_id)
