import pytest
from httpx import AsyncClient

from app.models.user import UserRole

pytestmark = pytest.mark.anyio


def _auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


async def test_operator_can_manage_agents(
    client: AsyncClient, create_test_user, get_token
):
    await create_test_user("admin", UserRole.ADMIN)
    await create_test_user("op", UserRole.OPERATOR)
    admin_token = await get_token("admin")
    op_token = await get_token("op")

    resp = await client.post(
        "/agents/",
        json={"host_name": "host1", "os": "linux"},
        headers=_auth(op_token),
    )
    assert resp.status_code == 201
    agent_id = resp.json()["agent_id"]

    resp = await client.get(f"/agents/{agent_id}", headers=_auth(op_token))
    assert resp.status_code == 200

    resp = await client.put(
        f"/agents/{agent_id}",
        json={"host_name": "host2"},
        headers=_auth(op_token),
    )
    assert resp.status_code == 200
    assert resp.json()["host_name"] == "host2"

    resp = await client.delete(f"/agents/{agent_id}", headers=_auth(admin_token))
    assert resp.status_code == 200
    resp = await client.get(f"/agents/{agent_id}", headers=_auth(op_token))
    assert resp.status_code == 404


async def test_reader_cannot_create_agent(
    client: AsyncClient, create_test_user, get_token
):
    await create_test_user("op", UserRole.OPERATOR)
    await create_test_user("reader", UserRole.READER)
    reader_token = await get_token("reader")

    resp = await client.post(
        "/agents/",
        json={"host_name": "bad", "os": "linux"},
        headers=_auth(reader_token),
    )
    assert resp.status_code == 403
