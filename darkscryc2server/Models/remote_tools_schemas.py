
from typing import Optional, Dict
from pydantic import BaseModel, Field
from enum import Enum


class ManagerAction(str, Enum):
    GET_CONNECTIONS = "get_connections"
    SEND_COMMAND    = "send_command"


class ManagerSendCommand(BaseModel):
    conn_id: str = Field(..., description="Optional agent identifier for the client connection.")
    command: str = Field(..., description="Optional command or directive to execute on client.")


class ManagerResponse(BaseModel):
    success: bool = Field(..., description="Indicates if the operation was successful.")
    data: Optional[Dict] = Field(None, description="Optional data returned by the operation.")
    error: Optional[str] = Field(None, description="Optional error message in case of failure.")


class ManagerRequestWs(BaseModel):
    action: ManagerAction = Field(..., description="The specific action the manager should perform.")
    conn_id: Optional[str] = Field(None, description="Optional agent identifier for the client connection.")
    command: Optional[str] = Field(None, description="Optional command or directive to execute on client.")