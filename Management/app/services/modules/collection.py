import uuid

from arq.jobs import Job
from darkscryc2server.models.messages import (
    CommandIdentifiers,
    AgentResponse
)

from ...utils.tasks import get_task_executor


class CollectionService:
    """Service layer for collection module interactions."""

    async def basic_machine_info_task(self, agent_id: uuid.UUID) -> uuid.UUID:
        executor = await get_task_executor()
        job: Job = await executor.enqueue_job(
            "remote_send_command_task",
            agent_id=str(agent_id),
            action_id=CommandIdentifiers.GET_BASIC_MACHINE_INFO
        )
        return uuid.UUID(job.job_id)
