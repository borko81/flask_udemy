from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity


app = Flask(__name__)
app.secret_key = 'botk@'
api = Api(app)
jwt = JWT(app, authenticate, identity)  # /auth

items = []


class _Helper:
    @staticmethod
    def check_name_in_list(name):
        return next(filter(lambda x: x['name'] == name, items), None)

    @staticmethod
    def all_item_except_searching_for(name):
        return list(filter(lambda n: n['name'] != name, items))


class Item(Resource, _Helper):
    """
        Return possible item
    """
    @jwt_required()
    def get(self, name):
        item = _Helper.check_name_in_list(name)
        return item, 200 if item else 404

    def post(self, name):
        """
            Create new item, get price from request.get_json()
        """
        if _Helper.check_name_in_list(name) is not None:
            return {"error": "This name is already exists"}, 400

        data = request.get_json()
        item = {"name": name, "price": data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        """
            Looked all elelemns in list except for searching for
        """
        global items
        items = _Helper.all_item_except_searching_for(name)
        return {"message": f"Item {name} deleted successfully"}, 204

    def put(self, name):
        data = request.get_json()
        item = _Helper.check_name_in_list(name)
        if item is None:
            item = {"name": name, "price": data['price']}
            items.append(item)
        item.update(name)
        return {"message": "Operation was successfull"}, 200


class ItemList(Resource):
    """
        Return lsit with items
    """
    def get(self):
        return {'items': items}, 200


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')


if __name__ == '__main__':
    app.run(debug=True)
