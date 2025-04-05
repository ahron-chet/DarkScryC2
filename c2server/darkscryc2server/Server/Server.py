import asyncio
import ssl
import websockets
from json import loads
from websockets.asyncio.server import ServerConnection

from ..settings.config import (
    SERVER_HOST,
    SERVER_PORT,
    internalapplogger as logger,
    REDIS_URI,
    PRIVATE_KEY_PATH
)

from ..Managers.connection_manager import ConnectionManager, Connection
from ..Managers.wsbased_connection import WsConnection
from ..Cryptography.Asymetric import RSAManager
from ..Cryptography.Symetric import AesCrypto
from ..Models.schemas import AgentConnection


class Server:
    def __init__(self) -> None:
        # Shared manager for both ACPROTO and WSPROTO connections
        self.connection_manager = ConnectionManager(REDIS_URI)
        # RSA manager for legacy handshake
        # self._rsa_manager = RSAManager(PRIVATE_KEY_PATH)

        # Optionally choose a separate port for WebSocket
        self.ws_port = 876


        self.ssl_context = None
        # Example:
        # self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        # self.ssl_context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    async def start(self) -> None:
        """
        Start listening on:
          - A TCP server for the old AC protocol (RSA handshake + AES).
          - A WebSocket server for the new protocol.
        Run both indefinitely.
        """
        # Make sure Redis is connected
        await self.connection_manager.wait_until_connected()

        try:
            # 1) Start the legacy TCP server
            # tcp_server = await asyncio.start_server(
            #     self._handle_client,
            #     SERVER_HOST,
            #     SERVER_PORT,
            #     limit=100 * 1024 * 1024 # 100MB
            # )
            # logger.info(f"TCP server started on {SERVER_HOST}:{SERVER_PORT}")

            # 2) Start the WebSocket server on a separate port
            ws_server = await websockets.serve(
                self._handle_websocket,
                SERVER_HOST,
                self.ws_port,
                ssl=self.ssl_context,  # pass SSL context if using TLS
                max_size=104857600 # 100MB
            )
            logger.info(f"WebSocket server started on {SERVER_HOST}:{self.ws_port}")

            # 3) Run both servers concurrently until cancelled
            # async with tcp_server, ws_server:
            #     await asyncio.gather(
            #         tcp_server.serve_forever(),
            #         ws_server.wait_closed()
            #     )
            async with  ws_server:
                await asyncio.gather(
                    ws_server.wait_closed()
                )

        except Exception as e:
            logger.error(f"Server failed to start: {e}")

    # -------------------------------------------------------------------------
    #                     Legacy TCP Handling (ACPROTO)
    # -------------------------------------------------------------------------
    async def _handle_client(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter
    ) -> None:
        """
        Handle a new legacy TCP client using your existing ACPROTO handshake.
        """
        try:
            # 1) Perform RSA-based handshake to get (conn_id, aes_manager)
            conn_id, aes_manager = await self._perform_handshake(reader, writer)
            if not conn_id or not aes_manager:
                # Handshake failed or incomplete => bail out
                return

            # 2) Build the Connection object
            connection = Connection(reader, writer, aes_manager, conn_id)
            # 3) Register it with the shared manager
            await self.connection_manager.register(connection)

        except Exception as e:
            logger.error(f"Handshake error: {e}")
            writer.close()
            return

        try:
            # 4) Enter the normal read loop for that connection
            await connection.start()
        except Exception as e:
            logger.error(f"Connection {connection.id} error: {e}")
        finally:
            await self.connection_manager.unregister(connection)

    async def _perform_handshake(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter
    ):
        """
        Reads 256 bytes, decrypts with RSA, expects JSON => AgentConnection.
        Then creates an AesCrypto with the provided key.
        Returns (agent_id, aes_manager).
        """
        # 1) read exactly 256 bytes
        try:
            raw_connection = await reader.readexactly(256)
        except asyncio.IncompleteReadError:
            logger.warning("Client disconnected before sending handshake.")
            writer.close()
            return None, None

        # 2) RSA-decrypt that data
        try:
            decrypted_data = await asyncio.to_thread(self._rsa_manager.decrypt_data, raw_connection)
        except Exception as e:
            logger.error(f"RSA decryption failed: {e}")
            writer.close()
            return None, None

        # 3) parse JSON => build AesCrypto
        try:
            connect_data = AgentConnection(**loads(decrypted_data))
            # connect_data.key is the AES key in hex or raw bytes?
            # (Adapt as needed; e.g. if it's hex, decode it here.)
            aes = AesCrypto(connect_data.key, None)
            aes.set_iv(key=connect_data.key)
            return str(connect_data.agent_id), aes
        except Exception as e:
            logger.error(f"Invalid handshake data: {e}")
            writer.close()
            return None, None

    # -------------------------------------------------------------------------
    #                    WebSocket Handling (WSPROTO)
    # -------------------------------------------------------------------------
    async def _handle_websocket(self, websocket: ServerConnection):
        """
        Handle a new WebSocket client. 
        We'll assume the client sends a JSON handshake message with agent_id.
        If you want RSA-based handshake for WebSockets, do it here.
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
