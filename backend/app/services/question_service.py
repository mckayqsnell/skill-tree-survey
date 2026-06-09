"""
Business logic service for Question operations.
"""

from fastapi import HTTPException, status

from app.dao.factory import DAOFactory
from app.schemas.question import (
    QuestionCreate,
    QuestionMove,
    QuestionReorder,
    QuestionResponse,
    QuestionStatistics,
    QuestionTree,
    QuestionUpdate,
    QuestionWithChildren,
)


class QuestionService:
    """
    Service layer for Question operations.

    Handles business logic and validation for questions.
    """

    def __init__(self, dao_factory: DAOFactory):
        """
        Initialize QuestionService.

        Args:
            dao_factory: DAO factory instance
        """
        self.dao_factory = dao_factory
        self.question_dao = dao_factory.get_question_dao()
        self.response_dao = dao_factory.get_response_dao()

    def create_question(self, question_data: QuestionCreate) -> QuestionResponse:
        """
        Create a new question.

        Args:
            question_data: Question creation data

        Returns:
            QuestionResponse: Created question

        Raises:
            HTTPException: If parent doesn't exist
        """
        # Validate parent exists if specified
        if question_data.parent_id:
            parent = self.question_dao.get(question_data.parent_id)
            if not parent:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Parent question with ID {question_data.parent_id} not found",
                )
            # Child questions should not be base questions
            question_data.is_base = False
        else:
            # Root level questions should be base questions
            question_data.is_base = True

        question = self.question_dao.create(**question_data.model_dump())
        return QuestionResponse.model_validate(question)

    def get_question(self, question_id: int) -> QuestionResponse:
        """
        Get a question by ID.

        Args:
            question_id: Question ID

        Returns:
            QuestionResponse: Question data

        Raises:
            HTTPException: If not found
        """
        question = self.question_dao.get(question_id)
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Question with ID {question_id} not found",
            )
        return QuestionResponse.model_validate(question)

    def get_question_with_children(self, question_id: int) -> QuestionWithChildren:
        """
        Get a question with all its children.

        Args:
            question_id: Question ID

        Returns:
            QuestionWithChildren: Question with nested children

        Raises:
            HTTPException: If not found
        """
        question = self.question_dao.get_with_children(question_id)
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Question with ID {question_id} not found",
            )
        return QuestionWithChildren.model_validate(question)

    def update_question(
        self, question_id: int, update_data: QuestionUpdate
    ) -> QuestionResponse:
        """
        Update a question.

        Args:
            question_id: Question ID
            update_data: Update data

        Returns:
            QuestionResponse: Updated question

        Raises:
            HTTPException: If not found or invalid update
        """
        # Check if question exists
        existing = self.question_dao.get(question_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Question with ID {question_id} not found",
            )

        # Validate parent if changing to a new, non-null parent
        if update_data.parent_id and update_data.parent_id != existing.parent_id:
            parent = self.question_dao.get(update_data.parent_id)
            if not parent:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Parent question with ID {update_data.parent_id} not found",
                )
            # Check for circular reference
            if self.question_dao._would_create_cycle(
                question_id, update_data.parent_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot create circular reference in question tree",
                )

        update_dict = update_data.model_dump(exclude_unset=True)
        question = self.question_dao.update(question_id, **update_dict)
        return QuestionResponse.model_validate(question)

    def delete_question(self, question_id: int) -> bool:
        """
        Delete a question and all its descendants.

        Args:
            question_id: Question ID

        Returns:
            bool: True if deleted

        Raises:
            HTTPException: If not found
        """
        if not self.question_dao.exists(question_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Question with ID {question_id} not found",
            )

        return self.question_dao.delete_with_children(question_id)

    def get_base_questions(self, category: str | None = None) -> list[QuestionResponse]:
        """
        Get all base questions.

        Args:
            category: Optional category filter

        Returns:
            List[QuestionResponse]: Base questions
        """
        questions = self.question_dao.get_base_questions(category)
        return [QuestionResponse.model_validate(q) for q in questions]

    def get_child_questions(self, parent_id: int) -> list[QuestionResponse]:
        """
        Get child questions for a parent.

        Args:
            parent_id: Parent question ID

        Returns:
            List[QuestionResponse]: Child questions

        Raises:
            HTTPException: If parent not found
        """
        if not self.question_dao.exists(parent_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Parent question with ID {parent_id} not found",
            )

        questions = self.question_dao.get_children(parent_id)
        return [QuestionResponse.model_validate(q) for q in questions]

    def get_tree_structure(self) -> list[QuestionTree]:
        """
        Get the entire question tree structure.

        Returns:
            List[QuestionTree]: Tree structure
        """
        tree_data = self.question_dao.get_tree_structure()
        return [QuestionTree(**node) for node in tree_data]

    def reorder_questions(self, reorder_data: QuestionReorder) -> bool:
        """
        Reorder questions within the same parent level.

        Args:
            reorder_data: Reorder data

        Returns:
            bool: True if successful

        Raises:
            HTTPException: If invalid reorder
        """
        # Validate all questions exist and have the same parent
        for question_id in reorder_data.question_ids:
            question = self.question_dao.get(question_id)
            if not question:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Question with ID {question_id} not found",
                )
            if question.parent_id != reorder_data.parent_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Question {question_id} does not belong to parent {reorder_data.parent_id}",
                )

        return self.question_dao.reorder_questions(
            reorder_data.parent_id, reorder_data.question_ids
        )

    def move_question(self, move_data: QuestionMove) -> QuestionResponse:
        """
        Move a question to a new parent.

        Args:
            move_data: Move data

        Returns:
            QuestionResponse: Updated question

        Raises:
            HTTPException: If invalid move
        """
        question = self.question_dao.move_question(
            move_data.question_id, move_data.new_parent_id
        )

        if not question:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid move operation"
            )

        return QuestionResponse.model_validate(question)

    def get_question_statistics(self, question_id: int) -> QuestionStatistics:
        """
        Get response statistics for a question.

        Args:
            question_id: Question ID

        Returns:
            QuestionStatistics: Statistics data

        Raises:
            HTTPException: If question not found
        """
        if not self.question_dao.exists(question_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Question with ID {question_id} not found",
            )

        stats = self.response_dao.get_question_statistics(question_id)
        return QuestionStatistics(**stats)

    def get_categories(self) -> list[str]:
        """
        Get all unique question categories.

        Returns:
            List[str]: Category names
        """
        return self.question_dao.get_categories()
