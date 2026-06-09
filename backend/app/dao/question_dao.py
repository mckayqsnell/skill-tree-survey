"""
Data Access Object for Question model.
"""

from typing import Any

from sqlalchemy.orm import Session, joinedload

from app.dao.base import BaseDAO
from app.models.question import Question


class QuestionDAO(BaseDAO[Question]):
    """
    DAO for Question model with specialized tree operations.
    """

    def __init__(self, db: Session):
        """
        Initialize QuestionDAO.

        Args:
            db: Database session
        """
        super().__init__(db, Question)

    def get_base_questions(self, category: str | None = None) -> list[Question]:
        """
        Get all base-level questions.

        Args:
            category: Optional category filter

        Returns:
            List[Question]: Base questions ordered by order_index
        """
        query = self.db.query(Question).filter(Question.is_base.is_(True))

        if category:
            query = query.filter(Question.category == category)

        return query.order_by(Question.order_index).all()

    def get_children(self, parent_id: int) -> list[Question]:
        """
        Get child questions for a parent.

        Args:
            parent_id: Parent question ID

        Returns:
            List[Question]: Child questions ordered by order_index
        """
        return (
            self.db.query(Question)
            .filter(Question.parent_id == parent_id)
            .order_by(Question.order_index)
            .all()
        )

    def get_with_children(self, id: int) -> Question | None:
        """
        Get a question with its children loaded.

        Args:
            id: Question ID

        Returns:
            Optional[Question]: Question with children or None
        """
        return (
            self.db.query(Question)
            .options(joinedload(Question.children))
            .filter(Question.id == id)
            .first()
        )

    def get_tree_structure(self) -> list[dict[str, Any]]:
        """
        Get the entire question tree structure.

        Returns:
            List[Dict]: Tree structure with nested children
        """
        base_questions = self.get_base_questions()
        return [self._build_tree_node(q) for q in base_questions]

    def _build_tree_node(self, question: Question) -> dict[str, Any]:
        """
        Recursively build a tree node for a question.

        Args:
            question: Question model instance

        Returns:
            Dict: Tree node with nested children
        """
        node = {
            "id": question.id,
            "text": question.text,
            "is_base": question.is_base,
            "category": question.category,
            "order_index": question.order_index,
            "children": [],
        }

        # Recursively add children
        for child in sorted(question.children, key=lambda x: x.order_index):
            node["children"].append(self._build_tree_node(child))

        return node

    def reorder_questions(self, parent_id: int | None, new_order: list[int]) -> bool:
        """
        Reorder questions within the same parent level.

        Args:
            parent_id: Parent ID (None for base questions)
            new_order: List of question IDs in new order

        Returns:
            bool: True if successful
        """
        try:
            for index, question_id in enumerate(new_order):
                question = self.get(question_id)
                if question and question.parent_id == parent_id:
                    question.order_index = index

            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            raise

    def delete_with_children(self, id: int) -> bool:
        """
        Delete a question and all its descendants.

        Args:
            id: Question ID

        Returns:
            bool: True if deleted
        """
        question = self.get_with_children(id)
        if not question:
            return False

        # Recursively delete children first
        for child in question.children:
            self.delete_with_children(child.id)

        # Then delete the question itself
        return self.delete(id)

    def get_categories(self) -> list[str]:
        """
        Get all unique categories.

        Returns:
            List[str]: List of category names
        """
        results = (
            self.db.query(Question.category)
            .filter(Question.category.isnot(None))
            .distinct()
            .all()
        )
        return [r[0] for r in results]

    def move_question(
        self, question_id: int, new_parent_id: int | None
    ) -> Question | None:
        """
        Move a question to a new parent.

        Args:
            question_id: Question to move
            new_parent_id: New parent ID (None for making it a base question)

        Returns:
            Optional[Question]: Updated question or None
        """
        question = self.get(question_id)
        if not question:
            return None

        # Check for circular reference
        if new_parent_id:
            parent = self.get(new_parent_id)
            if not parent or self._would_create_cycle(question_id, new_parent_id):
                return None

        question.parent_id = new_parent_id
        question.is_base = new_parent_id is None

        self.db.commit()
        self.db.refresh(question)
        return question

    def _would_create_cycle(self, question_id: int, new_parent_id: int) -> bool:
        """
        Check if moving would create a circular reference.

        Args:
            question_id: Question being moved
            new_parent_id: Proposed new parent

        Returns:
            bool: True if would create cycle
        """
        current = self.get(new_parent_id)
        while current:
            if current.id == question_id:
                return True
            current = self.get(current.parent_id) if current.parent_id else None
        return False
