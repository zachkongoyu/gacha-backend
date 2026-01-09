"""Shared settings configuration using pydantic-settings."""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Database
    database_url: str = "postgresql+asyncpg://gacha_user:gacha_password@localhost:5432/gacha_db"
    postgres_user: str = "gacha_user"
    postgres_password: str = "gacha_password"
    postgres_db: str = "gacha_db"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # JWT
    jwt_secret_key: str = "your-secret-key-change-this-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30

    # OAuth
    oauth_client_id: Optional[str] = None
    oauth_client_secret: Optional[str] = None
    oauth_authorize_url: str = "https://accounts.google.com/o/oauth2/v2/auth"
    oauth_token_url: str = "https://oauth2.googleapis.com/token"
    oauth_userinfo_url: str = "https://www.googleapis.com/oauth2/v2/userinfo"
    oauth_redirect_uri: str = "http://localhost:8000/auth/callback"

    # Service URLs
    auth_service_url: str = "http://localhost:8001"
    gacha_service_url: str = "http://localhost:8002"
    inventory_service_url: str = "http://localhost:8003"
    ai_service_url: str = "http://localhost:8004"
    asset_service_url: str = "http://localhost:8005"

    # Environment
    environment: str = "development"


# Global settings instance
settings = Settings()
