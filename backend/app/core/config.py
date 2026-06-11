"""
Application configuration using Pydantic settings.

This module centralizes all application settings and the shared structured logger.
Environment variables are loaded from .env files (generated from 1Password via
`task env:generate`) and the system environment.

Usage throughout the app:

    from app.core.config import settings

    logger = settings.logger
    logger.info("Something happened", session_id=session.id)

To add a new setting: add the field below, add the matching item to your 1Password
vault, then re-run `task env:generate`.
"""

import json
import logging
from functools import lru_cache
from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from python_sentry_logger_wrapper import get_logger


class Settings(BaseSettings):
    """Application settings loaded from environment variables (case-sensitive, UPPER_SNAKE_CASE)."""

    # -------------------------------------------------------------------------
    # Database
    # -------------------------------------------------------------------------
    DATABASE_URL: str = "sqlite:///./skill_survey.db"

    # -------------------------------------------------------------------------
    # Admin
    # -------------------------------------------------------------------------
    ADMIN_PASSWORD: str = "admin123"

    # -------------------------------------------------------------------------
    # CORS - accepts a JSON array or comma-separated string
    # -------------------------------------------------------------------------
    CORS_ORIGINS: list[str] | str = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> Any:
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [origin.strip() for origin in v.split(",")]
        return v

    # -------------------------------------------------------------------------
    # Database management
    # -------------------------------------------------------------------------
    RESET_DATABASE: bool = False

    # -------------------------------------------------------------------------
    # API
    # -------------------------------------------------------------------------
    API_PREFIX: str = "/api"

    # -------------------------------------------------------------------------
    # Application
    # -------------------------------------------------------------------------
    APP_NAME: str = "Skill Tree Survey"
    APP_VERSION: str = "1.1.0"
    DEBUG: bool = False

    # -------------------------------------------------------------------------
    # Environment & logging
    # -------------------------------------------------------------------------
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "info"

    # -------------------------------------------------------------------------
    # Sentry (optional - production only). Leave SENTRY_DSN unset to disable.
    # -------------------------------------------------------------------------
    SENTRY_DSN: str | None = None
    SENTRY_ENVIRONMENT: str | None = None
    SENTRY_SAMPLE_RATE: float = 1.0
    SENTRY_SEND_PII: bool = False
    SENTRY_BREADCRUMBS_LEVEL: str | None = None
    SENTRY_LOG_LEVEL: str | None = None

    # === task env:add inserts new settings above this line ===

    # -------------------------------------------------------------------------
    # Shared structured logger (initialized in get_settings, after env load)
    # -------------------------------------------------------------------------
    logger: Any | None = None

    model_config = SettingsConfigDict(
        # Later files win. Includes the repo-root .env.local that
        # `task env:generate` writes, so `cd backend && uv run uvicorn ...`
        # picks up generated values too (missing files are ignored).
        env_file=(".env", "../.env.local", ".env.local"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


_LOG_LEVEL_MAP = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}

# Environments treated as "local" (no Sentry health-check filtering, etc.)
LOCAL_ENVIRONMENTS = ("local", "development", "dev")


@lru_cache
def get_settings() -> Settings:
    """Return the cached application settings singleton, with the logger attached.

    The Sentry-backed structured logger is initialized once here. Sentry is only
    enabled when SENTRY_DSN is set (so local development logs to stdout only).
    """
    settings = Settings()

    # Fail fast on insecure production deploys: the dev default is fine locally,
    # but production must set a real ADMIN_PASSWORD (1Password -> .env.prod).
    if settings.ENVIRONMENT == "production" and settings.ADMIN_PASSWORD == "admin123":
        raise ValueError(
            "ADMIN_PASSWORD is still the dev default in production. "
            "Set it in the SKILL-TREE-PROD vault and redeploy (task prod:deploy)."
        )

    log_level = _LOG_LEVEL_MAP.get(settings.LOG_LEVEL.lower(), logging.INFO)
    sentry_logs_level = (
        _LOG_LEVEL_MAP.get(settings.SENTRY_LOG_LEVEL.lower(), logging.INFO)
        if settings.SENTRY_LOG_LEVEL
        else logging.INFO
    )
    sentry_breadcrumbs_level = (
        _LOG_LEVEL_MAP.get(settings.SENTRY_BREADCRUMBS_LEVEL.lower(), logging.ERROR)
        if settings.SENTRY_BREADCRUMBS_LEVEL
        else logging.ERROR
    )

    settings.logger = get_logger(
        service_name=settings.APP_NAME,
        log_level=log_level,
        sentry_dsn=settings.SENTRY_DSN,
        sentry_breadcrumbs_level=sentry_breadcrumbs_level,
        sentry_logs_level=sentry_logs_level,
        sentry_environment=settings.SENTRY_ENVIRONMENT or settings.ENVIRONMENT,
        traces_sample_rate=settings.SENTRY_SAMPLE_RATE,
        sentry_send_pii=settings.SENTRY_SEND_PII,
    )
    return settings


# Singleton imported throughout the application: `from app.core.config import settings`
settings = get_settings()
