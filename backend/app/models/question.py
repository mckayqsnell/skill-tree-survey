"""
Question model for skill tree structure.
"""

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.connection import Base


class Question(Base):
    """
    Question model with self-referencing for tree structure.

    Attributes:
        id: Primary key
        parent_id: Foreign key to parent question (nullable for base questions)
        text: Question text
        is_base: Whether this is a base-level question
        category: Question category (e.g., DevOps, Backend, Frontend)
        order_index: Order within same parent level
        created_at: Timestamp when created
        updated_at: Timestamp when last updated
    """

    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("questions.id"), nullable=True, index=True)
    text = Column(Text, nullable=False)
    is_base = Column(Boolean, default=False, nullable=False)
    category = Column(String(50), nullable=True, index=True)
    order_index = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Self-referencing relationship
    parent = relationship("Question", remote_side=[id], backref="children")

    # Relationship to responses
    responses = relationship(
        "Response", back_populates="question", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """String representation of Question."""
        return f"<Question(id={self.id}, text='{self.text[:50]}...', is_base={self.is_base})>"

    def get_all_descendants(self) -> list["Question"]:
        """
        Get all descendant questions recursively.

        Returns:
            List[Question]: All descendant questions
        """
        descendants = []
        for child in self.children:
            descendants.append(child)
            descendants.extend(child.get_all_descendants())
        return descendants

    def get_depth(self) -> int:
        """
        Get the depth of this question in the tree.

        Returns:
            int: Depth level (0 for base questions)
        """
        if self.parent_id is None:
            return 0
        return 1 + self.parent.get_depth()
