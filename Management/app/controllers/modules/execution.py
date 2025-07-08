import uuid

from darkscryc2server.Models.remote_tools_schemas import ManagerResponse
from fastapi import Depends

from ...schemas.module import RunCommandIn, TaskOut
from ...services.modules.execution import ExecutionService


class ExecutionController:
    """Controller for execution module operations."""

    service: ExecutionService = Depends(ExecutionService)

    async def start_shell_job(self, agent_id: uuid.UUID) -> TaskOut:
        job_id = await self.service.start_shell_task(agent_id)
        return TaskOut(task_id=job_id)

    async def run_command_job(
        self, agent_id: uuid.UUID, payload: RunCommandIn
    ) -> TaskOut:
        job_id = await self.service.run_command_task(agent_id, payload.command)
        return TaskOut(task_id=job_id)

    async def execute_command(
        self, agent_id: uuid.UUID, payload: RunCommandIn
    ) -> ManagerResponse:
        return await self.service.run_command(agent_id, payload.command)
