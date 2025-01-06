from pydantic import BaseModel, Field, field_validator
from typing import Union
from uuid import UUID
from ..Utils.tools import hex_to_bytes

class AgentConnection(BaseModel):
    agent_id: Union[str, UUID] = Field(..., description="A valid UUID representing the agent's ID")
    key: Union[str, bytes] = Field(..., description="A valid Aes key for the session")


    @field_validator("agent_id")
    def validate_agent_id(cls, v):
        try:
            return UUID(v)
        except:
            raise ValueError ("agent_id is not a valide UUID")
        
    @field_validator("key")
    def validate_key(cls, v):
        if isinstance(v, str):
            return hex_to_bytes(v)
        return v
    