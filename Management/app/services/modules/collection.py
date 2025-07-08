import uuid

from arq.jobs import Job
from darkscryc2server.Models.ModulesSchemas import GenAction
from darkscryc2server.Models.remote_tools_schemas import ManagerResponse
from darkscryc2server.Models.schemas import CommandIdentifiers
from darkscryc2server.Utils.remote_utils.commands import remote_send_command

from ...utils.tasks import get_task_executor


class CollectionService:
    """Service layer for collection module interactions."""

    async def fetch_basic_machine_info(self, agent_id: uuid.UUID) -> ManagerResponse:
        payload = GenAction(
            action=CommandIdentifiers.GET_BASIC_MACHINE_INFO
        ).model_dump_json()
        return await remote_send_command(conn_id=str(agent_id), command=payload)

    async def basic_machine_info_task(self, agent_id: uuid.UUID) -> uuid.UUID:
        payload = GenAction(
            action=CommandIdentifiers.GET_BASIC_MACHINE_INFO
        ).model_dump_json()
        executor = await get_task_executor()
        job: Job = await executor.enqueue_job(
            "remote_send_command_task",
            agent_id=str(agent_id),
            command=payload,
            _action_name=CommandIdentifiers.GET_BASIC_MACHINE_INFO,
        )
        return uuid.UUID(job.job_id)
