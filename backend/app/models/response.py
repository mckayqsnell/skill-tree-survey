"""
Response model for tracking answers to questions.
"""
from sqlalchemy import Column, Integer, Boolean, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.connection import Base


class Response(Base):
    """
    Response model to track individual answers.
    
    Attributes:
        id: Primary key
        session_id: Foreign key to survey session
        question_id: Foreign key to question
        answer: Boolean answer (True for yes, False for no)
        answered_at: Timestamp when answered
    """
    __tablename__ = "responses"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("survey_sessions.id"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False, index=True)
    answer = Column(Boolean, nullable=False)
    answered_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    session = relationship("SurveySession", back_populates="responses")
    question = relationship("Question", back_populates="responses")
    
    # Unique constraint to prevent duplicate answers
    __table_args__ = (
        UniqueConstraint('session_id', 'question_id', name='_session_question_uc'),
    )
    
    def __repr__(self) -> str:
        """String representation of Response."""
        return f"<Response(session_id={self.session_id}, question_id={self.question_id}, answer={self.answer})>"