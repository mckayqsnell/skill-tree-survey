"""
Pydantic schemas for SurveySession model.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class SessionBase(BaseModel):
    """Base schema for SurveySession."""
    user_name: str = Field(..., min_length=1, max_length=100, description="User's name")
    user_email: EmailStr = Field(..., description="User's email address")
    company: Optional[str] = Field(None, max_length=100, description="Company name")


class SessionCreate(SessionBase):
    """Schema for creating a SurveySession."""
    pass


class SessionUpdate(BaseModel):
    """Schema for updating a SurveySession."""
    completed_at: Optional[datetime] = None


class SessionResponse(SessionBase):
    """Schema for SurveySession response."""
    id: int
    started_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class SessionSummary(SessionResponse):
    """Schema for session summary with statistics."""
    is_completed: bool
    completion_time_minutes: Optional[float]
    total_responses: int
    yes_responses: int
    no_responses: int


class SessionWithResponses(SessionResponse):
    """Schema for session with responses."""
    responses: List["ResponseBase"] = []
    
    class Config:
        from_attributes = True


class SessionAnalytics(BaseModel):
    """Schema for session analytics."""
    total_sessions: int
    completed_sessions: int
    completion_rate: float
    average_completion_time_minutes: Optional[float]
    unique_users: int


class UserSkillsSummary(BaseModel):
    """Schema for user skills summary."""
    email: str
    name: Optional[str]
    company: Optional[str]
    total_sessions: int
    completed_sessions: int
    latest_session: Optional[int]
    skills: List[Dict[str, Any]]


class CategoryStatistics(BaseModel):
    """Schema for category-based response statistics."""
    category: str
    yes_count: int
    no_count: int
    total: int


class SkillDepthAnalysis(BaseModel):
    """Schema for skill depth analysis."""
    depth_distribution: Dict[str, int]
    max_depths_by_category: Dict[str, int]
    average_depth: float


# Import at the end to avoid circular dependency
from app.schemas.response import ResponseBase

# Update forward references
SessionWithResponses.model_rebuild()