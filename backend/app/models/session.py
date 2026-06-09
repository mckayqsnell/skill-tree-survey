"""
Survey session model for tracking user assessments.
"""

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.connection import Base


class SurveySession(Base):
    """
    Survey session to track individual assessments.

    Attributes:
        id: Primary key
        user_name: Name of the person taking the survey
        user_email: Email of the person taking the survey
        company: Company/organization name
        started_at: When the survey was started
        completed_at: When the survey was completed (nullable)
    """

    __tablename__ = "survey_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(100), nullable=False)
    user_email = Column(String(100), nullable=False, index=True)
    company = Column(String(100), nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationship to responses
    responses = relationship(
        "Response", back_populates="session", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """String representation of SurveySession."""
        return f"<SurveySession(id={self.id}, user={self.user_name}, email={self.user_email})>"

    def is_completed(self) -> bool:
        """
        Check if the survey session is completed.

        Returns:
            bool: True if completed, False otherwise
        """
        return self.completed_at is not None

    def get_completion_time(self) -> float | None:
        """
        Get the time taken to complete the survey in minutes.

        Returns:
            Optional[float]: Time in minutes if completed, None otherwise
        """
        if not self.is_completed():
            return None

        time_diff = self.completed_at - self.started_at
        return time_diff.total_seconds() / 60.0

    def get_response_count(self) -> int:
        """
        Get the number of responses in this session.

        Returns:
            int: Number of responses
        """
        return len(self.responses)
