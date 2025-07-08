import uuid

from arq.jobs import Job
from darkscryc2server.Models.ModulesSchemas.Execution import (
    RunCommand,
    StartShellCommand,
)
from darkscryc2server.Models.remote_tools_schemas import ManagerResponse
from darkscryc2server.Models.schemas import CommandIdentifiers
from darkscryc2server.Utils.remote_utils.commands import remote_send_command

from ...utils.tasks import get_task_executor


class ExecutionService:
    """Service layer for execution module interactions."""

    async def start_shell(self, agent_id: uuid.UUID) -> ManagerResponse:
        command = StartShellCommand().model_dump_json()
        return await remote_send_command(conn_id=str(agent_id), command=command)

    async def run_command(self, agent_id: uuid.UUID, command: str) -> ManagerResponse:
        payload = RunCommand(command=command).model_dump_json()
        return await remote_send_command(conn_id=str(agent_id), command=payload)

    async def start_shell_task(self, agent_id: uuid.UUID) -> uuid.UUID:
        command = StartShellCommand().model_dump_json()
        executor = await get_task_executor()
        job: Job = await executor.enqueue_job(
            "remote_send_command_task",
            agent_id=str(agent_id),
            command=command,
            _action_name=CommandIdentifiers.START_SHELL_INSTANCE,
        )
        return uuid.UUID(job.job_id)

    async def run_command_task(self, agent_id: uuid.UUID, command: str) -> uuid.UUID:
        payload = RunCommand(command=command).model_dump_json()
        executor = await get_task_executor()
        job: Job = await executor.enqueue_job(
            "remote_send_command_task",
            agent_id=str(agent_id),
            command=payload,
            _action_name=CommandIdentifiers.RUN_COMMAND,
        )
        return uuid.UUID(job.job_id)
