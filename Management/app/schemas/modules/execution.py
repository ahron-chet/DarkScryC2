from typing import Optional

from darkscryc2server.models.messages import CommandIdentifiers
from pydantic import BaseModel, Field


class StartShellCommand(BaseModel):
    file_name: Optional[str] = Field(
        "cmd.exe",
        title="Session Name",
        description="Optional name for the shell session.",
    )
    user_name: Optional[str] = Field(
        None, title="Session Name", description="Optional name for the shell session."
    )


class RunCommand(BaseModel):
    command: str = Field(
        ..., title="Command", description="The command to be executed."
    )
