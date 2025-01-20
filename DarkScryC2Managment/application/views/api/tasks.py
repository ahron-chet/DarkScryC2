

from ...services.view_base import ApiRouteV2
from application.Utils.arq_tasks_utils import get_task_executor

from arq.jobs import Job, JobStatus
# from DarkScryC2Managment.arq_worker import WorkerSettings
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Any
from darkscryc2server.Models.schemas import CommandIdentifiersName, CommandIdentifiers


class TaskStatusOut(BaseModel):
    """
    Schema to represent the current status of a task.
    """
    status: JobStatus = Field(..., description="The current status of the job.")
    job_id: UUID = Field(..., description="The unique identifier of the job.")


class TaskResultOut(BaseModel):
    """
    Schema to represent the result of a task.
    """
    success: bool = Field(..., description="Indicates whether the task completed successfully.")
    result: Any = Field(..., description="The result or output of the task. This can be of any type depending on the task.")
    start_time: datetime = Field(..., description="The timestamp when the task started.")
    finish_time: datetime = Field(..., description="The timestamp when the task finished.")
    action: CommandIdentifiersName = Field(..., description="The name identifier of the action the job was processed in.")
    job_id: UUID = Field(..., description="The unique identifier of the job.")
    

    model_config = ConfigDict(use_enum_values=True)


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
        