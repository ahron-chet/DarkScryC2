

from darkscryc2server.Models.ModulesSchemas import GenAction
from darkscryc2server.Models.schemas import CommandIdentifiers
from darkscryc2server.Models.remote_tools_schemas import ManagerResponse

from application.services.view_base import ApiRouteV2


from application.Utils.arq_tasks_utils import get_task_executor
from uuid import UUID


from ninja import Schema, Field

class TaskOut(Schema):
    """
    Schema to represent a task with its unique identifier.
    """
    task_id: UUID = Field(..., description="The unique identifier for the task.")


class MashineCollection(ApiRouteV2):
    def __init__(self, tags = ['Collection']):
        super().__init__(tags)
        self.register_routes()

    
    async def fetch_basic(self, request, agent_id:UUID, *args, **kwargs):
        payload = GenAction(action=CommandIdentifiers.GET_BASIC_MACHINE_INFO).xml()
        task_excutor = await get_task_executor()
        job = await task_excutor.enqueue_job(
            "remote_send_command_task",
            agent_id=str(agent_id), 
            command=payload,
            _action_name=CommandIdentifiers.GET_BASIC_MACHINE_INFO
        )
        return TaskOut(task_id=job.job_id)

    
    def register_routes(self):
        return self.register_route(
            path="/{agent_id}", 
            methods=["GET"], 
            view_func=self.fetch_basic, 
            response={200:TaskOut},
            summary="Fetsh basic machine ibfo"
        )