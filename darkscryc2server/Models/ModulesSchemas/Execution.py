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
    action: str = (CommandIdentifiers.RUN_COMMAND.value)
    command: str = Field(
        ...,
        title="Command",
        description="The command to be executed."
    )


class GenAction(Command):
    action: CommandIdentifiers = Field(..., Literal=False, description="Action to prform basen on CommandIdentifiers enum")


