# manager_client.py
import asyncio
import json
from ..tools import pack_base_header, unpack_base_header
from ...Models.protocols import SOCKET_BASE_MESSAGE_HEADER, SIZE_OF_SOCKET_BASE_MESSAGE_HEADER
from ...Models.remote_tools_schemas import ManagerResponse

async def _send_manager_request(host, port, data_dict: dict) -> dict:
    """
    data_dict is basically {"action": "...", "conn_id": ..., "command": ...}
    We'll build JSON, measure length, send 4-byte header + payload, read response.
    Returns the parsed JSON dict from server.
    """
    reader, writer = await asyncio.open_connection(host, port)

    payload_bytes = json.dumps(data_dict).encode("utf-8")
    hdr = SOCKET_BASE_MESSAGE_HEADER()
    hdr.payload_length = len(payload_bytes)
    header_data = pack_base_header(hdr)

    # write
    writer.write(header_data)
    writer.write(payload_bytes)
    await writer.drain()

    # read response header
    resp_hdr_data = await reader.readexactly(SIZE_OF_SOCKET_BASE_MESSAGE_HEADER)
    resp_hdr = unpack_base_header(resp_hdr_data)
    resp_len = resp_hdr.payload_length

    # read the payload
    resp_data = await reader.readexactly(resp_len)
    writer.close()
    return json.loads(resp_data.decode("utf-8"))


# Then you define convenience methods:
async def remote_get_connections(host="127.0.0.1", port=9100):
    req = {"action": "get_connections"}
    resp = await _send_manager_request(host, port, req)
    return ManagerResponse(**resp)

async def remote_send_command(conn_id: str, command: str, host="127.0.0.1", port=9100):
    req = {"action": "send_command", "conn_id": conn_id, "command": command}
    resp = await _send_manager_request(host, port, req)
    return ManagerResponse(**resp)
