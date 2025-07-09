from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    host: str = "0.0.0.0"
    port: int = 9100
    redis_url: str = "redis://localhost:6379/0"
    ws_port: int = 876
    ssl_cert: str | None = None
    ssl_key: str | None = None

    model_config = SettingsConfigDict(
        env_prefix="C2_SERVER_", env_file=".env", env_file_encoding="utf-8"
    )


settings = Settings()  # type: ignore
