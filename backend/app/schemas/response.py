"""
Pydantic schemas for Response model.
"""
from datetime import datetime
from pydantic import BaseModel, Field


class ResponseBase(BaseModel):
    """Base schema for Response."""
    session_id: int = Field(..., description="Survey session ID")
    question_id: int = Field(..., description="Question ID")
    answer: bool = Field(..., description="Answer (True for yes, False for no)")


class ResponseCreate(BaseModel):
    """Schema for creating a Response."""
    question_id: int = Field(..., description="Question ID")
    answer: bool = Field(..., description="Answer (True for yes, False for no)")


class ResponseUpdate(BaseModel):
    """Schema for updating a Response."""
    answer: bool = Field(..., description="Updated answer")


class ResponseInDB(ResponseBase):
    """Schema for Response in database."""
    id: int
    answered_at: datetime
    
    class Config:
        from_attributes = True


class ResponseWithQuestion(ResponseInDB):
    """Schema for Response with question details."""
    question_text: str
    question_category: str
    question_depth: int


class BulkResponseCreate(BaseModel):
    """Schema for creating multiple responses."""
    session_id: int = Field(..., description="Survey session ID")
    responses: list[ResponseCreate] = Field(..., min_length=1, description="List of responses")