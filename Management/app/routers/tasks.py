from __future__ import annotations

import uuid

from app.controllers.task_controller import TaskController
from app.core.security import get_current_user, required_role
from app.models.user import UserRole
from app.schemas.tasks import TaskResultOut, TaskStatusOut
from app.schemas.user import Deleted
from fastapi import APIRouter, Depends
from fastapi import status as http_status
from fastapi_utils.cbv import cbv

router = APIRouter(
    prefix="/tasks", tags=["tasks"], dependencies=[Depends(get_current_user)]
)


@cbv(router)
class TaskRoutes(TaskController):
    """Routes for inspecting background tasks."""

    @router.get("/{task_id}/status", response_model=TaskStatusOut)
    async def status(self, task_id: uuid.UUID) -> TaskStatusOut:
        return await self.get_task_status(task_id)

    @router.get("/{task_id}/result", response_model=TaskResultOut)
    async def result(self, task_id: uuid.UUID) -> TaskResultOut:
        return await self.get_task_result(task_id)

    @router.put(
        "/{task_id}/revoke",
        response_model=Deleted,
        status_code=http_status.HTTP_200_OK,
        dependencies=[Depends(required_role(UserRole.OPERATOR))],
    )
    async def revoke(self, task_id: uuid.UUID) -> Deleted:
        return await self.revoke_task(task_id)

    @router.delete(
        "/{task_id}",
        response_model=Deleted,
        dependencies=[Depends(required_role(UserRole.ADMIN))],
    )
    async def delete(self, task_id: uuid.UUID) -> Deleted:
        return await self.delete_task(task_id)
