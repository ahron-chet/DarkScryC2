from __future__ import annotations

import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi_utils.cbv import cbv

from ..controllers.user_controller import UserController
from ..core.security import get_current_user, required_role
from ..models.user import UserRole
from ..schemas.user import Deleted, UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@cbv(router)
class UserRoutes(UserController):
    """CRUD routes for managing users."""

    @router.post(
        "/",
        response_model=UserRead,
        status_code=status.HTTP_201_CREATED,
        dependencies=[Depends(required_role(UserRole.ADMIN))],
    )
    async def create(self, user_in: UserCreate) -> UserRead:
        return await self.create_user(user_in)

    @router.get(
        "/",
        response_model=List[UserRead],
        dependencies=[Depends(get_current_user)],
    )
    async def list(self) -> List[UserRead]:
        return await self.list_users()

    @router.get(
        "/{user_id}",
        response_model=UserRead,
        dependencies=[Depends(get_current_user)],
    )
    async def read(self, user_id: uuid.UUID) -> UserRead:
        return await self.get_user(user_id)

    @router.put(
        "/{user_id}",
        response_model=UserRead,
        dependencies=[Depends(required_role(UserRole.ADMIN))],
    )
    async def update(self, user_id: uuid.UUID, user_in: UserUpdate) -> UserRead:
        return await self.update_user(user_id, user_in)

    @router.delete(
        "/{user_id}",
        response_model=Deleted,
        dependencies=[Depends(required_role(UserRole.ADMIN))],
    )
    async def delete(self, user_id: uuid.UUID) -> Deleted:
        return await self.delete_user(user_id)
