from flask import Flask, jsonify, request


app = Flask(__name__)

stores = [
    {
        "name": "My wonderfull",
        "items": [
            {"name": "My Items", "price": 15.99}
        ]
    }
]


# POST /store data: {name}
@app.route("/store", methods=["POST"])
def create_store():
    # Get data from request.get_json()
    # stores append new data
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)


# GET /store/name
@app.route("/store/<string:name>")
def get_store(name):
    # Iterate over stores
    # if the store name mathces, return it
    # if not matches, return error message
    for store in stores:
        if store['name'] == name:
            return jsonify(name)
    return jsonify({'message': f'error, {name} not found'})


# GET /store
@app.route("/store")
def get_stores():
    # Return all stores
    return jsonify({'stores': stores})


@app.route("/store/<string:name>/items", methods=["POST"])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_items = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_items)
            return jsonify(new_items)
    return jsonify({'message': 'store not found'})


@app.route("/store/<string:name>/items")
def get_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store['items'])
    return jsonify({'message': 'store not found'})


if __name__ == "__main__":
    app.run(debug=True)
