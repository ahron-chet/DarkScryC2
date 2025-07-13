import uuid

from fastapi import Depends

from ...schemas.modules.collection import (
    FileCollectionRequest,
    UploadBase64FileRequest,
)
from ...schemas.tasks import TaskOut
from ...services.modules.collection import CollectionService


class CollectionController:
    """Controller for collection module operations."""

    service: CollectionService = Depends(CollectionService)

    async def basic_machine_info_job(self, agent_id: uuid.UUID) -> TaskOut:
        job_id = await self.service.basic_machine_info_task(agent_id)
        return TaskOut(task_id=job_id)

    async def stream_directory_job(
        self, agent_id: uuid.UUID, payload: FileCollectionRequest
    ) -> TaskOut:
        job_id = await self.service.stream_directory_task(agent_id, payload.path)
        return TaskOut(task_id=job_id)

    async def get_file_base64_job(
        self, agent_id: uuid.UUID, payload: FileCollectionRequest
    ) -> TaskOut:
        job_id = await self.service.get_file_base64_task(agent_id, payload.path)
        return TaskOut(task_id=job_id)

    async def upload_file_base64_job(
        self, agent_id: uuid.UUID, payload: UploadBase64FileRequest
    ) -> TaskOut:
        job_id = await self.service.upload_file_base64_task(
            agent_id,
            payload.path,
            payload.file_base64,
            payload.file_name,
        )
        return TaskOut(task_id=job_id)

    async def wifi_basic_info_job(self, agent_id: uuid.UUID) -> TaskOut:
        job_id = await self.service.wifi_basic_info_task(agent_id)
        return TaskOut(task_id=job_id)

    async def enumerate_processes_job(self, agent_id: uuid.UUID) -> TaskOut:
        job_id = await self.service.enumerate_processes_task(agent_id)
        return TaskOut(task_id=job_id)
