"""
Category-related API routes (public).
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.config import settings
from app.dao.factory import DAOFactory, get_dao_factory
from app.schemas.category import CategoryOrderResponse
from app.services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])
logger = settings.logger


def get_category_service(
    dao_factory: DAOFactory = Depends(get_dao_factory),
) -> CategoryService:
    """Get CategoryService instance."""
    return CategoryService(dao_factory)


@router.get("/order", response_model=list[CategoryOrderResponse])
def get_category_order(service: CategoryService = Depends(get_category_service)):
    """
    Get current category display order (public endpoint).

    This endpoint is used by the frontend to maintain consistent
    category ordering across all views.

    Args:
        service: Category service

    Returns:
        List of categories in their display order
    """
    try:
        logger.info("Fetching category order for public display")
        return service.get_category_order()
    except Exception as e:
        logger.error(f"Error fetching category order: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve category order",
        ) from e
