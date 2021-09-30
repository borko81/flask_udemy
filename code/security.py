from users import User
from werkzeug.security import safe_str_cmp

users = [
    User(1, 'borko', 'borko'),
    User(2, 'test', 'test')
]

username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}


def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)


if __name__ == '__main__':
    a = authenticate("borko", "borko")
    print(identity)
