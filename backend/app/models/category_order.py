"""
Category order model for storing the display order of categories.
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.database.connection import Base


class CategoryOrder(Base):
    """
    Model for storing the display order of categories.

    Attributes:
        id: Primary key
        category: Category name
        order_index: Display order (lower = appears first)
        updated_at: Last update timestamp
    """
    __tablename__ = "category_orders"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(50), unique=True, nullable=False, index=True)
    order_index = Column(Integer, nullable=False, default=0)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<CategoryOrder(category='{self.category}', order={self.order_index})>"