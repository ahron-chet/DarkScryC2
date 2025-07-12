import os
import sys

from fastapi.testclient import TestClient

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
os.environ.setdefault("C2_SERVER_HOST", "127.0.0.1")
os.environ.setdefault("C2_SERVER_PORT", "9100")
os.environ.setdefault("C2_SERVER_REDIS_URL", "redis://localhost")

from darkscryc2server.api.app import app
from darkscryc2server.core.connection import ConnectionManager


class DummyConn:
    def __init__(self):
        self.address = ("10.0.0.1", 4444)


class DummyManager:
    def __init__(self):
        self.connections = {"agent1": DummyConn()}

    async def get(self, id_):
        return self.connections.get(id_)

    async def list_all(self):
        return self.connections


def override_manager() -> DummyManager:
    return DummyManager()


def test_get_single_connection():
    app.dependency_overrides[ConnectionManager] = override_manager
    app.state.conn_manager = override_manager()
    client = TestClient(app)

    resp = client.get("/connections/agent1")
    assert resp.status_code == 200
    data = resp.json()
    assert data["agent_id"] == "agent1"
    assert data["address"] == "('10.0.0.1', 4444)"

    resp2 = client.get("/connections/missing")
    assert resp2.status_code == 404

    app.dependency_overrides.clear()
    app.state.conn_manager = None
