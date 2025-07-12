import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class AgentCreate(BaseModel):
    """Schema for creating a new agent."""

    host_name: str = Field(..., description="Hostname of the agent")
    os: str = Field(..., description="Operating system")


class AgentUpdate(BaseModel):
    """Schema for updating an existing agent."""

    host_name: Optional[str] = Field(None, description="Hostname of the agent")
    os: Optional[str] = Field(None, description="Operating system")


class AgentRead(BaseModel):
    """Public representation of an agent."""

    agent_id: uuid.UUID = Field(..., description="Public UUID of the agent")
    host_name: str = Field(..., description="Hostname of the agent")
    os: str = Field(..., description="Operating system")
    last_time_update: Optional[datetime] = Field(
        None, description="Last update timestamp"
    )
    onboarded_time: Optional[datetime] = Field(
        None, description="Time the agent was onboarded"
    )
    is_active: bool = Field(
        False,
        description="Whether the agent currently has an active connection",
    )
    address: Optional[str] = Field(
        None,
        description="Last known remote address for the agent",
    )

    model_config = ConfigDict(from_attributes=True)


class Deleted(BaseModel):
    """Confirmation response for delete operations."""

    detail: str = Field("Deleted successfully", description="Status message")
