"""
Admin API routes with password protection.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header

from app.config.settings import get_settings
from app.database.connection import get_db
from app.dao.factory import get_dao_factory, DAOFactory
from app.services.question_service import QuestionService
from app.services.session_service import SessionService
from app.services.response_service import ResponseService
from app.schemas.question import (
    QuestionCreate, QuestionUpdate, QuestionResponse,
    QuestionReorder, QuestionMove, QuestionStatistics
)
from app.schemas.session import SessionResponse, SessionAnalytics
from app.schemas.response import ResponseInDB

router = APIRouter(prefix="/admin", tags=["Admin"])
settings = get_settings()


def verify_admin_password(x_admin_password: str = Header(...)):
    """
    Verify admin password from header.
    
    Args:
        x_admin_password: Admin password from header
        
    Raises:
        HTTPException: If password is incorrect
    """
    if x_admin_password != settings.ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin password"
        )
    return True


def get_question_service(dao_factory: DAOFactory = Depends(get_dao_factory)) -> QuestionService:
    """Get QuestionService instance."""
    return QuestionService(dao_factory)


def get_session_service(dao_factory: DAOFactory = Depends(get_dao_factory)) -> SessionService:
    """Get SessionService instance."""
    return SessionService(dao_factory)


def get_response_service(dao_factory: DAOFactory = Depends(get_dao_factory)) -> ResponseService:
    """Get ResponseService instance."""
    return ResponseService(dao_factory)


# Question Management Routes

@router.post("/questions", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
def create_question(
    question_data: QuestionCreate,
    service: QuestionService = Depends(get_question_service),
    _: bool = Depends(verify_admin_password)
):
    """
    Create a new question.
    
    Args:
        question_data: Question creation data
        service: Question service
        
    Returns:
        Created question
    """
    return service.create_question(question_data)


@router.put("/questions/{question_id}", response_model=QuestionResponse)
def update_question(
    question_id: int,
    update_data: QuestionUpdate,
    service: QuestionService = Depends(get_question_service),
    _: bool = Depends(verify_admin_password)
):
    """
    Update an existing question.
    
    Args:
        question_id: Question ID
        update_data: Update data
        service: Question service
        
    Returns:
        Updated question
    """
    return service.update_question(question_id, update_data)


@router.delete("/questions/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(
    question_id: int,
    service: QuestionService = Depends(get_question_service),
    _: bool = Depends(verify_admin_password)
):
    """
    Delete a question and all its children.
    
    Args:
        question_id: Question ID
        service: Question service
    """
    service.delete_question(question_id)
    return None


@router.put("/questions/reorder", response_model=dict)
def reorder_questions(
    reorder_data: QuestionReorder,
    service: QuestionService = Depends(get_question_service),
    _: bool = Depends(verify_admin_password)
):
    """
    Reorder questions within the same parent level.
    
    Args:
        reorder_data: Reorder data
        service: Question service
        
    Returns:
        Success status
    """
    success = service.reorder_questions(reorder_data)
    return {"success": success}


@router.put("/questions/move", response_model=QuestionResponse)
def move_question(
    move_data: QuestionMove,
    service: QuestionService = Depends(get_question_service),
    _: bool = Depends(verify_admin_password)
):
    """
    Move a question to a new parent.
    
    Args:
        move_data: Move data
        service: Question service
        
    Returns:
        Updated question
    """
    return service.move_question(move_data)


@router.get("/questions/{question_id}/statistics", response_model=QuestionStatistics)
def get_question_statistics(
    question_id: int,
    service: QuestionService = Depends(get_question_service),
    _: bool = Depends(verify_admin_password)
):
    """
    Get response statistics for a question.
    
    Args:
        question_id: Question ID
        service: Question service
        
    Returns:
        Question statistics
    """
    return service.get_question_statistics(question_id)


# Session Management Routes

@router.get("/sessions", response_model=List[SessionResponse])
def get_all_sessions(
    skip: int = 0,
    limit: int = 100,
    completed_only: bool = False,
    service: SessionService = Depends(get_session_service),
    _: bool = Depends(verify_admin_password)
):
    """
    Get all sessions with pagination.
    
    Args:
        skip: Number to skip
        limit: Maximum number to return
        completed_only: Only return completed sessions
        service: Session service
        
    Returns:
        List of sessions
    """
    return service.get_all_sessions(skip, limit, completed_only)


@router.get("/analytics", response_model=SessionAnalytics)
def get_analytics(
    company: Optional[str] = None,
    service: SessionService = Depends(get_session_service),
    _: bool = Depends(verify_admin_password)
):
    """
    Get analytics data for sessions.
    
    Args:
        company: Optional company filter
        service: Session service
        
    Returns:
        Analytics data
    """
    return service.get_analytics(company)


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(
    session_id: int,
    service: SessionService = Depends(get_session_service),
    _: bool = Depends(verify_admin_password)
):
    """
    Delete a session and all its responses.
    
    Args:
        session_id: Session ID
        service: Session service
    """
    service.delete_session(session_id)
    return None


@router.post("/sessions/cleanup", response_model=dict)
def cleanup_incomplete_sessions(
    hours_threshold: int = 24,
    service: SessionService = Depends(get_session_service),
    _: bool = Depends(verify_admin_password)
):
    """
    Clean up incomplete sessions older than threshold.
    
    Args:
        hours_threshold: Age threshold in hours
        service: Session service
        
    Returns:
        Number of sessions deleted
    """
    count = service.cleanup_incomplete_sessions(hours_threshold)
    return {"deleted_sessions": count}