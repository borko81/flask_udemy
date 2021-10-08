import os
import unittest
from app import app
from db import db
from models.user import UserModel
import requests


class TestCase(unittest.TestCase):
    URL = 'http://127.0.0.1:5000/auth'
    
    data = {
        'username': 'borko',
        'password': 'borko'
    }

    uncorect_data = {
        'username': 'borko123',
        'password': 'borko123'
    }

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_make_login(self):
        u = UserModel(_id=10, username='bork', password='borko')
        db.session.add(u)
        db.session.commit()
        response = requests.post(self.URL, json=self.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue((response.json()['access_token']))
        print(response.text)
        print("Test one complete")

    def test_user_try_login_with_uncorect_data_return_message(self):
        response = requests.post(self.URL, json=self.uncorect_data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()['description'], 'Invalid credentials')
        print("Test two complete")


if __name__ == '__main__':
    db.init_app(app)
    t = TestCase()
    t.test_user_make_login()
    t.test_user_try_login_with_uncorect_data_return_message()