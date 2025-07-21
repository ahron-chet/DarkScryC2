from enum import Enum
from typing import Optional

from darkscryc2server.models.messages import CommandIdentifiers
from pydantic import BaseModel, Field


class ShellCreationType(str, Enum):
    current_user = "current_user"
    impersonate_token_duplicate = "impersonate_token_duplicate"
    credentials = "credentials"


class StartShellCommand(BaseModel):
    file_name: Optional[str] = Field(
        "cmd.exe",
        description="Optional name for the shell session.",
    )
    user_name: Optional[str] = Field(
        None,
        description="Optional username when using credentials.",
    )
    password: Optional[str] = Field(
        None,
        description="Optional password used with credentials mode.",
    )

    creation_type: ShellCreationType = Field(
        default=ShellCreationType.current_user,
        description="How to create the shell session",
    )


class RunCommand(BaseModel):
    command: str = Field(..., description="The command to be executed.")
