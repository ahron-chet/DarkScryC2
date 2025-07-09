import asyncio

import pytest

from darkscryc2server.core.server import WebSocketServer


class DummyWebSocket:
    def __init__(self, path: str) -> None:
        self.path = path
        self.remote_address = ("127.0.0.1", 0)
        self.closed = False
        self._closed = asyncio.Event()

    async def wait_closed(self) -> None:
        await self._closed.wait()

    async def close(self) -> None:
        self.closed = True
        self._closed.set()


@pytest.mark.asyncio
async def test_handle_ws_registers_and_unregisters(fake_redis):
    server = WebSocketServer()
    await server.conn_manager.wait_ready()
    ws = DummyWebSocket("/agent/agent1")
    task = asyncio.create_task(server.handle_ws(ws))
    await asyncio.sleep(0)
    assert "agent1" in (await server.conn_manager.list_all())
    await ws.close()
    await task
    assert "agent1" not in (await server.conn_manager.list_all())
    assert ws.closed
