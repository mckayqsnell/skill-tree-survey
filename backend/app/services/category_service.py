"""
Service layer for category order management.
"""

from app.core.config import settings
from app.dao.factory import DAOFactory
from app.schemas.category import (
    CategoryOrderBulkUpdate,
    CategoryOrderCreate,
    CategoryOrderResponse,
)

logger = settings.logger


class CategoryService:
    """
    Service for managing category display orders.

    Attributes:
        dao_factory: DAO factory instance
    """

    def __init__(self, dao_factory: DAOFactory):
        """
        Initialize CategoryService.

        Args:
            dao_factory: DAO factory for database access
        """
        self.dao_factory = dao_factory
        self.category_dao = dao_factory.get_category_dao()

    def get_category_order(self) -> list[CategoryOrderResponse]:
        """
        Get all categories in their display order.

        Returns:
            List of categories sorted by order_index
        """
        try:
            logger.info("Fetching category display order")
            categories = self.category_dao.get_all_ordered()

            if not categories:
                logger.info("No category orders found, initializing defaults")
                # Initialize with default order from seeder categories
                default_categories = [
                    "Backend",
                    "Frontend",
                    "DevOps",
                    "Cloud",
                    "Data",
                    "Machine Learning",
                    "Mobile",
                    "Security",
                    "Architecture",
                    "Testing",
                    "Leadership",
                    "Data Science",
                    "AI/ML Engineering",
                    "UI/UX Design",
                ]
                categories = self.category_dao.initialize_defaults(default_categories)

            return [CategoryOrderResponse.model_validate(cat) for cat in categories]

        except Exception as e:
            logger.error(f"Error fetching category order: {str(e)}")
            raise

    def update_category_order(
        self, bulk_update: CategoryOrderBulkUpdate
    ) -> list[CategoryOrderResponse]:
        """
        Bulk update category display orders.

        Args:
            bulk_update: Bulk update data containing categories with new order indices

        Returns:
            Updated list of category orders
        """
        try:
            logger.info(f"Updating order for {len(bulk_update.categories)} categories")

            # Validate that order indices are unique
            order_indices = [cat.order_index for cat in bulk_update.categories]
            if len(order_indices) != len(set(order_indices)):
                logger.error("Duplicate order indices provided")
                raise ValueError("Each category must have a unique order index")

            # Convert to CategoryOrderCreate objects
            category_creates = [
                CategoryOrderCreate(category=cat.category, order_index=cat.order_index)
                for cat in bulk_update.categories
            ]

            # Perform bulk update
            updated = self.category_dao.bulk_update(category_creates)

            if not updated:
                logger.error("Failed to update category orders")
                raise Exception("Failed to update category orders")

            logger.info(f"Successfully updated {len(updated)} category orders")
            return [CategoryOrderResponse.model_validate(cat) for cat in updated]

        except ValueError as ve:
            logger.error(f"Validation error updating category order: {str(ve)}")
            raise
        except Exception as e:
            logger.error(f"Error updating category order: {str(e)}")
            raise

    def reset_to_defaults(self) -> list[CategoryOrderResponse]:
        """
        Reset category orders to default configuration.

        Returns:
            List of categories in default order
        """
        try:
            logger.info("Resetting category orders to defaults")

            default_categories = [
                "Backend",
                "Frontend",
                "DevOps",
                "Cloud",
                "Data",
                "Machine Learning",
                "Mobile",
                "Security",
                "Architecture",
                "Testing",
                "Leadership",
                "Data Science",
                "AI/ML Engineering",
                "UI/UX Design",
            ]

            # Create bulk update with default order
            category_creates = [
                CategoryOrderCreate(category=cat, order_index=idx)
                for idx, cat in enumerate(default_categories)
            ]

            updated = self.category_dao.bulk_update(category_creates)

            logger.info(f"Reset {len(updated)} categories to default order")
            return [CategoryOrderResponse.model_validate(cat) for cat in updated]

        except Exception as e:
            logger.error(f"Error resetting category order to defaults: {str(e)}")
            raise

    def add_new_category(self, category_name: str) -> CategoryOrderResponse:
        """
        Add a new category with the highest order index.

        Args:
            category_name: Name of the new category

        Returns:
            Created category order
        """
        try:
            logger.info(f"Adding new category: {category_name}")

            # Check if category already exists
            existing = self.category_dao.get_by_category(category_name)
            if existing:
                logger.warning(f"Category '{category_name}' already exists")
                return CategoryOrderResponse.model_validate(existing)

            # Get current max order index
            all_categories = self.category_dao.get_all_ordered()
            max_index = max([cat.order_index for cat in all_categories], default=-1)

            # Create new category with next index
            new_category = CategoryOrderCreate(
                category=category_name, order_index=max_index + 1
            )

            created = self.category_dao.create(new_category)
            if not created:
                raise Exception(
                    f"Failed to create category order for '{category_name}'"
                )

            logger.info(
                f"Successfully added category '{category_name}' with order index {created.order_index}"
            )
            return CategoryOrderResponse.model_validate(created)

        except Exception as e:
            logger.error(f"Error adding new category '{category_name}': {str(e)}")
            raise
