import uuid
from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database import get_db
from ..schemas.user import Deleted, UserCreate, UserRead, UserUpdate
from ..services import UserService


class UserController:
    """Controller with common user operations."""

    session: AsyncSession = Depends(get_db)
    user_service: UserService = Depends(UserService)

    async def create_user(self, user_in: UserCreate) -> UserRead:
        """Create a new user."""
        user = await self.user_service.create(self.session, user_in)
        return UserRead.model_validate(user)

    async def get_user(self, user_id: uuid.UUID) -> UserRead:
        """Retrieve a single user."""
        user = await self.user_service.get(self.session, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return UserRead.model_validate(user)

    async def list_users(self) -> List[UserRead]:
        """Return all users."""
        users = await self.user_service.list(self.session)
        return [UserRead.model_validate(u) for u in users]

    async def update_user(self, user_id: uuid.UUID, user_in: UserUpdate) -> UserRead:
        """Update a user's data."""
        user = await self.user_service.get(self.session, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        user = await self.user_service.update(self.session, user, user_in)
        return UserRead.model_validate(user)

    async def delete_user(self, user_id: uuid.UUID) -> Deleted:
        """Delete a user."""
        user = await self.user_service.get(self.session, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        await self.user_service.delete(self.session, user)
        return Deleted()
