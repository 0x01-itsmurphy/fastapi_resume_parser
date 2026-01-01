"""
Core configuration management for FastAPI Resume Parser.
"""
from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application Configuration
    app_name: str = "FastAPI Resume Parser"
    app_version: str = "2.0.0"
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
    allow_credentials: bool = True
    
    # Geocoding Configuration
    geocoding_user_agent: str = "resume-parser-api"
    geocoding_timeout: int = 5
    
    # Logging Configuration
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_file: str = "logs/app.log"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance.
    
    Returns:
        Settings instance
    """
    return Settings()


# Global settings instance
settings = get_settings()
