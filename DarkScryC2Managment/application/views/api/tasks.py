from uuid import UUID
from arq.jobs import Job
from application.Utils.arq_tasks_utils import get_task_executor

from darkscryc2server.Models.schemas import CommandIdentifiersName, CommandIdentifiers
from application.views.api.Schemas.general import TaskResultOut, TaskStatusOut, DeletedSuccessfully
from ...services.view_base import ApiRouteV2


class TaskApi(ApiRouteV2):
    def __init__(self):
        super().__init__(tags=["Task"])
        self.register_routes()

    async def get_task_status(self, request, task_id: UUID):
        redis = await get_task_executor()
        job = Job(task_id.hex, redis)
        status = await job.status()
        return TaskStatusOut(status=status, job_id=task_id)
    
    async def get_task_results(self, request, task_id: UUID):
        redis = await get_task_executor()
        job = Job(task_id.hex, redis)
        info = await job.result_info()

        if isinstance(info.result, Exception):
            result = str(info.result)
        else:
            result = info.result

        act = info.kwargs.get("_action_name", CommandIdentifiersName.UNKNOW)
        if isinstance(act, CommandIdentifiers):
            act = CommandIdentifiersName(act.name)
        else:
            act = CommandIdentifiersName.UNKNOW

        return TaskResultOut(
            success=info.success,
            result=result,
            start_time=info.start_time,
            finish_time=info.finish_time,
            queue_name=info.queue_name,
            job_id=task_id,
            action=act
        )

    async def revoke_task(self, request, task_id: UUID):
        """
        Attempt to stop a running task if it's in progress (arq 'abort').
        If the task is already finished, abort() does nothing.
        """
        redis = await get_task_executor()
        job = Job(task_id.hex, redis)
        # If job doesn't exist, job.status() might return None or raise an error
        await job.abort()  # stops the job if still active
        return {"detail": f"Task {task_id} was revoked (if it was running)."}

    async def delete_task(self, request, task_id: UUID):
        """
        Remove the job data from redis (arq 'delete').
        This only succeeds if the job is completed or aborted.
        """
        redis = await get_task_executor()
        job = Job(task_id.hex, redis)
        # If job isn't finished or doesn't exist, this might fail
        await job.delete()
        return DeletedSuccessfully(detail=f"Task {task_id} deleted successfully")

    def register_routes(self):
        self.register_route(
            path="/{task_id}/result",
            methods=["GET"],
            view_func=self.get_task_results,
            response={200: TaskResultOut},
            summary="Get task result"
        )
        self.register_route(
            path="/{task_id}/status",
            methods=["GET"],
            view_func=self.get_task_status,
            response={200: TaskStatusOut},
            summary="Check task status"
        )
        self.register_route(
            path="/{task_id}/revoke",
            methods=["PUT"],
            view_func=self.revoke_task,
            summary="Revoke a running task (if in progress)"
        )
        self.register_route(
            path="/{task_id}",
            methods=["DELETE"],
            view_func=self.delete_task,
            response={200: DeletedSuccessfully},
            summary="Delete a completed/aborted task from redis"
        )
