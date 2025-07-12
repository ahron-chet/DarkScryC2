import uuid

from fastapi import Depends

from app.schemas.tasks import TaskResultOut, TaskStatusOut
from app.schemas.user import Deleted
from app.services.task_service import TaskService


class TaskController:
    """Controller for background task management."""

    service: TaskService = Depends(TaskService)

    async def get_task_status(self, task_id: uuid.UUID) -> TaskStatusOut:
        status = await self.service.get_status(task_id)
        return TaskStatusOut(status=status, job_id=task_id)

    async def get_task_result(self, task_id: uuid.UUID) -> TaskResultOut:
        return await self.service.get_result(task_id)

    async def revoke_task(self, task_id: uuid.UUID) -> Deleted:
        await self.service.revoke_task(task_id)
        return Deleted(detail=f"Task {task_id} was revoked (if it was running).")

    async def delete_task(self, task_id: uuid.UUID) -> Deleted:
        await self.service.delete_task(task_id)
        return Deleted(detail=f"Task {task_id} deleted successfully")
