import pytest
from app.models.user import UserRole
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


def _auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


async def test_operator_can_manage_agents(
    client: AsyncClient, create_test_user, get_token, monkeypatch
):
    await create_test_user("admin", UserRole.ADMIN)
    await create_test_user("op", UserRole.OPERATOR)
    admin_token = await get_token("admin")
    op_token = await get_token("op")

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
        json={"host_name": "host1", "os": "linux"},
        headers=_auth(op_token),
    )
    assert resp.status_code == 201
    agent_id = resp.json()["agent_id"]

    resp = await client.get(f"/agents/{agent_id}", headers=_auth(op_token))
    assert resp.status_code == 200
    assert "is_active" in resp.json()
    assert "address" in resp.json()

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
