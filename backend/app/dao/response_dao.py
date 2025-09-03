"""
Data Access Object for Response model.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_

from app.dao.base import BaseDAO
from app.models.response import Response
from app.models.question import Question


class ResponseDAO(BaseDAO[Response]):
    """
    DAO for Response model with specialized operations.
    """
    
    def __init__(self, db: Session):
        """
        Initialize ResponseDAO.
        
        Args:
            db: Database session
        """
        super().__init__(db, Response)
    
    def get_by_session(self, session_id: int) -> List[Response]:
        """
        Get all responses for a session.
        
        Args:
            session_id: Session ID
            
        Returns:
            List[Response]: Responses for the session
        """
        return (
            self.db.query(Response)
            .filter(Response.session_id == session_id)
            .order_by(Response.answered_at)
            .all()
        )
    
    def get_by_question(self, question_id: int) -> List[Response]:
        """
        Get all responses for a specific question.
        
        Args:
            question_id: Question ID
            
        Returns:
            List[Response]: Responses for the question
        """
        return (
            self.db.query(Response)
            .filter(Response.question_id == question_id)
            .all()
        )
    
    def get_response(self, session_id: int, question_id: int) -> Optional[Response]:
        """
        Get a specific response for a session and question.
        
        Args:
            session_id: Session ID
            question_id: Question ID
            
        Returns:
            Optional[Response]: Response or None
        """
        return (
            self.db.query(Response)
            .filter(
                and_(
                    Response.session_id == session_id,
                    Response.question_id == question_id
                )
            )
            .first()
        )
    
    def create_response(self, session_id: int, question_id: int, answer: bool) -> Response:
        """
        Create or update a response.
        
        Args:
            session_id: Session ID
            question_id: Question ID
            answer: Boolean answer
            
        Returns:
            Response: Created or updated response
        """
        # Check if response already exists
        existing = self.get_response(session_id, question_id)
        
        if existing:
            # Update existing response
            existing.answer = answer
            self.db.commit()
            self.db.refresh(existing)
            return existing
        else:
            # Create new response
            return self.create(
                session_id=session_id,
                question_id=question_id,
                answer=answer
            )
    
    def get_session_responses_with_questions(self, session_id: int) -> List[Response]:
        """
        Get all responses for a session with questions loaded.
        
        Args:
            session_id: Session ID
            
        Returns:
            List[Response]: Responses with questions
        """
        return (
            self.db.query(Response)
            .options(joinedload(Response.question))
            .filter(Response.session_id == session_id)
            .order_by(Response.answered_at)
            .all()
        )
    
    def get_question_statistics(self, question_id: int) -> Dict[str, Any]:
        """
        Get statistics for responses to a question.
        
        Args:
            question_id: Question ID
            
        Returns:
            Dict: Statistics including yes/no counts and percentage
        """
        responses = self.get_by_question(question_id)
        
        total = len(responses)
        yes_count = sum(1 for r in responses if r.answer)
        no_count = total - yes_count
        
        return {
            "question_id": question_id,
            "total_responses": total,
            "yes_count": yes_count,
            "no_count": no_count,
            "yes_percentage": (yes_count / total * 100) if total > 0 else 0,
            "no_percentage": (no_count / total * 100) if total > 0 else 0
        }
    
    def get_category_statistics(self, session_id: int) -> Dict[str, Dict[str, int]]:
        """
        Get response statistics grouped by category for a session.
        
        Args:
            session_id: Session ID
            
        Returns:
            Dict: Statistics by category
        """
        responses = self.get_session_responses_with_questions(session_id)
        
        stats = {}
        for response in responses:
            category = response.question.category or "Uncategorized"
            if category not in stats:
                stats[category] = {"yes": 0, "no": 0, "total": 0}
            
            stats[category]["total"] += 1
            if response.answer:
                stats[category]["yes"] += 1
            else:
                stats[category]["no"] += 1
        
        return stats
    
    def get_skill_depth_analysis(self, session_id: int) -> Dict[str, Any]:
        """
        Analyze the depth of skills for a session.
        
        Args:
            session_id: Session ID
            
        Returns:
            Dict: Analysis of skill depths
        """
        responses = self.get_session_responses_with_questions(session_id)
        
        depth_analysis = {}
        max_depths_by_category = {}
        
        for response in responses:
            if response.answer:  # Only count "yes" responses as skills
                depth = response.question.get_depth()
                category = response.question.category or "Uncategorized"
                
                # Track overall depth distribution
                depth_key = f"level_{depth}"
                depth_analysis[depth_key] = depth_analysis.get(depth_key, 0) + 1
                
                # Track maximum depth by category
                if category not in max_depths_by_category:
                    max_depths_by_category[category] = depth
                else:
                    max_depths_by_category[category] = max(max_depths_by_category[category], depth)
        
        return {
            "depth_distribution": depth_analysis,
            "max_depths_by_category": max_depths_by_category,
            "average_depth": (
                sum(int(k.split("_")[1]) * v for k, v in depth_analysis.items()) /
                sum(depth_analysis.values())
            ) if depth_analysis else 0
        }