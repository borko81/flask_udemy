import sqlite3


class User:

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
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


if __name__ == '__main__':
    u = User.find_by_username("borko")
    print(u)
