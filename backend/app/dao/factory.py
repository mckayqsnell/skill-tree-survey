"""
DAO Factory for creating Data Access Objects.
"""

from fastapi import Depends
from sqlalchemy.orm import Session

from app.dao.category_dao import CategoryDAO
from app.dao.question_dao import QuestionDAO
from app.dao.response_dao import ResponseDAO
from app.dao.session_dao import SessionDAO
from app.database.connection import get_db


class DAOFactory:
    """
    Factory class for creating DAO instances.

    This pattern allows for easy switching between different database
    implementations if needed in the future.
    """

    def __init__(self, db: Session):
        """
        Initialize the DAO factory with a database session.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db
        self._daos = {}

    def get_question_dao(self) -> QuestionDAO:
        """
        Get or create QuestionDAO instance.

        Returns:
            QuestionDAO: DAO for Question model
        """
        if "question" not in self._daos:
            self._daos["question"] = QuestionDAO(self.db)
        return self._daos["question"]

    def get_session_dao(self) -> SessionDAO:
        """
        Get or create SessionDAO instance.

        Returns:
            SessionDAO: DAO for SurveySession model
        """
        if "session" not in self._daos:
            self._daos["session"] = SessionDAO(self.db)
        return self._daos["session"]

    def get_response_dao(self) -> ResponseDAO:
        """
        Get or create ResponseDAO instance.

        Returns:
            ResponseDAO: DAO for Response model
        """
        if "response" not in self._daos:
            self._daos["response"] = ResponseDAO(self.db)
        return self._daos["response"]

    def get_category_dao(self) -> CategoryDAO:
        """
        Get or create CategoryDAO instance.

        Returns:
            CategoryDAO: DAO for CategoryOrder model
        """
        if "category" not in self._daos:
            self._daos["category"] = CategoryDAO(self.db)
        return self._daos["category"]

    def commit(self) -> None:
        """
        Commit the current transaction.
        """
        self.db.commit()

    def rollback(self) -> None:
        """
        Rollback the current transaction.
        """
        self.db.rollback()

    def close(self) -> None:
        """
        Close the database session.
        """
        self.db.close()


def get_dao_factory(db: Session = Depends(get_db)) -> DAOFactory:
    """
    Dependency injection function for FastAPI.

    Args:
        db: Database session from dependency

    Returns:
        DAOFactory: Factory instance for the session
    """
    return DAOFactory(db)
