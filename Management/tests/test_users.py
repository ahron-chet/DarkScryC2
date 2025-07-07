import pytest
from httpx import AsyncClient

from app.schemas.user import UserCreate, UserRole
from app.services.user_service import UserService

pytestmark = pytest.mark.anyio


async def test_user_routes_crud_and_permissions(client: AsyncClient, db_session):
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
    await service.create(
        db_session,
        UserCreate(
            username="op",
            password="Str0ng!Pass",
            email="op@example.com",
            role=UserRole.OPERATOR,
        ),
    )

    admin_token = (
        await client.post(
            "/auth/login", json={"username": "admin", "password": "Str0ng!Pass"}
        )
    ).json()["access_token"]
    op_token = (
        await client.post(
            "/auth/login", json={"username": "op", "password": "Str0ng!Pass"}
        )
    ).json()["access_token"]

    headers_admin = {"Authorization": f"Bearer {admin_token}"}
    headers_op = {"Authorization": f"Bearer {op_token}"}

    resp = await client.post(
        "/users/",
        json={
            "username": "reader",
            "password": "Str0ng!Pass",
            "email": "reader@example.com",
            "role": "reader",
        },
        headers=headers_admin,
    )
    assert resp.status_code == 201
    user_id = resp.json()["user_id"]

    resp = await client.post(
        "/users/",
        json={
            "username": "bad",
            "password": "Str0ng!Pass",
            "email": "bad@example.com",
            "role": "reader",
        },
        headers=headers_op,
    )
    assert resp.status_code == 403

    resp = await client.get("/users/", headers=headers_admin)
    assert resp.status_code == 200

    resp = await client.get(f"/users/{user_id}", headers=headers_admin)
    assert resp.status_code == 200

    resp = await client.put(
        f"/users/{user_id}",
        json={"first_name": "Updated"},
        headers=headers_admin,
    )
    assert resp.status_code == 200
    assert resp.json()["first_name"] == "Updated"

    resp = await client.delete(f"/users/{user_id}", headers=headers_admin)
    assert resp.status_code == 200
