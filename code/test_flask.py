import unittest
import requests
from models.user import UserModel
from db import db
from app import app


class TestAPI(unittest.TestCase):
    URL = "http://127.0.0.1:5000/items"

    def test_1_get_all_items(self):
        resp = requests.get(self.URL)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 1)
        print("Test one completed")


if __name__ == '__main__':
    tester1 = TestAPI()
    tester1.test_1_get_all_items()
