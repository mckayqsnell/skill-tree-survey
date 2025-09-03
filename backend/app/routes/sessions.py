"""
API routes for SurveySession operations.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, status, Query

from app.database.connection import get_db
from app.dao.factory import get_dao_factory, DAOFactory
from app.services.session_service import SessionService
from app.schemas.session import (
    SessionCreate, SessionResponse, SessionSummary,
    UserSkillsSummary
)

router = APIRouter(prefix="/sessions", tags=["Sessions"])


def get_session_service(dao_factory: DAOFactory = Depends(get_dao_factory)) -> SessionService:
    """
    Dependency injection for SessionService.
    
    Args:
        dao_factory: DAO factory from dependency
        
    Returns:
        SessionService: Service instance
    """
    return SessionService(dao_factory)


@router.post("/", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(
    session_data: SessionCreate,
    service: SessionService = Depends(get_session_service)
):
    """
    Start a new survey session.
    
    Args:
        session_data: Session creation data
        service: Session service
        
    Returns:
        Created session
    """
    return service.create_session(session_data)


@router.get("/{session_id}", response_model=SessionResponse)
def get_session(
    session_id: int,
    service: SessionService = Depends(get_session_service)
):
    """
    Get a specific session by ID.
    
    Args:
        session_id: Session ID
        service: Session service
        
    Returns:
        Session data
    """
    return service.get_session(session_id)


@router.get("/{session_id}/summary", response_model=SessionSummary)
def get_session_summary(
    session_id: int,
    service: SessionService = Depends(get_session_service)
):
    """
    Get a session summary with response statistics.
    
    Args:
        session_id: Session ID
        service: Session service
        
    Returns:
        Session summary
    """
    return service.get_session_summary(session_id)


@router.post("/{session_id}/complete", response_model=SessionResponse)
def complete_session(
    session_id: int,
    service: SessionService = Depends(get_session_service)
):
    """
    Mark a session as completed.
    
    Args:
        session_id: Session ID
        service: Session service
        
    Returns:
        Updated session
    """
    return service.complete_session(session_id)


@router.get("/by-email/{email}", response_model=List[SessionResponse])
def get_sessions_by_email(
    email: str,
    service: SessionService = Depends(get_session_service)
):
    """
    Get all sessions for a specific email.
    
    Args:
        email: User email
        service: Session service
        
    Returns:
        List of sessions
    """
    return service.get_sessions_by_email(email)


@router.get("/by-company/{company}", response_model=List[SessionResponse])
def get_sessions_by_company(
    company: str,
    service: SessionService = Depends(get_session_service)
):
    """
    Get all sessions for a specific company.
    
    Args:
        company: Company name
        service: Session service
        
    Returns:
        List of sessions
    """
    return service.get_sessions_by_company(company)


@router.get("/user-skills/{email}", response_model=UserSkillsSummary)
def get_user_skills_summary(
    email: str,
    service: SessionService = Depends(get_session_service)
):
    """
    Get skills summary for a specific user.
    
    Args:
        email: User email
        service: Session service
        
    Returns:
        Skills summary
    """
    return service.get_user_skills_summary(email)