from uuid import UUID
from typing import List, Optional
from ninja import Schema, Field
from datetime import datetime

class UserCreateSchema(Schema):
    username: str = Field(..., description="The username (or email) for the new user")
    password: str = Field(..., description="The password for the new user")
    email: str = Field(..., description="The email of the new user")
    role: str = Field(default="user", description="Role of the user (default 'user')")
    first_name: str = Field(..., description="Optional first name")
    last_name: str = Field(..., description="Optional last name")
    company_name: Optional[str] = Field(None, description="Company name of the user")
    industry: Optional[str] = Field(None, description="Industry of the user")
    country: Optional[str] = Field(None, description="Country of the user")


class UserUpdateSchema(Schema):
    username: Optional[str] = Field(None, description="Update username (or email)")
    password: Optional[str] = Field(None, description="Update the user's password")
    email: Optional[str] = Field(None, description="Update the user's email")
    role: Optional[str] = Field(None, description="Update the user's role")
    first_name: Optional[str] = Field(None, description="Update the user's first name")
    last_name: Optional[str] = Field(None, description="Update the user's last name")
    company_name: Optional[str] = Field(None, description="Update the user's company name")
    industry: Optional[str] = Field(None, description="Update the user's industry")
    country: Optional[str] = Field(None, description="Update the user's country")
    otpuri: Optional[str] = Field(None, description="Update the user's OTP URI")


class UserOutSchema(Schema):
    user_id: UUID = Field(..., description="Unique ID of the user (UUID)")
    username: str = Field(..., description="Username of the user")
    email: str = Field(..., description="Email address of the user")
    role: str = Field(..., description="Role of the user")
    first_name: str = Field(..., description="First name of the user")
    last_name: str = Field(..., description="Last name of the user")
    company_name: Optional[str] = Field(None, description="Company name of the user")
    industry: Optional[str] = Field(None, description="Industry of the user")
    country: Optional[str] = Field(None, description="Country of the user")
    time_generated: Optional[datetime] = Field(None, description="Time when user was created")
    last_login: Optional[datetime] = Field(None, description="Last login time of the user")



