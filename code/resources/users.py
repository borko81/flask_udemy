import sqlite3
from flask_restful import Resource, reqparse

from ..models.user import UserModel


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
        if UserModel.find_by_username(data['username']):
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
    u = UserModel.find_by_username("borko")
    print(u)
