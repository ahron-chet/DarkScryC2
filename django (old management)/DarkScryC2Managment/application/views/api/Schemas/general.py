from ninja import Schema
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Any
from darkscryc2server.Models.schemas import CommandIdentifiersName
from arq.jobs import JobStatus


class SuccessBase(Schema):
    detail: str

class DeletedSuccessfully(SuccessBase):
    # default value for the detail field:
    detail: str = "Deleted successfully"

class EditedSuccessfully(SuccessBase):
    detail: str = "Edited successfully"

class CreatedSuccessfully(SuccessBase):
    detail: str = "Created successfully"



class Unauthorize(Schema):
    detail: str = Field(default="User name or password is incorrect")


class TaskOut(Schema):
    """
    Schema to represent a task with its unique identifier.
    """
    task_id: UUID = Field(..., description="The unique identifier for the task.")





class TaskStatusOut(BaseModel):
    """
    Schema to represent the current status of a task.
    """
    status: JobStatus = Field(..., description="The current status of the job.")
    job_id: UUID = Field(..., description="The unique identifier of the job.")


class TaskResultOut(BaseModel):
    """
    Schema to represent the result of a task.
    """
    success: bool = Field(..., description="Indicates whether the task completed successfully.")
    result: Any = Field(..., description="The result or output of the task. This can be of any type depending on the task.")
    start_time: datetime = Field(..., description="The timestamp when the task started.")
    finish_time: datetime = Field(..., description="The timestamp when the task finished.")
    action: CommandIdentifiersName = Field(..., description="The name identifier of the action the job was processed in.")
    job_id: UUID = Field(..., description="The unique identifier of the job.")
    

    model_config = ConfigDict(use_enum_values=True)


class GeneralError(BaseModel):
    error:str