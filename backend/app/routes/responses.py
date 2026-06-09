"""
API routes for Response operations.
"""

from fastapi import APIRouter, Depends, status

from app.dao.factory import DAOFactory, get_dao_factory
from app.schemas.response import (
    BulkResponseCreate,
    ResponseCreate,
    ResponseInDB,
    ResponseWithQuestion,
)
from app.schemas.session import CategoryStatistics, SkillDepthAnalysis
from app.services.response_service import ResponseService

router = APIRouter(prefix="/responses", tags=["Responses"])


def get_response_service(
    dao_factory: DAOFactory = Depends(get_dao_factory),
) -> ResponseService:
    """
    Dependency injection for ResponseService.

    Args:
        dao_factory: DAO factory from dependency

    Returns:
        ResponseService: Service instance
    """
    return ResponseService(dao_factory)


@router.post(
    "/session/{session_id}",
    response_model=ResponseInDB,
    status_code=status.HTTP_201_CREATED,
)
def create_response(
    session_id: int,
    response_data: ResponseCreate,
    service: ResponseService = Depends(get_response_service),
):
    """
    Submit a response for a question in a session.

    Args:
        session_id: Session ID
        response_data: Response data
        service: Response service

    Returns:
        Created response
    """
    return service.create_response(session_id, response_data)


@router.post(
    "/bulk", response_model=list[ResponseInDB], status_code=status.HTTP_201_CREATED
)
def create_bulk_responses(
    bulk_data: BulkResponseCreate,
    service: ResponseService = Depends(get_response_service),
):
    """
    Submit multiple responses at once.

    Args:
        bulk_data: Bulk response data
        service: Response service

    Returns:
        List of created responses
    """
    return service.create_bulk_responses(bulk_data)


@router.get("/session/{session_id}", response_model=list[ResponseInDB])
def get_session_responses(
    session_id: int, service: ResponseService = Depends(get_response_service)
):
    """
    Get all responses for a session.

    Args:
        session_id: Session ID
        service: Response service

    Returns:
        List of responses
    """
    return service.get_session_responses(session_id)


@router.get("/session/{session_id}/detailed", response_model=list[ResponseWithQuestion])
def get_session_responses_detailed(
    session_id: int, service: ResponseService = Depends(get_response_service)
):
    """
    Get session responses with question details.

    Args:
        session_id: Session ID
        service: Response service

    Returns:
        List of responses with question information
    """
    return service.get_session_responses_with_questions(session_id)


@router.get(
    "/session/{session_id}/category-stats", response_model=list[CategoryStatistics]
)
def get_category_statistics(
    session_id: int, service: ResponseService = Depends(get_response_service)
):
    """
    Get response statistics grouped by category.

    Args:
        session_id: Session ID
        service: Response service

    Returns:
        Statistics by category
    """
    return service.get_category_statistics(session_id)


@router.get("/session/{session_id}/depth-analysis", response_model=SkillDepthAnalysis)
def get_skill_depth_analysis(
    session_id: int, service: ResponseService = Depends(get_response_service)
):
    """
    Analyze skill depths for a session.

    Args:
        session_id: Session ID
        service: Response service

    Returns:
        Skill depth analysis
    """
    return service.get_skill_depth_analysis(session_id)


@router.delete("/{response_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_response(
    response_id: int, service: ResponseService = Depends(get_response_service)
):
    """
    Delete a specific response.

    Args:
        response_id: Response ID
        service: Response service
    """
    service.delete_response(response_id)
    return None
