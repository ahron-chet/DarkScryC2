from pydantic import BaseModel, Field


class Token(BaseModel):
    """JWT tokens returned after successful authentication."""

    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")


class Login(BaseModel):
    """Credentials required to obtain an access token."""

    username: str = Field(..., description="User login name")
    password: str = Field(..., description="User password")


class RefreshTokenRequest(BaseModel):
    """Schema for requesting a new access token."""

    refresh_token: str = Field(..., description="JWT refresh token")
