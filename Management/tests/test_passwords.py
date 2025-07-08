import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate, UserRole
from app.services.user_service import UserService

pytestmark = pytest.mark.anyio


async def test_password_complexity_validation(db_session: AsyncSession):
    service = UserService()
    weak_user = UserCreate(
        username="weak",
        password="password",
        email="weak@example.com",
        role=UserRole.ADMIN,
    )
    with pytest.raises(ValueError):
        await service.create(db_session, weak_user)
