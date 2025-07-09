from __future__ import annotations

from dataclasses import dataclass
from websockets.server import WebSocketServerProtocol

@dataclass
class WsConnection:
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
        """Send a message and wait for exactly one response."""
        await self.websocket.send(message)
        try:
            response = await self.websocket.recv()
        except Exception as exc:
            raise ConnectionError(f"WebSocket closed: {exc}")
        return response
