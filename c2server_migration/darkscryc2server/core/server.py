import ssl

import websockets
from websockets.server import WebSocketServerProtocol

from .config import settings
from .connection import ConnectionManager, WsConnection


class WebSocketServer:
    def __init__(self) -> None:
        self.conn_manager = ConnectionManager(settings.redis_url)
        if settings.ssl_cert and settings.ssl_key:
            self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            self.ssl_context.load_cert_chain(settings.ssl_cert, settings.ssl_key)
        else:
            self.ssl_context = None

    async def start(self) -> None:
        await self.conn_manager.wait_ready()
        server = await websockets.serve(
            self.handle_ws,
            settings.host,
            settings.ws_port,
            ssl=self.ssl_context,
            max_size=104857600,
            compression=None,
        )
        async with server:
            await server.wait_closed()

    async def handle_ws(self, websocket: WebSocketServerProtocol) -> None:
        agent_id = websocket.path.removeprefix("/agent/").strip("/")
        conn = WsConnection(websocket=websocket, id=agent_id)
        await self.conn_manager.register(conn)
        try:
            await websocket.wait_closed()
        finally:
            await self.conn_manager.unregister(conn)
