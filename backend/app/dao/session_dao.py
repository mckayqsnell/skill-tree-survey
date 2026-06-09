"""
Data Access Object for SurveySession model.
"""

from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import and_, func
from sqlalchemy.orm import Session, joinedload

from app.dao.base import BaseDAO
from app.models.session import SurveySession


class SessionDAO(BaseDAO[SurveySession]):
    """
    DAO for SurveySession model with specialized operations.
    """

    def __init__(self, db: Session):
        """
        Initialize SessionDAO.

        Args:
            db: Database session
        """
        super().__init__(db, SurveySession)

    def get_with_responses(self, session_id: int) -> SurveySession | None:
        """
        Get a session with all responses loaded.

        Args:
            session_id: Session ID

        Returns:
            Optional[SurveySession]: Session with responses or None
        """
        return (
            self.db.query(SurveySession)
            .options(joinedload(SurveySession.responses))
            .filter(SurveySession.id == session_id)
            .first()
        )

    def get_by_email(self, email: str) -> list[SurveySession]:
        """
        Get all sessions for a specific email.

        Args:
            email: User email

        Returns:
            List[SurveySession]: Sessions for the email
        """
        return (
            self.db.query(SurveySession)
            .filter(SurveySession.user_email == email)
            .order_by(SurveySession.started_at.desc())
            .all()
        )

    def get_by_company(self, company: str) -> list[SurveySession]:
        """
        Get all sessions for a specific company.

        Args:
            company: Company name

        Returns:
            List[SurveySession]: Sessions for the company
        """
        return (
            self.db.query(SurveySession)
            .filter(SurveySession.company == company)
            .order_by(SurveySession.started_at.desc())
            .all()
        )

    def get_completed_sessions(self) -> list[SurveySession]:
        """
        Get all completed sessions.

        Returns:
            List[SurveySession]: Completed sessions
        """
        return (
            self.db.query(SurveySession)
            .filter(SurveySession.completed_at.isnot(None))
            .order_by(SurveySession.completed_at.desc())
            .all()
        )

    def get_incomplete_sessions(
        self, older_than_hours: int = 24
    ) -> list[SurveySession]:
        """
        Get incomplete sessions older than specified hours.

        Args:
            older_than_hours: Hours threshold

        Returns:
            List[SurveySession]: Incomplete sessions
        """
        threshold = datetime.utcnow() - timedelta(hours=older_than_hours)
        return (
            self.db.query(SurveySession)
            .filter(
                and_(
                    SurveySession.completed_at.is_(None),
                    SurveySession.started_at < threshold,
                )
            )
            .all()
        )

    def mark_completed(self, session_id: int) -> SurveySession | None:
        """
        Mark a session as completed.

        Args:
            session_id: Session ID

        Returns:
            Optional[SurveySession]: Updated session or None
        """
        session = self.get(session_id)
        if not session:
            return None

        session.completed_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(session)
        return session

    def get_session_summary(self, session_id: int) -> dict[str, Any] | None:
        """
        Get a summary of a session with response statistics.

        Args:
            session_id: Session ID

        Returns:
            Optional[Dict]: Session summary or None
        """
        session = self.get_with_responses(session_id)
        if not session:
            return None

        # Count yes/no responses
        yes_count = sum(1 for r in session.responses if r.answer)
        no_count = sum(1 for r in session.responses if not r.answer)

        return {
            "id": session.id,
            "user_name": session.user_name,
            "user_email": session.user_email,
            "company": session.company,
            "started_at": session.started_at,
            "completed_at": session.completed_at,
            "is_completed": session.is_completed(),
            "completion_time_minutes": session.get_completion_time(),
            "total_responses": len(session.responses),
            "yes_responses": yes_count,
            "no_responses": no_count,
        }

    def get_analytics(self, company: str | None = None) -> dict[str, Any]:
        """
        Get analytics data for sessions.

        Args:
            company: Optional company filter

        Returns:
            Dict: Analytics data
        """
        query = self.db.query(SurveySession)

        if company:
            query = query.filter(SurveySession.company == company)

        total_sessions = query.count()
        completed_sessions = query.filter(
            SurveySession.completed_at.isnot(None)
        ).count()

        # Average completion time for completed sessions
        completed = query.filter(SurveySession.completed_at.isnot(None)).all()
        avg_time = None
        if completed:
            times = [s.get_completion_time() for s in completed]
            avg_time = sum(times) / len(times) if times else None

        # Get unique users
        unique_users = self.db.query(
            func.count(func.distinct(SurveySession.user_email))
        ).scalar()

        return {
            "total_sessions": total_sessions,
            "completed_sessions": completed_sessions,
            "completion_rate": (completed_sessions / total_sessions * 100)
            if total_sessions > 0
            else 0,
            "average_completion_time_minutes": avg_time,
            "unique_users": unique_users,
        }

    def get_user_skills_summary(self, email: str) -> dict[str, Any]:
        """
        Get a skills summary for a specific user.

        Args:
            email: User email

        Returns:
            Dict: Skills summary
        """
        sessions = self.get_by_email(email)

        if not sessions:
            return {"email": email, "sessions": [], "skills": []}

        # Get the most recent completed session
        latest_completed = next((s for s in sessions if s.is_completed()), None)

        skills = []
        if latest_completed:
            # Get all "yes" responses from the latest session
            yes_responses = [r for r in latest_completed.responses if r.answer]

            for response in yes_responses:
                skills.append(
                    {
                        "question_id": response.question_id,
                        "question_text": response.question.text,
                        "category": response.question.category,
                        "depth": response.question.get_depth(),
                    }
                )

        return {
            "email": email,
            "name": sessions[0].user_name if sessions else None,
            "company": sessions[0].company if sessions else None,
            "total_sessions": len(sessions),
            "completed_sessions": sum(1 for s in sessions if s.is_completed()),
            "latest_session": latest_completed.id if latest_completed else None,
            "skills": skills,
        }
