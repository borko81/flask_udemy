from flask import Flask, render_template
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.users import UserRegister


app = Flask(__name__)
app.secret_key = 'botk@'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
jwt = JWT(app, authenticate, identity)  # /auth
from resources.items import Item, ItemList


# Fetch testing
@app.route('/fetch')
def fetch_get_all_items():
    return render_template('get_all_items.html')


# Fetch post new items
@app.route('/fetch_new', methods=["POST", "GET"])
def fetch_post_new_item():
    return render_template('post_new.html')


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)
