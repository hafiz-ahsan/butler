"""Configuration settings for Butler service."""

from functools import lru_cache
from typing import Any, Dict, Optional

from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    app_name: str = "Butler"
    app_version: str = "0.1.0"
    debug: bool = False

    # Server settings
    host: str = "127.0.0.1"
    port: int = 8000
    workers: int = 1
    reload: bool = False

    # Database settings
    database_url: str = Field(
        default="postgresql+asyncpg://butler:password@localhost:5432/butler",
        description="Database connection URL",
    )

    # Redis settings
    redis_url: str = Field(
        default="redis://localhost:6379/0", description="Redis connection URL"
    )

    # JWT settings
    secret_key: str = Field(
        default="your-secret-key-change-in-production",
        description="Secret key for JWT tokens",
    )
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # AI Service API Keys
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    google_ai_api_key: Optional[str] = None

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"

    # CORS settings
    allowed_origins: list[str] = ["http://localhost:3000", "http://localhost:8080"]
    allowed_methods: list[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    allowed_headers: list[str] = ["*"]

    # Rate limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_period: int = 60

    @validator("allowed_origins", pre=True)
    def parse_origins(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()
