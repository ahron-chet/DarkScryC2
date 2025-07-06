import os

os.environ.setdefault(
    "MANAGEMENT_DATABASE_URL", "postgresql+asyncpg://user:pass@localhost/db"
)
os.environ.setdefault("MANAGEMENT_SECRET_KEY", "secret")

import pytest
from fastapi import HTTPException

from Management.app.core.security import create_access_token, required_role
from Management.app.models.user import User, UserRole


def test_create_access_token():
    token = create_access_token({"sub": 1})
    assert isinstance(token, str)
    assert token


@pytest.mark.asyncio
async def test_required_role():
    user = User(id=1, username="u", password="p", role=UserRole.ADMIN.value)
    dep = required_role(UserRole.ADMIN)
    assert await dep(user=user) is user


@pytest.mark.asyncio
async def test_required_role_forbidden():
    user = User(id=1, username="u", password="p", role=UserRole.READER.value)
    dep = required_role(UserRole.ADMIN)
    with pytest.raises(HTTPException):
        await dep(user=user)
