import sqlite3
from sqlite3 import connect
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from flask import request
from models.item import ItemModel


class Item(Resource):
    """
        Return possible item
    """

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='price input')

    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        """
            Create new item, get price from request.get_json()
        """
        if ItemModel.find_by_name(name):
            return {'message': "An item with this name already exists"}

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'])

        try:
            item.save_to_db()
        except:
            return {'message': "An error occured while try to insert new item"}

    def delete(self, name):
        """
            Looked all elelemns in list except for searching for
        """
        item = ItemModel.find_by_name(name)
        if item:
            ItemModel.delete_from_db()

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            try:
                item = ItemModel(name, data['price'])
            except:
                return {'message': "An error occured  while try to insert item"}, 500
        else:
            try:
                item.price = data['price']
            except:
                return {'message': "An error occured while try to update item"}, 500
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    """
        Return lsit with items
    """
    def get(self):
        items = {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
        return items
