from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class CredentialType(str, Enum):
    PASSWORD = "password"
    COOKIES = "cookies"


# A single decrypted password record
class PasswordRecord(BaseModel):
    url: str = Field(..., description="The website or service URL where the credential was used.")
    created: str = Field(..., description="The timestamp when the credential was created.")
    last_used: str = Field(..., description="The timestamp when the credential was last used.")
    username: str = Field(..., description="The username associated with the credential.")
    password: str = Field(..., description="The decrypted password.")


# Per-profile result: which profile, and a list of password records
class ProfileResult(BaseModel):
    profile: str = Field(..., description="The profile name (e.g., 'Default', 'Profile 1').")
    credentials: List[PasswordRecord] = Field(..., description="List of decrypted password records for this profile.")


# Per-browser result: which browser, and the profile results
class BrowserResult(BaseModel):
    browser: str = Field(..., description="The name of the browser (e.g., 'Chrome', 'Firefox').")
    profiles: List[ProfileResult] = Field(..., description="List of profiles associated with this browser.")


class GatherCredentialsResult(BaseModel):
    browsers: List[BrowserResult] = Field(..., description="List of gathered credentials grouped by browser.")
