import uuid

from fastapi import Depends

from ...schemas.tasks import TaskOut
from ...services.modules.execution import ExecutionService
from app.schemas.modules.execution import StartShellCommand, RunCommand

from darkscryc2server.models.messages import AgentResponse

class ExecutionController:
    """Controller for execution module operations."""

    service: ExecutionService = Depends(ExecutionService)

    async def start_shell_task(self, agent_id: uuid.UUID, command: StartShellCommand) -> TaskOut:
        job_id = await self.service.start_shell_task(agent_id=agent_id, command=command)
        return TaskOut(task_id=job_id)

    async def run_command_task(
        self, agent_id: uuid.UUID, command: RunCommand
    ) -> TaskOut:
        job_id = await self.service.run_command_task(agent_id, command)
        return TaskOut(task_id=job_id)

    async def run_command(
        self, agent_id: uuid.UUID, command: RunCommand
    ) -> AgentResponse:
        """Only run command donst need to specify task so it will be faster all other modul commands operation are needs to be tasks"""
        return await self.service.run_command(agent_id, command)
