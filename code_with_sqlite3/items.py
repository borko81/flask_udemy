import sqlite3
from sqlite3 import connect
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from flask import request


class Item(Resource):
    """
        Return possible item
    """

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='price input')

    def get(self, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT * FROM items where name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {"item": {'name': row[0], 'price': row[1]}}
        return {'message': 'Item not found'}, 404

    def post(self, name):
        """
            Create new item, get price from request.get_json()
        """
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES(?, ?)"
        data = Item.parser.parse_args()
        cursor.execute(query, (name, data['price']))
        connection.commit()
        connection.close()
        return {'message': 'New item was created'}, 201

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
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = 'UPDATE items SET price=? WHERE name=?'
        cursor.execute(query, (data['price'], name,))
        connection.commit()
        connection.close()
        return {'message': 'Item was updated successfully'}, 201


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

