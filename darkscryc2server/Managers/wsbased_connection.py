import websockets
from websockets.asyncio.server import ServerConnection
from typing import Callable
from uuid import UUID

class WsConnection:
    """
    A WebSocket-based connection that can operate in one of two modes:
      1) send_and_receive(message): sends a message, then awaits exactly one message in return.
      2) start_stream(on_message): continuously reads messages and calls on_message(msg).

    We do NOT use request IDs or opcodes here—it's strictly 'next message in' is the response.
    """

    def __init__(
        self,
        websocket: ServerConnection,
        agent_id: UUID
    ):
        """
        :param websocket: An active `websockets` server-side connection.
        :param agent_id: A string that identifies the remote client. If not given, generate a UUID.
        """
        self.id = agent_id
        self.websocket = websocket
        self.address = websocket.remote_address
        self._running = False

    async def send_and_receive(self, message: str) -> str:
        """
        Sends a message (string) to the client, then waits for exactly one incoming message.
        Returns the string that was received.

        NOTE: This blocks (awaits) until the client sends something back.
        """
        # 1) Send
        await self.websocket.send(message)

        # 2) Await next inbound message
        try:
            response = await self.websocket.recv()
            return response
        except websockets.ConnectionClosed as exc:
            raise ConnectionError(f"WebSocket closed: {exc}")

    async def start_stream(self, on_message: Callable[[str], None]) -> None:
        """
        Listens for incoming messages in a loop. For each message, calls on_message(msg).

        If the WebSocket closes or any exception occurs, the loop ends and closes the connection.
        """
        self._running = True
        try:
            while self._running:
                msg = await self.websocket.recv()
                on_message(msg)
        except websockets.ConnectionClosed as exc:
            print(f"[WsConnection {self.id}] WebSocket closed: {exc}")
        except Exception as exc:
            print(f"[WsConnection {self.id}] Error in stream: {exc}")
        finally:
            self._running = False
            await self.close()

    async def close(self):
        """
        Closes the WebSocket connection (if open).
        """
        await self.websocket.close()
