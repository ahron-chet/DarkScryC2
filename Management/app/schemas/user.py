import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from ..models.user import UserRole


class UserCreate(BaseModel):
    """Schema for creating a new user."""

    username: str = Field(..., description="Unique username")
    password: str = Field(..., description="Login password")
    email: str = Field(..., description="Email address")
    role: UserRole = Field(default=UserRole.READER, description="Assigned role")
    first_name: Optional[str] = Field(None, description="Given name")
    last_name: Optional[str] = Field(None, description="Family name")
    company_name: Optional[str] = Field(None, description="Company affiliation")
    industry: Optional[str] = Field(None, description="Industry sector")
    country: Optional[str] = Field(None, description="Country of residence")


class UserUpdate(BaseModel):
    """Schema for updating existing users."""

    username: Optional[str] = Field(None, description="Unique username")
    password: Optional[str] = Field(None, description="Login password")
    email: Optional[str] = Field(None, description="Email address")
    role: Optional[UserRole] = Field(None, description="Assigned role")
    first_name: Optional[str] = Field(None, description="Given name")
    last_name: Optional[str] = Field(None, description="Family name")
    company_name: Optional[str] = Field(None, description="Company affiliation")
    industry: Optional[str] = Field(None, description="Industry sector")
    country: Optional[str] = Field(None, description="Country of residence")
    otpuri: Optional[str] = Field(None, description="OTP URI")


class UserRead(BaseModel):
    """Public representation of a user."""

    user_id: uuid.UUID = Field(..., description="Public UUID of the user")
    username: str = Field(..., description="Unique username")
    email: Optional[str] = Field(None, description="Email address")
    role: UserRole = Field(..., description="Assigned role")
    first_name: Optional[str] = Field(None, description="Given name")
    last_name: Optional[str] = Field(None, description="Family name")
    company_name: Optional[str] = Field(None, description="Company affiliation")
    industry: Optional[str] = Field(None, description="Industry sector")
    country: Optional[str] = Field(None, description="Country of residence")
    time_generated: Optional[datetime] = Field(None, description="Creation time")
    last_login: Optional[datetime] = Field(None, description="Last login time")

    model_config = ConfigDict(from_attributes=True)


class Deleted(BaseModel):
    """Confirmation response for delete operations."""

    detail: str = Field("Deleted successfully", description="Status message")
