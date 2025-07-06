"""Application settings loaded from environment variables."""

import os
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    database_url: str = Field(..., description="Database connection URL")
    secret_key: str = Field(..., description="JWT signing secret")
    debug: bool = Field(False, description="Enable debug mode")

    model_config = {
        "env_file": None,
        "extra": "ignore",
    }


@lru_cache()
def get_settings() -> Settings:
    """Return application settings or raise if required variables are missing."""

    db_url = os.getenv("MANAGEMENT_DATABASE_URL")
    if not db_url:
        raise RuntimeError("MANAGEMENT_DATABASE_URL is not set")

    secret_key = os.getenv("MANAGEMENT_SECRET_KEY")
    if not secret_key:
        raise RuntimeError("MANAGEMENT_SECRET_KEY is not set")

    debug = os.getenv("MANAGEMENT_DEBUG", "False").lower() == "true"
    return Settings(database_url=db_url, secret_key=secret_key, debug=debug)
