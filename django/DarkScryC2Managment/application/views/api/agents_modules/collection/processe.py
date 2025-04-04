from uuid import UUID
from darkscryc2server.Models.schemas import GenAction
from application.services.view_base import ApiRouteV2
from darkscryc2server.Models.schemas import CommandIdentifiers
from django.shortcuts import aget_object_or_404
from application.models import Agent
from application.views.api.Schemas.general import TaskOut
from application.shortcuts import make_task

prefix_with_agent = "/agents/{agent_id}/modules/collection/process"
class ProcessCollection(ApiRouteV2):
    def __init__(self, tags = ['Collection']):
        super().__init__(tags=tags, prefix=prefix_with_agent)
        self.register_routes()

    
    async def enumerate_processes(self, request, agent_id:UUID, *args, **kwargs):
        agent = await aget_object_or_404(Agent, AgentId=agent_id)
        command = GenAction(action=CommandIdentifiers.ENUMERATE_PROCESSES).xml()
        job = await make_task(
            "remote_send_command_task",
            agent_id=str(agent.AgentId),
            command=command,
            _action_name=CommandIdentifiers.ENUMERATE_PROCESSES
        )
        return TaskOut(task_id=job.job_id)

    
    def register_routes(self):
        self.register_route(
            path="/enumerate_processes", 
            methods=["GET"], 
            view_func=self.enumerate_processes, 
            response={200:TaskOut},
            summary="Fetsh basic machine ibfo"
        )
