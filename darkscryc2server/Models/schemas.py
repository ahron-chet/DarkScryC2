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
    START_SHELL_INSTANCE   = ("be425fd08e9ea24230bac47493228ada", "Start a shell instance on client")
    RUN_COMMAND            = ("58e129c7158b9fed8be5473640e54ae4", "Execute a command on a running shell instance")
    GET_BASIC_MACHINE_INFO = ("929cecb8e795d93306020c7f2e8682d2", "GET_BASIC_MACHINE_INFO")
    SNAP_FULL_DIRECTORY    = ("74d6aa572d1b19102f9f5aedbe00dfd0", "SNAP_FULL_DIRECTORY")
    GET_FILE_BASE_64       = ("d69c0ca9f6848c89b7e9223b2d186a15", "GET_FILE_BASE_64")


    def __new__(cls, value, description):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        return obj

    @property
    def desc(self):
        """Returns the description of the command."""
        return self.description

class CommandIdentifiersName(str, Enum):
    pass
CommandIdentifiersName = Enum(
    "CommandIdentifiers", 
    {name: name for name in list(CommandIdentifiers.__members__.keys()) + ["UNKNOW"]}
)


class Command(BaseModel):

    action: str = Field(
        ...,
        title="Action",
        description="The identifier of the action to perform.",
        Literal=True
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


class GenAction(Command):
    action: CommandIdentifiers = Field(..., Literal=False, description="Action to prform basen on CommandIdentifiers enum")

    class Config:
        extra = "allow"
        allow_extra_fildes = True