from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    c2_server_host: str = Field(..., env="C2_SERVER_HOST")
    c2_server_port: int = Field(..., env="C2_SERVER_PORT")
    redis_url: str = Field(..., env="REDIS_URL")
    ws_port: int = Field(876, env="C2_WS_PORT")
    ssl_cert: str | None = Field(None, env="SSL_CERTIFICATE")
    ssl_key: str | None = Field(None, env="SSL_CERTIFICATE_KEY")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()  # type: ignore
