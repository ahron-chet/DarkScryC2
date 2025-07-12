import uuid
from app.schemas.modules.execution import StartShellCommand, RunCommand

from darkscryc2server.models.messages import AgentResponse
from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from ...controllers.modules.execution import ExecutionController
from ...core.security import required_role
from ...models.user import UserRole
from ...schemas.tasks import TaskOut

router = APIRouter(tags=["execution"])


@cbv(router)
class ExecutionRoutes(ExecutionController):
    """Execution related endpoints."""

    @router.post(
        "/shell/start_shell",
        response_model=TaskOut,
        dependencies=[Depends(required_role(UserRole.OPERATOR))],
    )
    async def start_shell(self, agent_id: uuid.UUID, command: StartShellCommand) -> TaskOut:
        """Start an interactive shell session on the specified agent."""
        return await self.start_shell_task(agent_id, command)

    @router.post(
        "/shell/run_command_task",
        response_model=TaskOut,
        dependencies=[Depends(required_role(UserRole.OPERATOR))],
    )
    async def run_command_job(
        self, agent_id: uuid.UUID, command: RunCommand
    ) -> TaskOut:
        """Queue a shell command to run asynchronously on the agent."""
        return await self.run_command_task(agent_id, command)

    @router.post(
        "/shell/run_command",
        response_model=AgentResponse,
        dependencies=[Depends(required_role(UserRole.OPERATOR))],
    )
    async def run_command_stream(
        self, agent_id: uuid.UUID, command: RunCommand
    ) -> AgentResponse:
        """Execute a shell command immediately and return its output."""
        return await self.run_command(agent_id, command)
