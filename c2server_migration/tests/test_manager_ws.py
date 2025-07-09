import os
import sys

from fastapi.testclient import TestClient

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
os.environ.setdefault("C2_SERVER_HOST", "127.0.0.1")
os.environ.setdefault("C2_SERVER_PORT", "9100")
os.environ.setdefault("C2_SERVER_REDIS_URL", "redis://localhost")

from darkscryc2server.api.app import app


class DummyConn:
    async def send_and_receive(self, msg: str) -> str:
        return "ok:" + msg


class DummyManager:
    def __init__(self):
        self.connections = {"agent1": DummyConn()}

    def get(self, id_):
        return self.connections.get(id_)

    def list_all(self):
        return self.connections


def override_manager() -> DummyManager:
    return DummyManager()


from darkscryc2server.core.connection import ConnectionManager


def test_manager_ws_get_connections():
    app.dependency_overrides[ConnectionManager] = override_manager
    client = TestClient(app)
    with client.websocket_connect("/manager_ws") as ws:
        ws.send_json({"action": "get_connections"})
        resp = ws.receive_json()
        assert resp["success"]
        assert "agent1" in resp["data"]["connections"]

        ws.send_json({"action": "send_command", "conn_id": "agent1", "command": "cmd"})
        resp2 = ws.receive_json()
        assert resp2["data"]["result"] == "ok:cmd"
    app.dependency_overrides.clear()
