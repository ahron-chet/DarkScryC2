from enum import Enum

from pydantic import BaseModel


class CommandMessage(BaseModel):
    command: str
    args: list[str] | None = None


class ManagerAction(str, Enum):
    GET_CONNECTIONS = "get_connections"
    SEND_COMMAND = "send_command"


class ManagerRequestWs(BaseModel):
    action: ManagerAction
    conn_id: str | None = None
    command: str | None = None


class ManagerResponse(BaseModel):
    success: bool
    data: dict | None = None
    error: str | None = None
