"""Shared pytest fixtures and configuration.

Point the app at a throwaway SQLite file BEFORE any app module is imported, so tests
never touch a developer's real database. Env vars are set at import time because the
settings singleton and SQLAlchemy engine are created at module import.
"""

import os

os.environ.setdefault("DATABASE_URL", "sqlite:////tmp/skill_survey_test.db")
os.environ.setdefault("RESET_DATABASE", "true")
os.environ.setdefault("ENVIRONMENT", "test")
