"""
Application configuration using Pydantic settings.
"""
from typing import List, Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    DATABASE_URL: str = "sqlite:///./skill_survey.db"
    
    # Admin
    ADMIN_PASSWORD: str = "admin123"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # Seeding
    SEED_ON_STARTUP: bool = True
    
    # API
    API_PREFIX: str = "/api"
    
    # Application
    APP_NAME: str = "Skill Tree Survey"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached application settings.
    
    Returns:
        Settings: Application settings instance
    """
    return Settings()