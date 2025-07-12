import pytest
from app.models.user import UserRole
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


async def _create_reader(client: AsyncClient, admin_token: str) -> str:
    headers = {"Authorization": f"Bearer {admin_token}"}
    resp = await client.post(
        "/users/",
        json={
            "username": "reader",
            "password": "Str0ng!Pass",
            "email": "reader@example.com",
            "role": "reader",
        },
        headers=headers,
    )
    assert resp.status_code == 201
    return resp.json()["user_id"]


def _auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


async def test_admin_can_crud_user(client: AsyncClient, create_test_user, get_token):
    await create_test_user("admin", UserRole.ADMIN)
    admin_token = await get_token("admin")

    user_id = await _create_reader(client, admin_token)

    resp = await client.get("/users/", headers=_auth_header(admin_token))
    assert resp.status_code == 200
    assert any(u["user_id"] == user_id for u in resp.json())

    resp = await client.get(f"/users/{user_id}", headers=_auth_header(admin_token))
    assert resp.status_code == 200

    resp = await client.put(
        f"/users/{user_id}",
        json={"first_name": "Updated"},
        headers=_auth_header(admin_token),
    )
    assert resp.status_code == 200
    assert resp.json()["first_name"] == "Updated"

    resp = await client.delete(f"/users/{user_id}", headers=_auth_header(admin_token))
    assert resp.status_code == 200
    resp = await client.get(f"/users/{user_id}", headers=_auth_header(admin_token))
    assert resp.status_code == 404


async def test_operator_cannot_create_user(
    client: AsyncClient, create_test_user, get_token
):
    await create_test_user("admin", UserRole.ADMIN)
    await create_test_user("op", UserRole.OPERATOR)
    op_token = await get_token("op")

    resp = await client.post(
        "/users/",
        json={
            "username": "bad",
            "password": "Str0ng!Pass",
            "email": "bad@example.com",
            "role": "reader",
        },
        headers=_auth_header(op_token),
    )
    assert resp.status_code == 403


async def test_user_can_update_self(client: AsyncClient, create_test_user, get_token):
    await create_test_user("admin", UserRole.ADMIN)
    await create_test_user("reader", UserRole.READER)
    reader_token = await get_token("reader")

    resp = await client.put(
        "/users/me",
        json={"first_name": "Self"},
        headers=_auth_header(reader_token),
    )
    assert resp.status_code == 200
    assert resp.json()["first_name"] == "Self"


async def test_user_cannot_update_other_user(
    client: AsyncClient, create_test_user, get_token
):
    await create_test_user("admin", UserRole.ADMIN)
    await create_test_user("reader", UserRole.READER)
    admin_token = await get_token("admin")
    reader_token = await get_token("reader")

    admin_list = await client.get("/users/", headers=_auth_header(admin_token))
    admin_id = next(u["user_id"] for u in admin_list.json() if u["username"] == "admin")
    resp = await client.put(
        f"/users/{admin_id}",
        json={"first_name": "Bad"},
        headers=_auth_header(reader_token),
    )
    assert resp.status_code == 403


async def test_admin_token_allows_operator_routes(
    client: AsyncClient, create_test_user, get_token, monkeypatch
):
    await create_test_user("admin", UserRole.ADMIN)
    admin_token = await get_token("admin")

    async def fake_get_connections():
        return []

    async def fake_get_connection(agent_id: str):
        return {}

    monkeypatch.setattr(
        "app.controllers.agent_controller.remote_get_connections",
        fake_get_connections,
    )
    monkeypatch.setattr(
        "app.controllers.agent_controller.remote_get_connection",
        fake_get_connection,
    )

    resp = await client.post(
        "/agents/",
        json={"host_name": "adminhost", "os": "linux"},
        headers=_auth_header(admin_token),
    )
    assert resp.status_code == 201
