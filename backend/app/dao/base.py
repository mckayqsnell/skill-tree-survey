"""
Base DAO abstract class for common database operations.
"""

from abc import ABC
from typing import Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database.connection import Base


class BaseDAO[ModelType: Base](ABC):
    """
    Abstract base class for Data Access Objects.

    Provides common CRUD operations for database models.
    """

    def __init__(self, db: Session, model: type[ModelType]):
        """
        Initialize the DAO with a database session and model class.

        Args:
            db: SQLAlchemy database session
            model: SQLAlchemy model class
        """
        self.db = db
        self.model = model

    def get(self, id: int) -> ModelType | None:
        """
        Get a single record by ID.

        Args:
            id: Record ID

        Returns:
            Optional[ModelType]: Model instance or None if not found
        """
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ModelType]:
        """
        Get all records with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List[ModelType]: List of model instances
        """
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, **kwargs) -> ModelType:
        """
        Create a new record.

        Args:
            **kwargs: Model field values

        Returns:
            ModelType: Created model instance

        Raises:
            SQLAlchemyError: If creation fails
        """
        try:
            db_obj = self.model(**kwargs)
            self.db.add(db_obj)
            self.db.commit()
            self.db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def update(self, id: int, **kwargs) -> ModelType | None:
        """
        Update an existing record.

        Args:
            id: Record ID
            **kwargs: Fields to update

        Returns:
            Optional[ModelType]: Updated model instance or None if not found

        Raises:
            SQLAlchemyError: If update fails
        """
        try:
            db_obj = self.get(id)
            if not db_obj:
                return None

            for key, value in kwargs.items():
                if hasattr(db_obj, key):
                    setattr(db_obj, key, value)

            self.db.commit()
            self.db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def delete(self, id: int) -> bool:
        """
        Delete a record by ID.

        Args:
            id: Record ID

        Returns:
            bool: True if deleted, False if not found

        Raises:
            SQLAlchemyError: If deletion fails
        """
        try:
            db_obj = self.get(id)
            if not db_obj:
                return False

            self.db.delete(db_obj)
            self.db.commit()
            return True
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def count(self) -> int:
        """
        Count total number of records.

        Returns:
            int: Total count
        """
        return self.db.query(self.model).count()

    def exists(self, id: int) -> bool:
        """
        Check if a record exists.

        Args:
            id: Record ID

        Returns:
            bool: True if exists, False otherwise
        """
        return self.db.query(self.model).filter(self.model.id == id).count() > 0

    def filter_by(self, **kwargs) -> list[ModelType]:
        """
        Filter records by field values.

        Args:
            **kwargs: Field value filters

        Returns:
            List[ModelType]: Filtered model instances
        """
        query = self.db.query(self.model)
        for key, value in kwargs.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        return query.all()

    def bulk_create(self, objects: list[dict[str, Any]]) -> list[ModelType]:
        """
        Create multiple records at once.

        Args:
            objects: List of dictionaries with field values

        Returns:
            List[ModelType]: Created model instances

        Raises:
            SQLAlchemyError: If creation fails
        """
        try:
            db_objects = [self.model(**obj) for obj in objects]
            self.db.add_all(db_objects)
            self.db.commit()
            return db_objects
        except SQLAlchemyError:
            self.db.rollback()
            raise
