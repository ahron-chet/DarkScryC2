import os
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
os.environ.setdefault("C2_SERVER_HOST", "127.0.0.1")
os.environ.setdefault("C2_SERVER_PORT", "9100")

from darkscryc2server.api.app import app


class DummyConn:
    def __init__(self):
        self.sent = None

    async def send_and_receive(self, msg: str) -> str:
        self.sent = msg
        return "resp:" + msg


class DummyManager:
    def __init__(self):
        self.connections = {"agent1": DummyConn()}

    async def get(self, id_):
        return self.connections.get(id_)

    async def list_all(self):
        return self.connections


def override_manager() -> DummyManager:
    return DummyManager()


from darkscryc2server.core.connection import ConnectionManager


def test_command_route():
    original = app.state.conn_manager
    app.state.conn_manager = DummyManager()
    client = TestClient(app)
    resp = client.post("/command/agent1", json={"command": "hello"})
    assert resp.status_code == 200
    assert resp.json()["result"] == 'resp:{"command":"hello","args":null}'
    app.state.conn_manager = original
