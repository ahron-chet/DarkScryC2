from functools import lru_cache

from pydantic import ConfigDict, Field, field_validator, model_validator
from pydantic_settings import BaseSettings


class ArqSettings(BaseSettings):
    """Settings required only for ARQ worker processes."""

    redis_host: str = Field(
        "localhost",
        description="Redis server hostname",
        validation_alias="MANAGEMENT_REDIS_HOST",
    )
    redis_port: int = Field(
        6379,
        description="Redis server port",
        validation_alias="MANAGEMENT_REDIS_PORT",
    )
    redis_password: str | None = Field(
        None,
        description="Redis password",
        validation_alias="MANAGEMENT_REDIS_PASSWORD",
    )
    arq_redis_db: int = Field(
        4,
        description="Database index for ARQ tasks",
        validation_alias="MANAGEMENT_ARQ_REDIS_DB",
    )
    model_config = ConfigDict(env_file=None, extra="ignore", populate_by_name=True)


class AppSettings(BaseSettings):
    """Main application settings, required only for application processes."""

    database_url: str | None = Field(
        None,
        description="Database connection URL",
        validation_alias="MANAGEMENT_DATABASE_URL",
    )
    db_user: str = Field(
        "default_user",
        description="Database username",
        validation_alias="DB_USER",
    )
    db_name: str = Field(
        "default_db_name",
        description="Database name",
        validation_alias="DB_NAME",
    )
    db_host: str = Field(
        "localhost",
        description="Database host",
        validation_alias="DB_HOST",
    )
    db_port: int = Field(
        5432,
        description="Database port",
        validation_alias="DB_PORT",
    )
    db_password: str = Field(
        "",
        description="Database password",
        validation_alias="DB_PASSWORD",
    )
    secret_key: str = Field(
        ...,
        description="JWT signing secret",
        validation_alias="MANAGEMENT_SECRET_KEY",
    )
    debug: bool = Field(
        False,
        description="Enable debug mode",
        validation_alias="MANAGEMENT_DEBUG",
    )
    access_token_expire_minutes: int = Field(
        15,
        description="Access token expiration window in minutes",
        validation_alias="MANAGEMENT_JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
    )
    refresh_token_expire_days: int = Field(
        9,
        description="Refresh token expiration window in days",
        validation_alias="MANAGEMENT_JWT_REFRESH_TOKEN_EXPIRE_DAYS",
    )
    jwt_issuer: str = Field(
        "management",
        description="Expected issuer claim for JWTs",
        validation_alias="MANAGEMENT_JWT_ISSUER",
    )
    jwt_audience: str = Field(
        "management-client",
        description="Expected audience claim for JWTs",
        validation_alias="MANAGEMENT_JWT_AUDIENCE",
    )
    cors_origins: list[str] = Field(
        [],
        description="Allowed CORS origins",
        validation_alias="MANAGEMENT_CORS_ORIGINS",
    )

    model_config = ConfigDict(env_file=None, extra="ignore", populate_by_name=True)

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [c.strip() for c in v.split(",") if c.strip()]
        return v

    @model_validator(mode="after")
    def build_database_url(self) -> "AppSettings":
        if not self.database_url:
            self.database_url = (
                f"postgresql+asyncpg://{self.db_user}:{self.db_password}@"
                f"{self.db_host}:{self.db_port}/{self.db_name}"
            )
        return self


# Separate cached getters:


@lru_cache()
def get_arq_settings() -> ArqSettings:
    """Get ARQ-specific settings."""
    return ArqSettings()


@lru_cache()
def get_app_settings() -> AppSettings:
    """Get main application settings."""
    settings = AppSettings()
    if settings.debug:
        settings.access_token_expire_minutes = 60 * 24
    return settings
