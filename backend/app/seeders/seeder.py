"""
Database seeder for initial questions.
"""
import json
import os
from typing import Dict, Any, List
from sqlalchemy.orm import Session

from app.models.question import Question
from app.database.connection import get_db, init_db


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
    
    def load_seed_data(self) -> Dict[str, Any]:
        """
        Load seed data from JSON file.
        
        Returns:
            Dict: Seed data
        """
        file_path = os.path.join(
            os.path.dirname(__file__),
            "initial_questions.json"
        )
        
        with open(file_path, "r") as f:
            return json.load(f)
    
    def create_question_tree(
        self,
        question_data: Dict[str, Any],
        parent: Question = None,
        order: int = 0
    ) -> Question:
        """
        Recursively create question tree.
        
        Args:
            question_data: Question data from JSON
            parent: Parent question (None for base questions)
            order: Order index
            
        Returns:
            Question: Created question
        """
        # Create the question
        question = Question(
            text=question_data["text"],
            parent_id=parent.id if parent else None,
            is_base=question_data.get("is_base", False),
            category=question_data.get("category"),
            order_index=order
        )
        
        self.db.add(question)
        self.db.flush()  # Get the ID without committing
        
        # Create children recursively
        children = question_data.get("children", [])
        for idx, child_data in enumerate(children):
            self.create_question_tree(child_data, question, idx)
        
        return question
    
    def seed_database(self) -> int:
        """
        Seed the database with initial questions.
        
        Returns:
            int: Number of base questions created
        """
        if not self.is_database_empty():
            print("Database already contains questions. Skipping seeding.")
            return 0
        
        print("Seeding database with initial questions...")
        
        try:
            seed_data = self.load_seed_data()
            questions = seed_data.get("questions", [])
            
            # Create all base questions and their trees
            base_count = 0
            for idx, question_data in enumerate(questions):
                self.create_question_tree(question_data, None, idx)
                base_count += 1
            
            self.db.commit()
            print(f"Successfully seeded {base_count} base questions with their children")
            return base_count
            
        except Exception as e:
            self.db.rollback()
            print(f"Error seeding database: {str(e)}")
            raise e
    
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