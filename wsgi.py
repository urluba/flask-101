from flask import Flask, jsonify, request
from uuid import uuid4
import logging

app = Flask(__name__)

class ProductDb:
    @property
    def values(self):
        return self.db

    def __init__(self, values):
        if values:
            self.db = values
        else:
            self.db = list()

    def get(self, id: int) -> dict:
        return self.search(key='id', value=id)

    def search(self, key: str, value: str) -> dict:
        for product in self.db:
            if product[key] == value:
                logging.debug('Found product: "%s"', product)
                return product

        return None

    def delete(self, id: int) -> bool:
        product = self.get(id)

        if product:
            self.db.remove(product)
            return True

        return False

    def add(self, new_product: dict) -> dict:
        new_product.update({'id': uuid4()})
        self.db.append(new_product)

        logging.debug('Adding %s to DB', new_product)

        return new_product

the_products = ProductDb(
    [
        { 'id': 1, 'name': 'Skello' },
        { 'id': 2, 'name': 'Socialive.tv' },
    ]
)

# @app.errorhandler(204) TODO
def no_content():
    return '', 204

def created(product, message='OK'):
    message = {
            'status': 201,
            'message': message,
            'product': product,

    }
    resp = jsonify(message)
    resp.status_code = 201

    logging.debug('Created returned %s', message)
    return resp

@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.errorhandler(400)
def bad_request(error='Bad Request'):
    message = {
            'status': 400,
            'message': error,
    }
    resp = jsonify(message)
    resp.status_code = 400

    return resp

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/api/v1/products', methods=['GET'])
def products():
    return jsonify(the_products.values)

@app.route('/api/v1/products', methods=['POST'])
def post_product():
    payload = request.get_json()
    logging.debug('Received payload %s', payload)

    if payload:
        product = the_products.add(payload)
        return created(product)

    return bad_request()

@app.route('/api/v1/products/<productid>', methods=['GET'])
def get_productid(productid: str):
    product = the_products.get(int(productid))

    if product:
        return jsonify(product)

    return not_found()

@app.route('/api/v1/products/<productid>', methods=['DELETE'])
def delete_productid(productid: str):
    result = the_products.delete(int(productid))
    
    if result:
        return no_content()
    else:
        return not_found()
