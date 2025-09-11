"""
Application configuration using Pydantic settings.
"""
from typing import List, Optional, Union
from pydantic_settings import BaseSettings
from pydantic import field_validator
from functools import lru_cache
import json


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    DATABASE_URL: str = "sqlite:///./skill_survey.db"
    
    # Admin
    ADMIN_PASSWORD: str = "admin123"
    
    # CORS
    CORS_ORIGINS: Union[List[str], str] = ["http://localhost:5173", "http://localhost:3000"]
    
    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            # Try to parse as JSON
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                # If not JSON, treat as comma-separated list
                return [origin.strip() for origin in v.split(',')]
        return v
    
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