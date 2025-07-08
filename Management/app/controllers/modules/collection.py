import uuid

from fastapi import Depends

from ...schemas.module import TaskOut
from ...services.modules.collection import CollectionService


class CollectionController:
    """Controller for collection module operations."""

    service: CollectionService = Depends(CollectionService)

    async def basic_machine_info_job(self, agent_id: uuid.UUID) -> TaskOut:
        job_id = await self.service.basic_machine_info_task(agent_id)
        return TaskOut(task_id=job_id)
