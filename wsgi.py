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

    def modify(self, id: int, new_product: dict) -> dict:
        product = self.get(id)

        if product:
            product.update(new_product)
            return product
        else:
            return None


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
    payload = {
            'status': 201,
            'message': message,
            'product': product,
            'url': f'{request.url}/{product["id"]}',

    }
    resp = jsonify(payload)
    resp.status_code = 201

    logging.debug('Created returned %s', payload)
    return resp

@app.errorhandler(422)
def unprocessable_entity(error=None):
    return error_4xx(422, message=error)

@app.errorhandler(404)
def not_found(error=None):
    return error_4xx(404, message=error)

@app.errorhandler(400)
def bad_request(error='Bad Request'):
    return error_4xx(400, message=error)

def error_4xx(status_code, message):
    message = {
            'status': status_code,
            'message': message,
            'url': request.url,
    }
    resp = jsonify(message)
    resp.status_code = status_code

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

@app.route('/api/v1/products/<int:productid>', methods=['GET'])
def get_productid(productid: str):
    product = the_products.get(productid)

    if product:
        return jsonify(product)

    return not_found()

@app.route('/api/v1/products/<int:productid>', methods=['DELETE'])
def delete_productid(productid: str):
    result = the_products.delete(productid)
    
    if result:
        return no_content()
    else:
        return not_found()

@app.route('/api/v1/products/<int:productid>', methods=['PATCH'])
def patch_productid(productid: str):
    result = the_products.modify(
        productid,
        request.get_json()
    )
    
    if result:
        return no_content()
    else:
        return unprocessable_entity()
