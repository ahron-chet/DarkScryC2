import pytest
from httpx import AsyncClient

from app.schemas.user import UserCreate, UserRole
from app.services.user_service import UserService

pytestmark = pytest.mark.anyio


async def test_agent_routes_crud_and_permissions(client: AsyncClient, db_session):
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
    await service.create(
        db_session,
        UserCreate(
            username="reader",
            password="Str0ng!Pass",
            email="reader@example.com",
            role=UserRole.READER,
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
    reader_token = (
        await client.post(
            "/auth/login", json={"username": "reader", "password": "Str0ng!Pass"}
        )
    ).json()["access_token"]

    headers_admin = {"Authorization": f"Bearer {admin_token}"}
    headers_op = {"Authorization": f"Bearer {op_token}"}
    headers_reader = {"Authorization": f"Bearer {reader_token}"}

    resp = await client.post(
        "/agents/",
        json={"host_name": "host1", "os": "linux"},
        headers=headers_op,
    )
    assert resp.status_code == 201
    agent_id = resp.json()["agent_id"]

    resp = await client.post(
        "/agents/",
        json={"host_name": "bad", "os": "linux"},
        headers=headers_reader,
    )
    assert resp.status_code == 403

    resp = await client.get("/agents/", headers=headers_op)
    assert resp.status_code == 200

    resp = await client.get(f"/agents/{agent_id}", headers=headers_op)
    assert resp.status_code == 200

    resp = await client.put(
        f"/agents/{agent_id}",
        json={"host_name": "host2"},
        headers=headers_op,
    )
    assert resp.status_code == 200
    assert resp.json()["host_name"] == "host2"

    resp = await client.delete(f"/agents/{agent_id}", headers=headers_admin)
    assert resp.status_code == 200
