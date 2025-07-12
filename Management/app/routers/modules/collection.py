
import uuid

from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from ...controllers.modules.collection import CollectionController
from ...core.security import required_role
from ...models.user import UserRole
from ...schemas.tasks import TaskOut

router = APIRouter()


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
