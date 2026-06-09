"""
Pydantic schemas for SurveySession model.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SessionBase(BaseModel):
    """Base schema for SurveySession."""

    user_name: str = Field(..., min_length=1, max_length=100, description="User's name")
    user_email: EmailStr = Field(..., description="User's email address")
    company: str | None = Field(None, max_length=100, description="Company name")


class SessionCreate(SessionBase):
    """Schema for creating a SurveySession."""

    pass


class SessionUpdate(BaseModel):
    """Schema for updating a SurveySession."""

    completed_at: datetime | None = None


class SessionResponse(SessionBase):
    """Schema for SurveySession response."""

    id: int
    started_at: datetime
    completed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class SessionSummary(SessionResponse):
    """Schema for session summary with statistics."""

    is_completed: bool
    completion_time_minutes: float | None
    total_responses: int
    yes_responses: int
    no_responses: int


class SessionWithResponses(SessionResponse):
    """Schema for session with responses."""

    responses: list["ResponseBase"] = []

    model_config = ConfigDict(from_attributes=True)


class SessionAnalytics(BaseModel):
    """Schema for session analytics."""

    total_sessions: int
    completed_sessions: int
    completion_rate: float
    average_completion_time_minutes: float | None
    unique_users: int


class UserSkillsSummary(BaseModel):
    """Schema for user skills summary."""

    email: str
    name: str | None
    company: str | None
    total_sessions: int
    completed_sessions: int
    latest_session: int | None
    skills: list[dict[str, Any]]


class CategoryStatistics(BaseModel):
    """Schema for category-based response statistics."""

    category: str
    yes_count: int
    no_count: int
    total: int


class SkillDepthAnalysis(BaseModel):
    """Schema for skill depth analysis."""

    depth_distribution: dict[str, int]
    max_depths_by_category: dict[str, int]
    average_depth: float


# Import at the end to avoid circular dependency
from app.schemas.response import ResponseBase  # noqa: E402

# Update forward references
SessionWithResponses.model_rebuild()
