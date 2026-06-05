"""
Pydantic schemas for Question model.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class QuestionBase(BaseModel):
    """Base schema for Question."""

    text: str = Field(..., min_length=1, description="Question text")
    parent_id: int | None = Field(None, description="Parent question ID")
    is_base: bool = Field(False, description="Whether this is a base question")
    category: str | None = Field(None, max_length=50, description="Question category")
    order_index: int = Field(0, ge=0, description="Order within same parent level")


class QuestionCreate(QuestionBase):
    """Schema for creating a Question."""

    pass


class QuestionUpdate(BaseModel):
    """Schema for updating a Question."""

    text: str | None = Field(None, min_length=1)
    parent_id: int | None = None
    is_base: bool | None = None
    category: str | None = Field(None, max_length=50)
    order_index: int | None = Field(None, ge=0)


class QuestionResponse(QuestionBase):
    """Schema for Question response."""

    id: int
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class QuestionWithChildren(QuestionResponse):
    """Schema for Question with children."""

    children: list["QuestionWithChildren"] = []

    model_config = ConfigDict(from_attributes=True)


class QuestionTree(BaseModel):
    """Schema for question tree structure."""

    id: int
    text: str
    is_base: bool
    category: str | None
    order_index: int
    children: list["QuestionTree"] = []


class QuestionReorder(BaseModel):
    """Schema for reordering questions."""

    parent_id: int | None = Field(
        None, description="Parent ID (None for base questions)"
    )
    question_ids: list[int] = Field(
        ..., min_length=1, description="Ordered list of question IDs"
    )


class QuestionMove(BaseModel):
    """Schema for moving a question."""

    question_id: int = Field(..., description="Question to move")
    new_parent_id: int | None = Field(
        None, description="New parent (None for base level)"
    )


class QuestionStatistics(BaseModel):
    """Schema for question response statistics."""

    question_id: int
    total_responses: int
    yes_count: int
    no_count: int
    yes_percentage: float
    no_percentage: float


# Update forward references
QuestionWithChildren.model_rebuild()
QuestionTree.model_rebuild()
