"""
Business logic service for SurveySession operations.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from fastapi import HTTPException, status

from app.dao.factory import DAOFactory
from app.schemas.session import (
    SessionCreate, SessionResponse, SessionSummary,
    SessionAnalytics, UserSkillsSummary
)


class SessionService:
    """
    Service layer for SurveySession operations.
    
    Handles business logic for survey sessions.
    """
    
    def __init__(self, dao_factory: DAOFactory):
        """
        Initialize SessionService.
        
        Args:
            dao_factory: DAO factory instance
        """
        self.dao_factory = dao_factory
        self.session_dao = dao_factory.get_session_dao()
    
    def create_session(self, session_data: SessionCreate) -> SessionResponse:
        """
        Create a new survey session.
        
        Args:
            session_data: Session creation data
            
        Returns:
            SessionResponse: Created session
        """
        session = self.session_dao.create(**session_data.model_dump())
        return SessionResponse.model_validate(session)
    
    def get_session(self, session_id: int) -> SessionResponse:
        """
        Get a session by ID.
        
        Args:
            session_id: Session ID
            
        Returns:
            SessionResponse: Session data
            
        Raises:
            HTTPException: If not found
        """
        session = self.session_dao.get(session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session with ID {session_id} not found"
            )
        return SessionResponse.model_validate(session)
    
    def get_session_summary(self, session_id: int) -> SessionSummary:
        """
        Get a session summary with statistics.
        
        Args:
            session_id: Session ID
            
        Returns:
            SessionSummary: Session summary
            
        Raises:
            HTTPException: If not found
        """
        summary = self.session_dao.get_session_summary(session_id)
        if not summary:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session with ID {session_id} not found"
            )
        return SessionSummary(**summary)
    
    def complete_session(self, session_id: int) -> SessionResponse:
        """
        Mark a session as completed.
        
        Args:
            session_id: Session ID
            
        Returns:
            SessionResponse: Updated session
            
        Raises:
            HTTPException: If not found or already completed
        """
        session = self.session_dao.get(session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session with ID {session_id} not found"
            )
        
        if session.is_completed():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session is already completed"
            )
        
        updated_session = self.session_dao.mark_completed(session_id)
        return SessionResponse.model_validate(updated_session)
    
    def get_all_sessions(
        self,
        skip: int = 0,
        limit: int = 100,
        completed_only: bool = False
    ) -> List[SessionResponse]:
        """
        Get all sessions with pagination.

        Args:
            skip: Number to skip
            limit: Maximum number to return
            completed_only: Only return completed sessions

        Returns:
            List[SessionResponse]: Sessions
        """
        if completed_only:
            sessions = self.session_dao.get_completed_sessions()
        else:
            sessions = self.session_dao.get_all(skip, limit)

        return [SessionResponse.model_validate(s) for s in sessions]

    def get_all_sessions_with_summaries(
        self,
        skip: int = 0,
        limit: int = 100,
        completed_only: bool = False
    ) -> List[SessionSummary]:
        """
        Get all sessions with summaries including completion time.

        Args:
            skip: Number to skip
            limit: Maximum number to return
            completed_only: Only return completed sessions

        Returns:
            List[SessionSummary]: Sessions with summaries
        """
        if completed_only:
            sessions = self.session_dao.get_completed_sessions()
        else:
            sessions = self.session_dao.get_all(skip, limit)

        summaries = []
        for session in sessions:
            summary_data = self.session_dao.get_session_summary(session.id)
            if summary_data:
                summaries.append(SessionSummary(**summary_data))

        return summaries
    
    def get_sessions_by_email(self, email: str) -> List[SessionResponse]:
        """
        Get all sessions for a user email.
        
        Args:
            email: User email
            
        Returns:
            List[SessionResponse]: Sessions
        """
        sessions = self.session_dao.get_by_email(email)
        return [SessionResponse.model_validate(s) for s in sessions]
    
    def get_sessions_by_company(self, company: str) -> List[SessionResponse]:
        """
        Get all sessions for a company.
        
        Args:
            company: Company name
            
        Returns:
            List[SessionResponse]: Sessions
        """
        sessions = self.session_dao.get_by_company(company)
        return [SessionResponse.model_validate(s) for s in sessions]
    
    def get_analytics(self, company: Optional[str] = None) -> SessionAnalytics:
        """
        Get analytics data for sessions.
        
        Args:
            company: Optional company filter
            
        Returns:
            SessionAnalytics: Analytics data
        """
        analytics = self.session_dao.get_analytics(company)
        return SessionAnalytics(**analytics)
    
    def get_user_skills_summary(self, email: str) -> UserSkillsSummary:
        """
        Get skills summary for a user.
        
        Args:
            email: User email
            
        Returns:
            UserSkillsSummary: Skills summary
        """
        summary = self.session_dao.get_user_skills_summary(email)
        return UserSkillsSummary(**summary)
    
    def delete_session(self, session_id: int) -> bool:
        """
        Delete a session and all its responses.
        
        Args:
            session_id: Session ID
            
        Returns:
            bool: True if deleted
            
        Raises:
            HTTPException: If not found
        """
        if not self.session_dao.exists(session_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session with ID {session_id} not found"
            )
        
        return self.session_dao.delete(session_id)
    
    def cleanup_incomplete_sessions(self, hours_threshold: int = 24) -> int:
        """
        Clean up incomplete sessions older than threshold.
        
        Args:
            hours_threshold: Age threshold in hours
            
        Returns:
            int: Number of sessions deleted
        """
        incomplete = self.session_dao.get_incomplete_sessions(hours_threshold)
        count = 0
        
        for session in incomplete:
            if self.session_dao.delete(session.id):
                count += 1
        
        return count