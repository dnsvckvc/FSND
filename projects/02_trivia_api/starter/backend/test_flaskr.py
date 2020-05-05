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
        self.client = self.app.test_client()
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432',
                                                       self.database_name)
        setup_db(self.app, self.database_path)

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
    Write at least one test for each test for successful operation and
    for expected errors.
    """

    def test_get_categories_successfully(self):
        res = self.client.get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_get_paginated_questions(self):
        res = self.client.get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_404_request_beyond_valid_page(self):
        res = self.client.get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_successfully(self):
        res = self.client.delete('/questions/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_unsuccessful(self):
        res = self.client.delete('/questions/3')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_new_question(self):
        before = json.loads(self.client.get('/questions').data)
        before_length = before['total_questions']

        test_new_json = {
                         'question': 'What does Corona stand for?',
                         'answer': 'Crown',
                         'category': 1,
                         'difficulty': 1
                         }

        res = self.client.post('/questions', json=test_new_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], before_length+1)
        self.assertTrue(data['new_question_id'])

        after = json.loads(self.client.get('/questions').data)
        after_length = after['total_questions']

        self.assertEqual(after_length-before_length, 1)

    def test_create_fail(self):
        res = self.client.post('/questions', json={'abc': 0})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_retrieve_questions_by_category(self):
        res = self.client.get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(len(data['questions']))

    def test_fail_questions_by_category(self):
        res = self.client.get('/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_successful_search(self):
        res = self.client.post('/questions', json={'searchTerm': "peanut"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['questions'][0]['answer'],
                         'George Washington Carver')

    def test_search_nothing_found(self):
        res = self.client.post('/questions', json={'searchTerm': "peanxt"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)

    def test_get_quiz_successful(self):
        quiz_json = {'previous_questions': [],
                     'quiz_category': {"id": 1, "category": "tbd"}}

        res = self.client.post('/quizzes', json=quiz_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertGreater(len(data['question']), 0)

    def test_get_quiz_with_history_successful(self):
        previously_played = [2, 4, 5, 6, 9,
                             10, 11, 12, 13, 14, 15, 16,
                             17, 18, 19, 20, 21, 22, 23]

        quiz_json = {'previous_questions': previously_played,
                     'quiz_category': {"id": 1, "category": "tbd"}}

        res = self.client.post('/quizzes', json=quiz_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertGreater(len(data['question']), 0)
        self.assertEqual(data['question']['answer'], 'Crown')

        question_temp = data['question']
        # print(question_temp['answer'], flush=True)
        # self.assertEqual(len(question_temp['answer']), 1)

    def test_get_quiz_without_data(self):
        res = self.client.post('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
