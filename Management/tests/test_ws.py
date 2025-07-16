import uuid

import pytest
import starlette.websockets
from httpx import AsyncClient

from app.models.user import UserRole
from app.routers.ws import shell_websocket

pytestmark = pytest.mark.anyio


async def test_shell_websocket(
    client: AsyncClient, create_test_user, get_token, monkeypatch
):
    await create_test_user("op", UserRole.OPERATOR)
    token = await get_token("op")

    fake_response = {"result": "pong"}

    async def fake_remote_send_command(**kwargs):
        from darkscryc2server.models.messages import AgentResponse

        return AgentResponse(success=True, data=fake_response)

    monkeypatch.setattr(
        "app.routers.ws.remote_send_command",
        fake_remote_send_command,
    )

    class DummyWebSocket:
        def __init__(self):
            self.sent = []
            self.accepted = False
            self.query_params = {"token": token}
            self._calls = 0

        async def accept(self):
            self.accepted = True

        async def receive_json(self):
            if self._calls == 0:
                self._calls += 1
                return {"command": "ping"}
            raise starlette.websockets.WebSocketDisconnect()

        async def send_json(self, data):
            self.sent.append(data)

        async def close(self, code: int):
            self.closed = code

    ws = DummyWebSocket()
    await shell_websocket(ws, uuid.uuid4())

    assert ws.accepted is True
    assert ws.sent == [{"message": fake_response}]
