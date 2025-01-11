from pydantic import BaseModel
from typing import Optional
from enum import Enum


class ManagerAction(str, Enum):
    GET_CONNECTIONS = "get_connections"
    SEND_COMMAND    = "send_command"
    # add more as needed

class ManagerRequest(BaseModel):
    action: ManagerAction
    conn_id: Optional[str] = None
    command: Optional[str] = None
    # You can add more fields if needed

class ManagerResponse(BaseModel):
    # For consistency, we'll also define a pydantic model for the response
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None