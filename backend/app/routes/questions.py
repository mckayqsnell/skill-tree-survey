"""
API routes for Question operations.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, status

from app.database.connection import get_db
from app.dao.factory import get_dao_factory, DAOFactory
from app.services.question_service import QuestionService
from app.schemas.question import (
    QuestionCreate, QuestionUpdate, QuestionResponse,
    QuestionWithChildren, QuestionTree
)

router = APIRouter(prefix="/questions", tags=["Questions"])


def get_question_service(dao_factory: DAOFactory = Depends(get_dao_factory)) -> QuestionService:
    """
    Dependency injection for QuestionService.
    
    Args:
        dao_factory: DAO factory from dependency
        
    Returns:
        QuestionService: Service instance
    """
    return QuestionService(dao_factory)


@router.get("/base", response_model=List[QuestionResponse])
def get_base_questions(
    category: Optional[str] = None,
    service: QuestionService = Depends(get_question_service)
):
    """
    Get all base-level questions.
    
    Args:
        category: Optional category filter
        service: Question service
        
    Returns:
        List of base questions
    """
    return service.get_base_questions(category)


@router.get("/tree", response_model=List[QuestionTree])
def get_question_tree(
    service: QuestionService = Depends(get_question_service)
):
    """
    Get the entire question tree structure.
    
    Args:
        service: Question service
        
    Returns:
        Tree structure with all questions
    """
    return service.get_tree_structure()


@router.get("/categories", response_model=List[str])
def get_categories(
    service: QuestionService = Depends(get_question_service)
):
    """
    Get all unique question categories.
    
    Args:
        service: Question service
        
    Returns:
        List of category names
    """
    return service.get_categories()


@router.get("/{question_id}", response_model=QuestionResponse)
def get_question(
    question_id: int,
    service: QuestionService = Depends(get_question_service)
):
    """
    Get a specific question by ID.
    
    Args:
        question_id: Question ID
        service: Question service
        
    Returns:
        Question data
    """
    return service.get_question(question_id)


@router.get("/{question_id}/with-children", response_model=QuestionWithChildren)
def get_question_with_children(
    question_id: int,
    service: QuestionService = Depends(get_question_service)
):
    """
    Get a question with all its children.
    
    Args:
        question_id: Question ID
        service: Question service
        
    Returns:
        Question with nested children
    """
    return service.get_question_with_children(question_id)


@router.get("/{question_id}/children", response_model=List[QuestionResponse])
def get_child_questions(
    question_id: int,
    service: QuestionService = Depends(get_question_service)
):
    """
    Get child questions for a specific parent.
    
    Args:
        question_id: Parent question ID
        service: Question service
        
    Returns:
        List of child questions
    """
    return service.get_child_questions(question_id)