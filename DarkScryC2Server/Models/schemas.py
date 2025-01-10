from pydantic import BaseModel, Field, field_validator, BaseModel
from typing import Union
from enum import Enum
from uuid import UUID
from ..Utils.tools import hex_to_bytes, gen_xml

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
    


class CommandIdentifiers(str, Enum):
    START_SHELL_INSTANCE = ("be425fd08e9ea24230bac47493228ada", "Start a shell instance on client")
    RUN_COMMAND = ("58e129c7158b9fed8be5473640e54ae4", "Execute a command on a running shell instance")

    def __new__(cls, value, description):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        return obj

    @property
    def desc(self):
        """Returns the description of the command."""
        return self.description
    


class Command(BaseModel):

    action: CommandIdentifiers = Field(
        ...,
        title="Action",
        description="The identifier of the action to perform."
    )


    def model_dump(self, *args, **kwargs):
        base_dump = super().model_dump(*args, **kwargs)
        if isinstance(self.action, CommandIdentifiers):
            base_dump['action'] = self.action.value
        return base_dump
    
    def xml(self, *args, **kwargs):
        base_dump = super().model_dump(*args, **kwargs)
        if isinstance(self.action, CommandIdentifiers):
            base_dump['action'] = self.action.value
        return gen_xml(tag="root", **base_dump)
    
    class Config:  
        use_enum_values = True
        