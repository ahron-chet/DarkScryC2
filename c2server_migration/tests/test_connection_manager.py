import asyncio

import pytest

from darkscryc2server.core.connection import ConnectionManager, WsConnection


class DummyWebSocket:
    def __init__(self) -> None:
        self.remote_address = ("127.0.0.1", 0)
        self.closed = False

    async def close(self) -> None:
        self.closed = True


@pytest.mark.asyncio
async def test_register_and_unregister(fake_redis):
    manager = ConnectionManager("redis://test")
    await manager.wait_ready()
    ws = DummyWebSocket()
    conn = WsConnection(websocket=ws, id="agent1")
    await manager.register(conn)
    assert await manager.get("agent1") is conn
    assert await fake_redis.get("connection:agent1") == conn.serialize()

    await manager.unregister(conn)
    assert await manager.get("agent1") is None
    assert await fake_redis.get("connection:agent1") is None
    assert ws.closed


@pytest.mark.asyncio
async def test_concurrent_register_unregister(fake_redis):
    manager = ConnectionManager("redis://test")
    await manager.wait_ready()
    ws1 = DummyWebSocket()
    ws2 = DummyWebSocket()
    conn1 = WsConnection(websocket=ws1, id="a1")
    conn2 = WsConnection(websocket=ws2, id="a2")

    async def worker(c: WsConnection):
        await manager.register(c)
        await asyncio.sleep(0)
        await manager.unregister(c)

    await asyncio.gather(worker(conn1), worker(conn2))
    assert await manager.list_all() == {}
    assert ws1.closed
    assert ws2.closed
