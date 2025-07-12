from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    host: str = Field("0.0.0.0", alias="C2_SERVER_HOST")
    port: int = Field(9100, alias="C2_SERVER_PORT")
    ws_port: int = Field(876, alias="C2_SERVER_WS_PORT")

    redis_host: str = Field("localhost", alias="C2_SERVER_REDIS_HOST")
    redis_password: str | None = Field(None, alias="C2_SERVER_REDIS_PASSWORD")
    redis_db: int = Field(1, alias="C2_SERVER_REDIS_DB")

    ssl_cert: str | None = Field(None, alias="C2_SERVER_SSL_CERT")
    ssl_key: str | None = Field(None, alias="C2_SERVER_SSL_KEY")

    model_config = SettingsConfigDict(
        env_file=None, 
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @computed_field
    @property
    def redis_url(self) -> str:
        if self.redis_password:
            return f"redis://:{self.redis_password}@{self.redis_host}:6379/{self.redis_db}"
        return f"redis://{self.redis_host}:6379/{self.redis_db}"


settings = Settings()
