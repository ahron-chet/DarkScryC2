import uuid

from pydantic import BaseModel, Field


class TaskOut(BaseModel):
    """Simple task identifier response."""

    task_id: uuid.UUID = Field(..., description="Job identifier")
