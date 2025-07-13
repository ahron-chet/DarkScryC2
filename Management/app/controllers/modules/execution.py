import uuid

from app.schemas.modules.execution import RunCommand, StartShellCommand
from darkscryc2server.models.messages import AgentResponse
from fastapi import Depends

from ...schemas.tasks import TaskOut
from ...services.modules.execution import ExecutionService


class ExecutionController:
    """Controller for execution module operations."""

    service: ExecutionService = Depends(ExecutionService)

    async def start_shell_task(
        self, agent_id: uuid.UUID, command: StartShellCommand
    ) -> TaskOut:
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
