"""
Category-related Pydantic schemas.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CategoryOrderBase(BaseModel):
    """Base schema for category order."""

    category: str
    order_index: int


class CategoryOrderCreate(CategoryOrderBase):
    """Schema for creating category order."""

    pass


class CategoryOrderUpdate(BaseModel):
    """Schema for updating category order."""

    order_index: int


class CategoryOrderResponse(CategoryOrderBase):
    """Schema for category order response."""

    id: int
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CategoryOrderBulkUpdate(BaseModel):
    """Schema for bulk updating category orders."""

    categories: list[CategoryOrderBase]
