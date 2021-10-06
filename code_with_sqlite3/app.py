from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from users import UserRegister


app = Flask(__name__)
app.secret_key = 'botk@'
api = Api(app)
jwt = JWT(app, authenticate, identity)  # /auth
from items import Item, ItemList


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    app.run(debug=True)