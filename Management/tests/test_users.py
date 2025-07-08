import pytest
from httpx import AsyncClient

from app.models.user import UserRole

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
