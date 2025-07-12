import uuid
from datetime import datetime
from typing import Any

from arq.jobs import JobStatus
from darkscryc2server.models.messages import CommandIdentifiers
from pydantic import BaseModel, ConfigDict, Field


class TaskOut(BaseModel):
    """Simple task identifier response."""

    task_id: uuid.UUID = Field(..., description="Job identifier")


class TaskStatusOut(BaseModel):
    """Current status of an enqueued job."""

    status: JobStatus = Field(..., description="The current status of the job")
    job_id: uuid.UUID = Field(..., description="Job identifier")


class TaskResultOut(BaseModel):
    """Detailed information about a finished job."""

    success: bool = Field(..., description="Whether the task succeeded")
    result: Any = Field(..., description="Task result payload")
    start_time: datetime = Field(..., description="When the task started")
    finish_time: datetime = Field(..., description="When the task finished")
    action: CommandIdentifiers | None = Field(
        None, description="Action identifier the job executed"
    )
    job_id: uuid.UUID = Field(..., description="Job identifier")

    model_config = ConfigDict(use_enum_values=True)
