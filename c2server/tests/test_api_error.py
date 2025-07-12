import pytest
from fastapi.testclient import TestClient

from darkscryc2server.api.app import app
from darkscryc2server.core.connection import ConnectionManager


class EmptyManager(ConnectionManager):
    def __init__(self):
        pass

    async def get(self, id_):
        return None

    async def list_all(self):
        return {}


@pytest.fixture(autouse=True)
def _override():
    app.dependency_overrides[ConnectionManager] = EmptyManager
    app.state.conn_manager = EmptyManager()
    yield
    app.dependency_overrides.clear()
    app.state.conn_manager = None


def test_command_not_found():
    client = TestClient(app)
    resp = client.post(
        "/command/unknown",
        json={"command": {"text": "hi"}, "action_id": 2},
    )
    assert resp.status_code == 404


def test_health_endpoint():
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_manager_ws_invalid_requests():
    client = TestClient(app)
    with client.websocket_connect("/manager_ws") as ws:
        ws.send_text("notjson")
        resp = ws.receive_json()
        assert not resp["success"]
        ws.send_json({"action": "send_command", "conn_id": "none"})
        resp2 = ws.receive_json()
        assert not resp2["success"]
