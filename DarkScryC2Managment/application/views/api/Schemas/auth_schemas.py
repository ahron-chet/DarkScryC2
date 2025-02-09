from pydantic import field_validator, Field
from typing import Optional
from ....services.schema_manager import SchemaManager
from ....Utils.utils import is_password_complex
from ninja import Schema


class UserRegistration(SchemaManager):
    first_name: str = Field(..., max_length=50, description="The first name of the user. Cannot be null.")
    last_name: str = Field(..., max_length=50, description="The last name of the user. Cannot be null.")
    username: str = Field(..., max_length=50, description="A unique username for the user. Cannot be null.")
    password: str = Field(..., max_length=50, description="The password of the user. Cannot be null.")
    role: str = Field(..., max_length=20, description="The role assigned to the user. Cannot be null.")
    otpuri: str = Field(..., max_length=250, description="The OTP URI for the user. Cannot be null.")
    company_name: Optional[str] = Field(None, max_length=100, description="The name of the company, if applicable.")
    industry: Optional[str] = Field(None, max_length=100, description="The industry associated with the user, if applicable.")
    country: Optional[str] = Field(None, max_length=50, description="The country of the user, if provided.")


    field_validator("password")
    def validate_passeord(cls, v):
        if not is_password_complex(v):
            raise ValueError("Password dosnt meet the complexity.")
        return v
    

class LoginSchema(SchemaManager):
    username: str = Field(..., max_length=50, description="A unique username for the user. Cannot be null.")
    password: str = Field(..., max_length=50, description="The password of the user. Cannot be null.")





class LoginSchemaV2(Schema):
    username: str = Field(..., max_length=50, description="A unique username for the user. Cannot be null.")
    password: str = Field(..., max_length=50, description="The password of the user. Cannot be null.")

class V2LoginResponseSchema(Schema):
    token: str = Field(..., description="JWT authentication token for the user")
    token_type: str = Field(default="Bearer", description="The type of the authentication token")
    expires_in: int = Field(default=3600, description="Token expiration time in seconds")
    refresh_token: str = Field(..., description="The long-lived refresh token (JWT).")

class V2RefreshRequestSchema(Schema):
    refresh_token: str = Field(..., description="The refresh token previously provided at login.")
    

class V2RefreshResponseSchema(Schema):
    token: str = Field(..., description="A new, short-lived access token (JWT).")
    expires_in: int = Field(..., description="Number of seconds until the new access token expires.")
