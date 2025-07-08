"""Application settings loaded from environment variables."""

from functools import lru_cache

from pydantic import ConfigDict, Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    database_url: str = Field(
        ..., 
        description="Database connection URL", 
        validation_alias="DATABASE_URL"
    )
    secret_key: str = Field(
        ..., 
        description="JWT signing secret", 
        validation_alias="SECRET_KEY"
    )
    debug: bool = Field(
        False, 
        description="Enable debug mode", 
        validation_alias="DEBUG"
    )
    access_token_expire_minutes: int = Field(
        15,
        description="Access token expiration window in minutes",
        validation_alias="JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
    )
    refresh_token_expire_days: int = Field(
        9,
        description="Refresh token expiration window in days",
        validation_alias="JWT_REFRESH_TOKEN_EXPIRE_DAYS",
    )
    jwt_issuer: str = Field(
        "management",
        description="Expected issuer claim for JWTs",
        validation_alias="JWT_ISSUER",
    )
    jwt_audience: str = Field(
        "management-client",
        description="Expected audience claim for JWTs",
        validation_alias="JWT_AUDIENCE",
    )
    cors_origins: list[str] = Field(
        [],
        description="Allowed CORS origins",
        validation_alias="CORS_ORIGINS"
    )

    # Redis connection settings used for background task queue
    redis_host: str = Field(
        "redis", 
        description="Redis server hostname",
        validation_alias="REDIS_HOST"
    )
    redis_port: int = Field(
        6379, 
        description="Redis server port",
        validation_alias="REDIS_PORT"
    )
    redis_password: str | None = Field(
        None, 
        description="Redis password",
        validation_alias="REDIS_PASSWORD"
    )
    arq_redis_db: int = Field(
        4, 
        description="Database index for ARQ tasks",
        validation_alias="ARQ_REDIS_DB"
    )

    model_config = ConfigDict(env_file=None, extra="ignore", env_prefix="MANAGEMENT_", populate_by_name=True)

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [c.strip() for c in v.split(",") if c.strip()]
        return v

@lru_cache()
def get_settings() -> Settings:
    """Return application settings or raise if required variables are missing."""

    settings = Settings()
    if settings.debug:
        settings.access_token_expire_minutes = 60 * 24

    return settings



