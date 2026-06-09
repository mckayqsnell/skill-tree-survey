"""
Business logic service for Response operations.
"""

from fastapi import HTTPException, status

from app.dao.factory import DAOFactory
from app.schemas.response import (
    BulkResponseCreate,
    ResponseCreate,
    ResponseInDB,
    ResponseWithQuestion,
)
from app.schemas.session import CategoryStatistics, SkillDepthAnalysis


class ResponseService:
    """
    Service layer for Response operations.

    Handles business logic for survey responses.
    """

    def __init__(self, dao_factory: DAOFactory):
        """
        Initialize ResponseService.

        Args:
            dao_factory: DAO factory instance
        """
        self.dao_factory = dao_factory
        self.response_dao = dao_factory.get_response_dao()
        self.session_dao = dao_factory.get_session_dao()
        self.question_dao = dao_factory.get_question_dao()

    def create_response(
        self, session_id: int, response_data: ResponseCreate
    ) -> ResponseInDB:
        """
        Create or update a response for a session.

        Args:
            session_id: Session ID
            response_data: Response data

        Returns:
            ResponseInDB: Created or updated response

        Raises:
            HTTPException: If session or question not found
        """
        # Validate session exists and is not completed
        session = self.session_dao.get(session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session with ID {session_id} not found",
            )

        if session.is_completed():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot add responses to completed session",
            )

        # Validate question exists
        if not self.question_dao.exists(response_data.question_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Question with ID {response_data.question_id} not found",
            )

        response = self.response_dao.create_response(
            session_id, response_data.question_id, response_data.answer
        )

        return ResponseInDB.model_validate(response)

    def create_bulk_responses(
        self, bulk_data: BulkResponseCreate
    ) -> list[ResponseInDB]:
        """
        Create multiple responses at once.

        Args:
            bulk_data: Bulk response data

        Returns:
            List[ResponseInDB]: Created responses

        Raises:
            HTTPException: If session or questions not found
        """
        # Validate session
        session = self.session_dao.get(bulk_data.session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session with ID {bulk_data.session_id} not found",
            )

        if session.is_completed():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot add responses to completed session",
            )

        # Validate all questions exist
        question_ids = [r.question_id for r in bulk_data.responses]
        for qid in question_ids:
            if not self.question_dao.exists(qid):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Question with ID {qid} not found",
                )

        # Create responses
        responses = []
        for response_data in bulk_data.responses:
            response = self.response_dao.create_response(
                bulk_data.session_id, response_data.question_id, response_data.answer
            )
            responses.append(ResponseInDB.model_validate(response))

        return responses

    def get_session_responses(self, session_id: int) -> list[ResponseInDB]:
        """
        Get all responses for a session.

        Args:
            session_id: Session ID

        Returns:
            List[ResponseInDB]: Session responses

        Raises:
            HTTPException: If session not found
        """
        if not self.session_dao.exists(session_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session with ID {session_id} not found",
            )

        responses = self.response_dao.get_by_session(session_id)
        return [ResponseInDB.model_validate(r) for r in responses]

    def get_session_responses_with_questions(
        self, session_id: int
    ) -> list[ResponseWithQuestion]:
        """
        Get session responses with question details.

        Args:
            session_id: Session ID

        Returns:
            List[ResponseWithQuestion]: Responses with questions

        Raises:
            HTTPException: If session not found
        """
        if not self.session_dao.exists(session_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session with ID {session_id} not found",
            )

        responses = self.response_dao.get_session_responses_with_questions(session_id)

        result = []
        for response in responses:
            result.append(
                ResponseWithQuestion(
                    id=response.id,
                    session_id=response.session_id,
                    question_id=response.question_id,
                    answer=response.answer,
                    answered_at=response.answered_at,
                    question_text=response.question.text,
                    question_category=response.question.category or "Uncategorized",
                    question_depth=response.question.get_depth(),
                )
            )

        return result

    def get_category_statistics(self, session_id: int) -> list[CategoryStatistics]:
        """
        Get response statistics by category for a session.

        Args:
            session_id: Session ID

        Returns:
            List[CategoryStatistics]: Statistics by category

        Raises:
            HTTPException: If session not found
        """
        if not self.session_dao.exists(session_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session with ID {session_id} not found",
            )

        stats = self.response_dao.get_category_statistics(session_id)

        return [
            CategoryStatistics(
                category=category,
                yes_count=data["yes"],
                no_count=data["no"],
                total=data["total"],
            )
            for category, data in stats.items()
        ]

    def get_skill_depth_analysis(self, session_id: int) -> SkillDepthAnalysis:
        """
        Analyze skill depths for a session.

        Args:
            session_id: Session ID

        Returns:
            SkillDepthAnalysis: Depth analysis

        Raises:
            HTTPException: If session not found
        """
        if not self.session_dao.exists(session_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session with ID {session_id} not found",
            )

        analysis = self.response_dao.get_skill_depth_analysis(session_id)
        return SkillDepthAnalysis(**analysis)

    def delete_response(self, response_id: int) -> bool:
        """
        Delete a response.

        Args:
            response_id: Response ID

        Returns:
            bool: True if deleted

        Raises:
            HTTPException: If not found or session is completed
        """
        response = self.response_dao.get(response_id)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Response with ID {response_id} not found",
            )

        session = self.session_dao.get(response.session_id)
        if session.is_completed():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete responses from completed session",
            )

        return self.response_dao.delete(response_id)
