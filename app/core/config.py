"""
Core configuration management for FastAPI Resume Parser.
"""

from functools import lru_cache
from typing import Any, List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application Configuration
    app_name: str = "FastAPI Resume Parser"
    app_version: str = "2.1.0"
    debug: bool = False

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1
    log_level: str = "info"

    # File Upload Configuration
    max_file_size: int = 10485760  # 10MB in bytes
    allowed_extensions: List[str] = [".pdf"]

    # CORS Configuration
    cors_origins: List[str] = ["*"]
    cors_methods: List[str] = ["*"]
    cors_headers: List[str] = ["*"]
    allow_credentials: bool = False

    # Logging Configuration
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_file: str = "logs/app.log"

    @field_validator("debug", "allow_credentials", mode="before")
    @classmethod
    def parse_bool(cls, value: Any) -> Any:
        """Accept common boolean-like deployment values."""
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"1", "true", "yes", "on", "debug", "development", "dev"}:
                return True
            if normalized in {"0", "false", "no", "off", "release", "production", "prod"}:
                return False
        return value

    @field_validator(
        "allowed_extensions", "cors_origins", "cors_methods", "cors_headers", mode="before"
    )
    @classmethod
    def parse_list(cls, value: Any) -> Any:
        """Allow comma-separated environment values for list settings."""
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance.

    Returns:
        Settings instance
    """
    return Settings()


# Global settings instance
settings = get_settings()
