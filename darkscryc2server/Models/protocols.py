import ctypes
import struct
import zlib
from os import urandom

class SOCKET_BASE_MESSAGE_HEADER(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("opcode", ctypes.c_uint8),
        ("request_id", ctypes.c_uint16),
        ("payload_length", ctypes.c_uint32),
    ]

SIZE_OF_SOCKET_BASE_MESSAGE_HEADER = ctypes.sizeof(SOCKET_BASE_MESSAGE_HEADER)
SIZE_OF_SUM = 4
PADDED_SUM_SIZE = 16
PADDING_SUM = PADDED_SUM_SIZE - SIZE_OF_SUM

OPCODE_KEEPALIVE = 1
OPCODE_CMD_REQUEST = 3
OPCODE_CMD_RESPONSE = 4

def pack_message(opcode, request_id, body):
    if body is None:
        body = b''
    h = SOCKET_BASE_MESSAGE_HEADER(opcode, request_id, len(body))
    return bytes(h) + body

def unpack_message(data):
    if len(data) < SIZE_OF_SOCKET_BASE_MESSAGE_HEADER:
        raise ValueError("Data too short")
    h = SOCKET_BASE_MESSAGE_HEADER.from_buffer_copy(data[:SIZE_OF_SOCKET_BASE_MESSAGE_HEADER])
    if len(data) < SIZE_OF_SOCKET_BASE_MESSAGE_HEADER + h.payload_length:
        raise ValueError("Truncated data")
    body = data[SIZE_OF_SOCKET_BASE_MESSAGE_HEADER:SIZE_OF_SOCKET_BASE_MESSAGE_HEADER + h.payload_length]
    return h.opcode, h.request_id, body


def compute_header_checksum(opcode, request_id, add_random_pad=True):
    data = struct.pack("<BH", opcode, request_id)
    csum = (zlib.crc32(data) & 0xFFFFFFFF).to_bytes(4, "little")
    if add_random_pad:
        csum += urandom(PADDING_SUM)
    return csum
