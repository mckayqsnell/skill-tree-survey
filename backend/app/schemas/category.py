"""
Category-related Pydantic schemas.
"""
from typing import List
from pydantic import BaseModel
from datetime import datetime


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

    class Config:
        from_attributes = True


class CategoryOrderBulkUpdate(BaseModel):
    """Schema for bulk updating category orders."""
    categories: List[CategoryOrderBase]