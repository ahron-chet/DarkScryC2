import asyncio
import uuid
import time
from typing import Dict, Optional, Union

from .redis_manager import RedisManager
from .wsbased_connection import WsConnection
from ..Cryptography.Symetric import AesCrypto
from ..settings.config import internalapplogger as logger
from pickle import dumps, loads

_MAX_LENGTH_FOR_SYNC = 65536

# Suppose these come from your "protocols.py" or similar
from ..Models.protocols import (
    OPCODE_KEEPALIVE,
    OPCODE_CMD_REQUEST,
    OPCODE_CMD_RESPONSE,
    pack_message,
    SOCKET_BASE_MESSAGE_HEADER,
    SIZE_OF_SOCKET_BASE_MESSAGE_HEADER,
    compute_header_checksum,
    SIZE_OF_SUM,
    PADDED_SUM_SIZE
)


class Connection:
    def __init__(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        aes_manager: AesCrypto,
        uid: uuid.UUID,
        keepalive_timeout: float = 900.0
    ):
        self.id = str(uid)
        self.reader = reader
        self.writer = writer
        self.aes_manager = aes_manager
        self.address = writer.get_extra_info("peername")

        self._running = True
        self._pending_requests: Dict[int, asyncio.Future] = {}
        self._next_request_id = 1

        self.keepalive_timeout = keepalive_timeout
        self.last_keepalive_recv = time.time()

    async def start(self):
        """
        Main read loop: 
          1) read header
          2) read body_length
          3) if opcode == KEEPALIVE => skip decrypt
          4) else decrypt => parse sum => dispatch
        """
        asyncio.create_task(self._keep_alive())
        logger.debug(f"[Connection {self.id}] Starting read loop.")
        try:
            while self._running and not self.writer.is_closing():
                header, body_data = await self._receive_message()
                if header is None:
                    # Possibly partial read => break
                    break

                if header.opcode == OPCODE_KEEPALIVE:
                    # For keepalive => assume body_length=0, so no decryption.
                    logger.debug(f"[{self.id}] KEEPALIVE => update last_keepalive_recv")
                    self.last_keepalive_recv = time.time()
                    # If you want to handle keepalive further, do it here or in dispatch
                    continue

                # else => normal message => decode & pass to dispatch
                await self._dispatch_message(header, body_data)

        except asyncio.CancelledError:
            logger.debug(f"[Connection {self.id}] Task cancelled.")
        except Exception as exc:
            logger.error(f"[Connection {self.id}] Read loop error: {exc}")
        finally:
            self._running = False
            for _, fut in self._pending_requests.items():
                if not fut.done():
                    fut.set_exception(ConnectionError("Connection closed"))
            self._pending_requests.clear()
            self.close()

    async def _dispatch_message(self, header: SOCKET_BASE_MESSAGE_HEADER, ciphertext: bytes):
        """
        Decrypt + parse sum + call _dispatch_opcode
        """
        use_async = (len(ciphertext) > _MAX_LENGTH_FOR_SYNC)
        try:
            plaintext = await self.aes_manager.decrypt(ciphertext, use_async=use_async)
            logger.debug(plaintext)
        except Exception as ex:
            logger.error(f"[{self.id}] Decrypt error: {ex}")
            self.close()
            return

        if len(plaintext) < SIZE_OF_SUM:
            logger.error(f"[{self.id}] Plaintext too short for sum => closing.")
            self.close()
            return

        # The first 4 bytes => actual sum, the next (PAD_LEN) if you used random padding => skip
        actual_sum = plaintext[:SIZE_OF_SUM]
        # skip random pad => e.g. plaintext[4:16] if used
        payload = plaintext[PADDED_SUM_SIZE:]  # the rest is the real body

        # compute expected sum => no random pad
        expected_sum = compute_header_checksum(header.opcode, header.request_id, add_random_pad=False)[:SIZE_OF_SUM]
        if actual_sum != expected_sum:
            logger.error(f"[{self.id}] Checksum mismatch => closing.")
            self.close()
            return

        # Finally handle the opcode logic
        await self._dispatch_opcode(header, payload)

    async def _dispatch_opcode(self, header: SOCKET_BASE_MESSAGE_HEADER, payload: bytes):
        """
        Decide how to handle the final payload, after we verified
        (opcode, request_id) with the sum. 
        """
        opcode = header.opcode
        req_id = header.request_id

        if opcode == OPCODE_CMD_RESPONSE:
            logger.debug(f"[{self.id}] CMD_RESPONSE => reqId={req_id}, {len(payload)} bytes.")
            fut = self._pending_requests.pop(req_id, None)
            if fut and not fut.done():
                fut.set_result(payload)

        elif opcode == OPCODE_CMD_REQUEST:
            logger.debug(f"[{self.id}] CMD_REQUEST => reqId={req_id}, {len(payload)} bytes.")
            pass

        else:
            logger.debug(f"[{self.id}] Unhandled opcode {opcode}, reqId={req_id}, payloadLen={len(payload)}.")

    async def _keep_alive(self):
        while True:
            await asyncio.sleep(600)
            if not self.is_alive():
                logger.debug("Client didnt sent keep alive for more than 20 minutes")
                self.close()
                return

    def is_alive(self):
        return time.time() < self.last_keepalive_recv + 1200

    async def send_command(self, body_data: bytes) -> Optional[bytes]:
        """
        Send a CMD_REQUEST to the client, wait for CMD_RESPONSE.
        """
        if not body_data:
            body_data = b''

        req_id = self._allocate_request_id()
        fut = asyncio.get_running_loop().create_future()
        self._pending_requests[req_id] = fut

        await self._send_encrypted(OPCODE_CMD_REQUEST, req_id, body_data)
        return await fut

    def close(self):
        if not self._running:
            return
        logger.debug(f"[{self.id}] Closing connection.")
        self._running = False
        if not self.writer.is_closing():
            self.writer.close()
     

    def _allocate_request_id(self) -> int:
        r = self._next_request_id
        self._next_request_id = (r + 1) % 65536
        return r

    async def _send_encrypted(self, opcode: int, request_id: int, body: bytes):
        """
        1) compute 4-byte sum (plus random pad)
        2) combine => plaintext
        3) encrypt => ciphertext
        4) pack => 7-byte header
        5) write to stream
        """
        # sum => 4 bytes + random pad => total PADDED_SUM_SIZE
        chksum = compute_header_checksum(opcode, request_id, add_random_pad=True)
        combined_plain = chksum + body

        use_async = (len(combined_plain) > _MAX_LENGTH_FOR_SYNC)
        ciphertext = await self.aes_manager.encrypt(combined_plain, use_async=use_async)

        message = pack_message(opcode, request_id, ciphertext)
        logger.debug(f"[{self.id}] Sending opcode={opcode}, reqId={request_id}, bodyLen={len(body)}, cipherLen={len(ciphertext)}.")
        self.writer.write(message)
        await self.writer.drain()

    async def _receive_message(self):
        """
        Returns (header, body_data).
        If opcode=KEEPALIVE => typically body_length=0 => read no data.
        """
        try:
            raw_header = await self.reader.readexactly(SIZE_OF_SOCKET_BASE_MESSAGE_HEADER)
        except asyncio.IncompleteReadError:
            logger.error(f"[{self.id}] Failed to read header => likely closed.")
            return None, None

        header = SOCKET_BASE_MESSAGE_HEADER.from_buffer_copy(raw_header)

        if header.payload_length < 0:
            logger.error(f"[{self.id}] Negative body_length => corrupted header => closing.")
            return None, None

        try:
            body_data = await self.reader.readexactly(header.payload_length)
        except asyncio.IncompleteReadError:
            logger.error(f"[{self.id}] Truncated ciphertext => closing.")
            return None, None

        logger.debug(f"[{self.id}] Received header(opcode={header.opcode}, reqId={header.request_id}, length={header.payload_length}).")
        return header, body_data


class ConnectionManager:
    def __init__(self, redis_url: str) -> None:
        self.connections: Dict[str, Union[Connection, WsConnection]] = {}
        self.redis_manager = RedisManager(redis_url)
        self._redis_connect_task = asyncio.create_task(self._async_connect())

    async def _async_connect(self):
        """
        Private async method that attempts to connect to Redis.
        """
        try:
            await self.redis_manager.connect()
        except RuntimeError as e:
            logger.error(f"Failed to connect to Redis: {e}")

    async def wait_until_connected(self):
        """
        Optional method to wait for the Redis connection to finish.
        If you want to ensure the connection is ready, call:
           await manager.wait_until_connected()
        """
        await self._redis_connect_task

    @staticmethod
    def _connection_type(connection):
        if isinstance(connection, Connection):
            return "ACPROTO" 
        elif isinstance(connection, WsConnection):
            return "WSPROTO" 
        raise TypeError("Unsupported connection type {}.".format(str(type(Connection))))

    async def register(self, connection: Union[Connection, WsConnection]) -> None:
        type = self._connection_type(connection)
        self.connections[connection.id] = connection
        logger.info(f"Registered connection {connection.id} from {connection.address}")
        try:
            
            await self.redis_manager.set(
                key=f"connection:{connection.id}",
                value=dumps({"address": str(connection.address), "type":type})
            )
        except RuntimeError as e:
            logger.error(f"Redis set error: {e}")

    async def unregister(self, connection: Union[Connection, WsConnection]) -> None:
        conn_id = connection.id
        if conn_id in self.connections:
            connection.close()
            del self.connections[conn_id]
            logger.info(f"Unregistered connection {conn_id}")
            try:
                await self.redis_manager.delete(key=f"connection:{conn_id}")
                # await self.redis_manager.delete(key=f"connection:{conn_id}:last_ping")
            except RuntimeError as e:
                logger.error(f"Redis delete error: {e}")

    def get_connection(self, conn_id: str) -> Optional[Union[Connection, WsConnection]]:
        return self.connections.get(conn_id)

    def get_all_connections(self) -> Dict[str, Union[Connection, WsConnection]]:
        return  self.connections
    
    async def get_all_connections_redis(self) -> Dict[str, dict]:
        return  {i: loads(await self.redis_manager.get(f"connection:{i}")) for i in self.connections}

    async def close_all_connections(self) -> None:
        for conn in list(self.connections.values()):
            await self.unregister(conn)
        logger.info("All connections have been closed.")   