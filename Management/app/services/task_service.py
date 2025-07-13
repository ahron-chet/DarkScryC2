import uuid

from app.schemas.tasks import TaskResultOut
from app.utils.tasks import get_task_executor
from arq.jobs import Job, JobStatus
from darkscryc2server.models.messages import CommandIdentifiers


class TaskService:
    """Service for retrieving and managing background tasks."""

    async def get_status(self, task_id: uuid.UUID) -> JobStatus:
        redis = await get_task_executor()
        job = Job(task_id.hex, redis)
        return await job.status()

    async def get_result(self, task_id: uuid.UUID) -> TaskResultOut:
        redis = await get_task_executor()
        job = Job(task_id.hex, redis)
        info = await job.result_info()

        result = (
            info.result if not isinstance(info.result, Exception) else str(info.result)
        )
        action = info.kwargs.get("_action_name")
        if isinstance(action, CommandIdentifiers):
            action = action
        else:
            action = None

        return TaskResultOut(
            success=info.success,
            result=result,
            start_time=info.start_time,
            finish_time=info.finish_time,
            action=action,
            job_id=task_id,
        )

    async def revoke_task(self, task_id: uuid.UUID) -> None:
        redis = await get_task_executor()
        job = Job(task_id.hex, redis)
        await job.abort()

    async def delete_task(self, task_id: uuid.UUID) -> None:
        redis = await get_task_executor()
        job = Job(task_id.hex, redis)
        await job.delete()
