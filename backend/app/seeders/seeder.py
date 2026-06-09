"""
Database seeder for initial questions.
"""

import json
import os
from typing import Any

from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.connection import get_db, init_db
from app.models.category_order import CategoryOrder
from app.models.question import Question

logger = settings.logger


class Seeder:
    """
    Seeder class to populate database with initial data.
    """

    def __init__(self, db: Session):
        """
        Initialize seeder with database session.

        Args:
            db: Database session
        """
        self.db = db

    def is_database_empty(self) -> bool:
        """
        Check if the database has any questions.

        Returns:
            bool: True if database is empty
        """
        count = self.db.query(Question).count()
        return count == 0

    def load_seed_data(self) -> dict[str, Any]:
        """
        Load seed data from JSON file.

        Returns:
            Dict: Seed data
        """
        file_path = os.path.join(os.path.dirname(__file__), "initial_questions.json")

        with open(file_path) as f:
            return json.load(f)

    def create_question_tree(
        self,
        question_data: dict[str, Any],
        parent: Question = None,
        order: int = 0,
        parent_category: str = None,
    ) -> Question:
        """
        Recursively create question tree.

        Args:
            question_data: Question data from JSON
            parent: Parent question (None for base questions)
            order: Order index
            parent_category: Category to inherit from parent

        Returns:
            Question: Created question
        """
        # Determine category - use provided category or inherit from parent
        category = question_data.get("category")
        if not category and parent_category:
            category = parent_category

        # Create the question
        question = Question(
            text=question_data["text"],
            parent_id=parent.id if parent else None,
            is_base=question_data.get("is_base", False),
            category=category,
            order_index=order,
        )

        self.db.add(question)
        self.db.flush()  # Get the ID without committing

        # Create children recursively
        children = question_data.get("children", [])
        for idx, child_data in enumerate(children):
            self.create_question_tree(child_data, question, idx, category)

        return question

    def seed_database(self) -> int:
        """
        Seed the database with initial questions and category orders.

        Returns:
            int: Number of base questions created
        """
        if not self.is_database_empty():
            logger.info("Database already contains questions, skipping seeding")
            return 0

        logger.info("Seeding database with initial questions and category orders")

        try:
            seed_data = self.load_seed_data()
            questions = seed_data.get("questions", [])
            categories = seed_data.get("categories", [])

            # Seed category orders
            logger.info("Seeding category orders", count=len(categories))
            for idx, category in enumerate(categories):
                # Check if category order already exists
                existing = (
                    self.db.query(CategoryOrder).filter_by(category=category).first()
                )
                if not existing:
                    category_order = CategoryOrder(category=category, order_index=idx)
                    self.db.add(category_order)

            # Create all base questions and their trees
            base_count = 0
            for idx, question_data in enumerate(questions):
                self.create_question_tree(question_data, None, idx, None)
                base_count += 1

            self.db.commit()
            logger.info(
                "Database seeded successfully",
                base_questions=base_count,
                category_orders=len(categories),
            )
            return base_count

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error seeding database: {str(e)}", exc_info=True)
            raise

    def clear_all_questions(self) -> int:
        """
        Clear all questions from the database.
        WARNING: This will delete all questions and responses!

        Returns:
            int: Number of questions deleted
        """
        count = self.db.query(Question).count()
        self.db.query(Question).delete()
        self.db.commit()
        return count


def run_seeder() -> None:
    """
    Run the seeder to populate initial data.
    """
    # Initialize database tables
    init_db()

    # Get database session
    db = next(get_db())

    try:
        seeder = Seeder(db)
        seeder.seed_database()
    finally:
        db.close()


if __name__ == "__main__":
    run_seeder()
