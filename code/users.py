import sqlite3
from flask_restful import Resource, reqparse


class User:
    """
        Create user, use classmethod, to initialize user class from given username
    """
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
            else:
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


class UserRegister(Resource):

    """
        Register class, usinf reqparse from flask_restful
        :validation from unique username in form and db too
    """

    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, help="Insert username")
    parser.add_argument("password", type=str, required=True, help="Insert password")

    def post(self):
        data = UserRegister.parser.parse_args()

        # this validata username unique
        if User.find_by_username(data['username']):
            return {"message": "This username not allowed!"}, 400

        try:
            connection = sqlite3.connect("data.db")
            cursor = connection.cursor()
        except sqlite3.Error as er:
            raise ValueError(er)
        else:
            query = "INSERT INTO users VALUES (NULL, ?, ?)"
            try:
                cursor.execute(query, (data['username'], data['password']))
            except sqlite3.Error as er:
                raise ValueError(er)
            else:
                connection.commit()
        finally:
            connection.close()

        return {"message": "User created successfully"}, 201


if __name__ == '__main__':
    u = User.find_by_username("borko")
    print(u)
