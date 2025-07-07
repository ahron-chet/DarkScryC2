import pytest
from httpx import AsyncClient

from app.schemas.user import UserCreate, UserRole
from app.services.user_service import UserService

pytestmark = pytest.mark.anyio


async def test_auth_flow(client: AsyncClient, db_session):
    service = UserService()
    await service.create(
        db_session,
        UserCreate(
            username="admin",
            password="Str0ng!Pass",
            email="admin@example.com",
            role=UserRole.ADMIN,
        ),
    )

    resp = await client.post(
        "/auth/login",
        json={"username": "admin", "password": "Str0ng!Pass"},
    )
    assert resp.status_code == 200
    tokens = resp.json()
    assert tokens["access_token"]
    assert tokens["refresh_token"]

    refresh = await client.post(
        "/auth/refresh", json={"refresh_token": tokens["refresh_token"]}
    )
    assert refresh.status_code == 200
    new_access = refresh.json()["access_token"]

    headers = {"Authorization": f"Bearer {new_access}"}
    resp2 = await client.get("/users/", headers=headers)
    assert resp2.status_code == 200


async def test_protected_endpoint_requires_auth(client: AsyncClient):
    resp = await client.get("/users/")
    assert resp.status_code == 403


async def test_inactive_user_token_forbidden(client: AsyncClient, db_session):
    service = UserService()
    user = await service.create(
        db_session,
        UserCreate(
            username="inactive",
            password="Str0ng!Pass",
            email="inactive@example.com",
            role=UserRole.ADMIN,
        ),
    )

    login = await client.post(
        "/auth/login",
        json={"username": "inactive", "password": "Str0ng!Pass"},
    )
    token = login.json()["access_token"]

    user.is_active = False
    await db_session.commit()

    headers = {"Authorization": f"Bearer {token}"}
    resp = await client.get("/users/", headers=headers)
    assert resp.status_code == 403
