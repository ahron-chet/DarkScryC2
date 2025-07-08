import uuid

from pydantic import BaseModel, Field


class RunCommandIn(BaseModel):
    """Input schema for running a command on an agent."""

    command: str = Field(..., description="Command to execute")


class TaskOut(BaseModel):
    """Simple task identifier response."""

    task_id: uuid.UUID = Field(..., description="Job identifier")
