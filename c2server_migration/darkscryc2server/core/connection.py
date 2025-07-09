from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Dict

from redis.asyncio import Redis
from websockets.server import WebSocketServerProtocol


@dataclass
class WsConnection:
    """Represents an active WebSocket connection to an agent."""

    websocket: WebSocketServerProtocol
    id: str

    def __post_init__(self) -> None:
        self.address = self.websocket.remote_address

    async def close(self) -> None:
        if not self.websocket.closed:
            await self.websocket.close()

    def serialize(self) -> bytes:
        return str({"address": str(self.address), "type": "ws"}).encode()

    async def send_and_receive(self, message: str) -> str:
        await self.websocket.send(message)
        try:
            response = await self.websocket.recv()
        except Exception as exc:  # pragma: no cover - network failures
            raise ConnectionError(f"WebSocket closed: {exc}")
        return response


class RedisClient:
    """Thin wrapper around redis.asyncio for easy mocking."""

    def __init__(self, url: str) -> None:
        self.url = url
        self._redis: Redis | None = None

    async def connect(self) -> None:
        self._redis = Redis.from_url(self.url)
        await self._redis.ping()

    async def set(self, key: str, value: bytes) -> None:
        if self._redis is None:
            raise RuntimeError("Redis not connected")
        await self._redis.set(key, value)

    async def get(self, key: str) -> bytes | None:
        if self._redis is None:
            raise RuntimeError("Redis not connected")
        return await self._redis.get(key)

    async def delete(self, key: str) -> None:
        if self._redis is None:
            raise RuntimeError("Redis not connected")
        await self._redis.delete(key)

    async def close(self) -> None:
        if self._redis:
            await self._redis.close()
            self._redis = None


class ConnectionManager:
    def __init__(self, redis_url: str) -> None:
        self.redis = RedisClient(redis_url)
        self.connections: Dict[str, WsConnection] = {}
        self._connect_task = asyncio.create_task(self.redis.connect())

    async def wait_ready(self) -> None:
        await self._connect_task

    async def register(self, conn: WsConnection) -> None:
        await self.wait_ready()
        self.connections[conn.id] = conn
        await self.redis.set(f"connection:{conn.id}", conn.serialize())

    async def unregister(self, conn: WsConnection) -> None:
        await self.wait_ready()
        self.connections.pop(conn.id, None)
        await conn.close()
        await self.redis.delete(f"connection:{conn.id}")

    def get(self, conn_id: str) -> WsConnection | None:
        return self.connections.get(conn_id)

    def list_all(self) -> Dict[str, WsConnection]:
        return dict(self.connections)
