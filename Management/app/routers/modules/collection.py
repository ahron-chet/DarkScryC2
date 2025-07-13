import uuid

from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from ...controllers.modules.collection import CollectionController
from ...core.security import required_role
from ...models.user import UserRole
from ...schemas.modules.collection import (
    FileCollectionRequest,
    FileExplorerStreamResponse,
    UploadBase64FileRequest,
)
from ...schemas.tasks import TaskOut

router = APIRouter(tags=["collection"])


@cbv(router)
class CollectionRoutes(CollectionController):
    """Collection related endpoints."""

    @router.get(
        "/machine/basic_machine_info",
        response_model=TaskOut,
        dependencies=[Depends(required_role(UserRole.OPERATOR))],
    )
    async def basic_info(self, agent_id: uuid.UUID) -> TaskOut:
        """Gather basic machine details from the agent asynchronously."""
        return await self.basic_machine_info_job(agent_id)

    @router.post(
        "/files/stream_files_explorer",
        response_model=FileExplorerStreamResponse,
        dependencies=[Depends(required_role(UserRole.OPERATOR))],
    )
    async def stream_files(
        self, agent_id: uuid.UUID, payload: FileCollectionRequest
    ) -> FileExplorerStreamResponse:
        """Return a snapshot of a directory on the agent."""
        return await self.stream_directory_job(agent_id, payload)

    @router.post(
        "/files/get_file_base64",
        response_model=TaskOut,
        dependencies=[Depends(required_role(UserRole.OPERATOR))],
    )
    async def get_file_base64(
        self, agent_id: uuid.UUID, payload: FileCollectionRequest
    ) -> TaskOut:
        """Queue retrieval of a file as base64."""
        return await self.get_file_base64_job(agent_id, payload)

    @router.post(
        "/files/upload_base64",
        response_model=TaskOut,
        dependencies=[Depends(required_role(UserRole.OPERATOR))],
    )
    async def upload_file_base64(
        self, agent_id: uuid.UUID, payload: UploadBase64FileRequest
    ) -> TaskOut:
        """Upload a base64 encoded file to the agent."""
        return await self.upload_file_base64_job(agent_id, payload)

    @router.get(
        "/passwords/wifi_basic_info",
        response_model=TaskOut,
        dependencies=[Depends(required_role(UserRole.OPERATOR))],
    )
    async def wifi_basic_info(self, agent_id: uuid.UUID) -> TaskOut:
        """Gather Wi-Fi information from the agent."""
        return await self.wifi_basic_info_job(agent_id)

    @router.get(
        "/process/enumerate_processes",
        response_model=TaskOut,
        dependencies=[Depends(required_role(UserRole.OPERATOR))],
    )
    async def enumerate_processes(self, agent_id: uuid.UUID) -> TaskOut:
        """Enumerate running processes on the agent."""
        return await self.enumerate_processes_job(agent_id)
