from pydantic import Field
from typing import Optional
from ..schemas import Command, CommandIdentifiers

        



class StartShellCommand(Command):
    action: CommandIdentifiers = Field(
        CommandIdentifiers.START_SHELL_INSTANCE,
        title="Action",
        description="Start a shell instance on the client."
    )
    file_name: Optional[str] = Field(
        "cmd.exe",
        title="Session Name",
        description="Optional name for the shell session."
    )

class RunCommand(Command):
    action: CommandIdentifiers = Field(
        CommandIdentifiers.RUN_COMMAND,
        title="Action",
        description="Execute a command on a running shell instance."
    )

    command: str = Field(
        ...,
        title="Command",
        description="The command to be executed."
    )


