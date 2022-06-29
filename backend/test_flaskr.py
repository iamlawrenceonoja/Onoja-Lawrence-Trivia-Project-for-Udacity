import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "postgres", "82522942Ag..", "localhost:5432", self.database_name
            )
        setup_db(self.app, self.database_path)

        self.new_question = {"question": "What is my name?", "answer": "Larry", "category": "4", "difficulty": "3"}
        self.search_term = {"searchTerm": "title"}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_retrieve_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])
        self.assertTrue(data["questions"])

    def test_retrieve_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
    
    def test_create_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["total_questions"])

    def test_search_for_question(self):
        res = self.client().post("/questions", json=self.search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["total_questions"])
    
    def test_delete_question(self):
        res = self.client().delete("/questions/31")
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 31).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 31)
        self.assertTrue(data["total_questions"])

    def test_retrieve_questions_with_cid(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["current_category"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["questions"])
    
    def test_get_random_quiz_question(self):
        quiz_parameters = {"quiz_category": {"type": "Science", "id": 1}, "previous_questions": []}

        res = self.client().post("/quizzes", json=quiz_parameters)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])
        self.assertTrue(data["categories"])

    def test_404_for_request_beyond_valid_page(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_404_for_failed_question_retrieval_by_category(self):
        res = self.client().get("/categories/10/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_422_for_failed_question_delete(self):
        res = self.client().delete("/questions/10000000000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable request")

    def test_405_for_unallowed_category_creation(self):
        res = self.client().post("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Method Not Allowed")

    def test_422_for_failed_question_creation(self):
        unprocessable_new_question = {"question": "What is my name?", "answer": "Larry", "category": "4"}
        res = self.client().post("/questions", json=unprocessable_new_question)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable request")


    def test_422_for_bad_quiz_request(self):
        quiz_parameters = {"quiz_category": {"type": "Science", "id": 1}, "previous_questions": None}

        res = self.client().post("/quizzes", json=quiz_parameters)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable request")

    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()