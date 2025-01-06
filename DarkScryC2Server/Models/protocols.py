import ctypes

class SOCKET_BASE_MESSAGE_HEADER(ctypes.Structure):
    _pack_ = 1

    _fields_ = [
        ("payload_length", ctypes.c_uint32),       
    ]


SIZE_OF_SOCKET_BASE_MESSAGE_HEADER = ctypes.sizeof(SOCKET_BASE_MESSAGE_HEADER)