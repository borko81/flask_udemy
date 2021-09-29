from flask import Flask, request
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

items = []


class _Helper:
    @staticmethod
    def check_name_in_list(name):
        return next(filter(lambda x: x['name'] == name, items), None)


class Item(Resource, _Helper):
    """
        Return possible item
    """
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
