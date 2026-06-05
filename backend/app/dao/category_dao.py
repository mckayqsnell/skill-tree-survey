"""
Data Access Object for category order operations.
"""

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.category_order import CategoryOrder
from app.schemas.category import CategoryOrderCreate, CategoryOrderUpdate

logger = settings.logger


class CategoryDAO:
    """
    DAO for category order operations.

    Attributes:
        db: Database session
    """

    def __init__(self, db: Session):
        """
        Initialize CategoryDAO.

        Args:
            db: Database session
        """
        self.db = db

    def get_all_ordered(self) -> list[CategoryOrder]:
        """
        Get all categories in order, excluding Pokemon.

        Returns:
            List of category orders sorted by order_index, excluding Pokemon
        """
        try:
            # Exclude Pokemon from category management
            stmt = (
                select(CategoryOrder)
                .where(CategoryOrder.category != "Pokemon")
                .order_by(CategoryOrder.order_index)
            )
            result = list(self.db.execute(stmt).scalars())
            logger.debug(f"Retrieved {len(result)} category orders (excluding Pokemon)")
            return result
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving category orders: {str(e)}")
            return []

    def get_by_category(self, category: str) -> CategoryOrder | None:
        """
        Get category order by category name.

        Args:
            category: Category name

        Returns:
            CategoryOrder object or None
        """
        try:
            stmt = select(CategoryOrder).where(CategoryOrder.category == category)
            result = self.db.execute(stmt).scalar_one_or_none()
            if result:
                logger.debug(f"Found category order for '{category}'")
            else:
                logger.debug(f"No category order found for '{category}'")
            return result
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving category order for '{category}': {str(e)}")
            return None

    def create(self, category_data: CategoryOrderCreate) -> CategoryOrder | None:
        """
        Create a new category order entry.

        Args:
            category_data: Category order creation data

        Returns:
            Created category order or None on error
        """
        try:
            category_order = CategoryOrder(**category_data.model_dump())
            self.db.add(category_order)
            self.db.commit()
            self.db.refresh(category_order)
            logger.info(
                f"Created category order for '{category_data.category}' with index {category_data.order_index}"
            )
            return category_order
        except IntegrityError as e:
            self.db.rollback()
            logger.error(
                f"Integrity error creating category order for '{category_data.category}': {str(e)}"
            )
            return None
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(
                f"Error creating category order for '{category_data.category}': {str(e)}"
            )
            return None

    def update(
        self, category: str, update_data: CategoryOrderUpdate
    ) -> CategoryOrder | None:
        """
        Update category order.

        Args:
            category: Category name
            update_data: Update data

        Returns:
            Updated category order or None if not found or on error
        """
        try:
            category_order = self.get_by_category(category)
            if not category_order:
                logger.warning(
                    f"Cannot update non-existent category order for '{category}'"
                )
                return None

            old_index = category_order.order_index
            category_order.order_index = update_data.order_index
            self.db.commit()
            self.db.refresh(category_order)
            logger.info(
                f"Updated category order for '{category}': {old_index} -> {update_data.order_index}"
            )
            return category_order
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error updating category order for '{category}': {str(e)}")
            return None

    def bulk_update(self, categories: list[CategoryOrderCreate]) -> list[CategoryOrder]:
        """
        Bulk update category orders.

        Args:
            categories: List of categories with their order indices

        Returns:
            List of updated category orders
        """
        result = []
        try:
            # Filter out Pokemon from updates
            filtered_categories = [
                cat for cat in categories if cat.category != "Pokemon"
            ]
            logger.info(
                f"Bulk updating {len(filtered_categories)} category orders (excluding Pokemon)"
            )

            for cat_data in filtered_categories:
                existing = self.get_by_category(cat_data.category)
                if existing:
                    existing.order_index = cat_data.order_index
                    result.append(existing)
                    logger.debug(
                        f"Updated existing category '{cat_data.category}' to index {cat_data.order_index}"
                    )
                else:
                    new_order = CategoryOrder(
                        category=cat_data.category, order_index=cat_data.order_index
                    )
                    self.db.add(new_order)
                    result.append(new_order)
                    logger.debug(
                        f"Created new category order '{cat_data.category}' with index {cat_data.order_index}"
                    )

            self.db.commit()
            for item in result:
                self.db.refresh(item)

            logger.info(f"Successfully bulk updated {len(result)} category orders")
            return result

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error during bulk update of category orders: {str(e)}")
            return []

    def delete(self, category: str) -> bool:
        """
        Delete category order entry.

        Args:
            category: Category name

        Returns:
            True if deleted, False if not found or on error
        """
        try:
            category_order = self.get_by_category(category)
            if not category_order:
                logger.warning(
                    f"Cannot delete non-existent category order for '{category}'"
                )
                return False

            self.db.delete(category_order)
            self.db.commit()
            logger.info(f"Deleted category order for '{category}'")
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error deleting category order for '{category}': {str(e)}")
            return False

    def initialize_defaults(self, categories: list[str]) -> list[CategoryOrder]:
        """
        Initialize default category orders if they don't exist.

        Args:
            categories: List of category names in default order

        Returns:
            List of category orders
        """
        result = []
        try:
            logger.info(
                f"Initializing default category orders for {len(categories)} categories"
            )

            for index, category in enumerate(categories):
                existing = self.get_by_category(category)
                if not existing:
                    new_order = CategoryOrder(category=category, order_index=index)
                    self.db.add(new_order)
                    result.append(new_order)
                    logger.debug(
                        f"Created default order for '{category}' at index {index}"
                    )
                else:
                    result.append(existing)
                    logger.debug(
                        f"Category '{category}' already has order index {existing.order_index}"
                    )

            self.db.commit()
            logger.info(f"Successfully initialized {len(result)} category orders")
            return result

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error initializing default category orders: {str(e)}")
            return []
