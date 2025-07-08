from __future__ import annotations

import uuid

from darkscryc2server.Models.remote_tools_schemas import ManagerResponse
from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from ...controllers.modules.execution import ExecutionController
from ...core.security import required_role
from ...models.user import UserRole
from ...schemas.module import RunCommandIn, TaskOut

router = APIRouter()


@cbv(router)
class ExecutionRoutes(ExecutionController):
    """Execution related endpoints."""

    @router.get(
        "/shell/start_shell",
        response_model=TaskOut,
        dependencies=[Depends(required_role(UserRole.OPERATOR))],
    )
    async def start_shell(self, agent_id: uuid.UUID) -> TaskOut:
        """Start an interactive shell session on the specified agent."""
        return await self.start_shell_job(agent_id)

    @router.post(
        "/shell/run_command_task",
        response_model=TaskOut,
        dependencies=[Depends(required_role(UserRole.OPERATOR))],
    )
    async def run_command_task(
        self, agent_id: uuid.UUID, payload: RunCommandIn
    ) -> TaskOut:
        """Queue a shell command to run asynchronously on the agent."""
        return await self.run_command_job(agent_id, payload)

    @router.post(
        "/shell/run_command",
        response_model=ManagerResponse,
        dependencies=[Depends(required_role(UserRole.OPERATOR))],
    )
    async def run_command(
        self, agent_id: uuid.UUID, payload: RunCommandIn
    ) -> ManagerResponse:
        """Execute a shell command immediately and return its output."""
        return await self.execute_command(agent_id, payload)
