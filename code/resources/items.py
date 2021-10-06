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
            item.insert()
        except:
            return {'message': "An error occured while try to insert new item"}

    def delete(self, name):
        """
            Looked all elelemns in list except for searching for
        """
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE NAME=?"
        try:
            cursor.execute(query, (name,))
            connection.commit()
        except sqlite3.Error:
            raise ValueError('Error when try to delete item')
        finally:
            connection.close()
        return {'message': f'Item with name {name} was deleted'}, 204

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if item is None:
            try:
                updated_item.insert()
                ItemModel.insert(updated_item)
            except:
                return {'message': "An error occured  while try to insert item"}, 500
        else:
            try:
                ItemModel.update(updated_item)
            except:
                return {'message': "An error occured while try to update item"}, 500
        return updated_item


class ItemList(Resource):
    """
        Return lsit with items
    """
    def get(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        data = result.fetchall()
        connection.close()
        result = []
        for line in data:
            item = {'name': line[0], 'price': line[1]}
            result.append(item)
        return {'items': result}

