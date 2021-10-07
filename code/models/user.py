import sqlite3
from db import db


class UserModel(db.Model):
    """
        Create user, use classmethod, to initialize user class from given username
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        """
            This method search user in database
        """
        try:
            connection = sqlite3.connect("data.db")
        except sqlite3.Error as er:
            raise ValueError(er)
        else:
            cursor = connection.cursor()

            query = "SELECT * FROM users WHERE username=?"
            result = cursor.execute(query, (username, ))
            row = result.fetchone()
            if row:
                user = cls(*row)
                return user
            user = None
            return user
        finally:
            connection.close()

    @classmethod
    def find_by_id(cls, _id):
        """
            This method search user in db from given as id
        """
        try:
            connection = sqlite3.connect("data.db")
        except sqlite3.Error as er:
            raise ValueError(er)
        else:
            cursor = connection.cursor()

            query = "SELECT * FROM users WHERE id=?"
            result = cursor.execute(query, (_id, ))
            row = result.fetchone()
            if row:
                user = cls(*row)
                return user
            else:
                user = None
                return user
        finally:
            connection.close()
