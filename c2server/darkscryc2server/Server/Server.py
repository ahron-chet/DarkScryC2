import asyncio
import ssl
import websockets
from websockets.asyncio.server import ServerConnection

from ..settings.config import (
    SERVER_HOST,
    internalapplogger as logger,
    REDIS_URI,
    SSL_CERTIFICATE,
    SSL_CERTIFICATE_KEY
)

from ..Managers.connection_manager import ConnectionManager
from ..Managers.wsbased_connection import WsConnection


class Server:
    def __init__(self) -> None:
        # Manager for active WebSocket connections
        self.connection_manager = ConnectionManager(REDIS_URI)

        # Optionally choose a separate port for WebSocket
        self.ws_port = 876
        if SSL_CERTIFICATE is None or SSL_CERTIFICATE_KEY is None:
            self.ssl_context = None
        else:
            self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            self.ssl_context.load_cert_chain(certfile=SSL_CERTIFICATE, keyfile=SSL_CERTIFICATE_KEY)


    async def start(self) -> None:
        """Start the WebSocket server and serve clients indefinitely."""
        # Make sure Redis is connected
        await self.connection_manager.wait_until_connected()

        try:
            # Start the WebSocket server on a separate port
            ws_server = await websockets.serve(
                self._handle_websocket,
                SERVER_HOST,
                self.ws_port,
                ssl=self.ssl_context,  # pass SSL context if using TLS
                max_size=104857600, # 100MB
                compression=None
            )
            logger.info(f"WebSocket server started on {SERVER_HOST}:{self.ws_port}")

            # Run the WebSocket server until it is closed
            async with  ws_server:
                await asyncio.gather(
                    ws_server.wait_closed()
                )

        except Exception as e:
            logger.error(f"Server failed to start: {e}")


    # -------------------------------------------------------------------------
    #                    WebSocket Handling (WSPROTO)
    # -------------------------------------------------------------------------
    async def _handle_websocket(self, websocket: ServerConnection):
        """
        Handle a new WebSocket client. The agent identifier is passed as part of
        the connection path.
        """
        ws_conn: WsConnection = None
        try:
            # 1) Read the agent_id
            agent_id = websocket.request.path.split("/", 1)[1]
            if not agent_id:
                await websocket.close()

            # 2) Create WsConnection
            ws_conn = WsConnection(websocket, agent_id=agent_id)

            # 3) Register with manager
            await self.connection_manager.register(ws_conn)
            logger.info(f"WebSocket client connected: agent_id={agent_id}, path={websocket.request.path}")

            # 4) Start reading messages. We'll do a streaming approach:
            # def on_message(msg: str):
            #     logger.info(f"[WsConnection {agent_id}] => {msg}")
            #     # Optionally echo or handle

            # await ws_conn.start_stream(on_message=on_message)
            
            await websocket.wait_closed()
        except websockets.ConnectionClosed as exc:
            logger.warning(f"WebSocket closed: {exc}")
        except Exception as e:
            logger.error(f"Error in _handle_websocket: {e}")
        finally:
            if ws_conn is not None:
                await self.connection_manager.unregister(ws_conn)
