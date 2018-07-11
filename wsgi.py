from flask import Flask, jsonify, request
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
        for product in self.db:
            if product['id'] == id:
                logging.debug('Found product %s: "%s"', id, product)
                return product

        return None

    def delete(self, id: int) -> bool:
        product = self.get(id)

        if product:
            self.db.remove(product)
            return True

        return False

the_products = ProductDb(
    [
        { 'id': 1, 'name': 'Skello' },
        { 'id': 2, 'name': 'Socialive.tv' },
        { 'id': 3, 'name': 'Truc' },
        { 'id': 4, 'name': 'Bidule' },
        { 'id': 5, 'name': 'Flute' },
    ]
)

# @app.errorhandler(204) TODO
def no_content():
    return '', 204

@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/api/v1/products')
def products():
    return jsonify(the_products.values)

@app.route('/api/v1/products/<productid>', methods=['GET'])
def get_productid(productid: str):
    product = the_products.get(int(productid))

    if product:
        return jsonify(product)

    return not_found(error='Product id not found')

@app.route('/api/v1/products/<productid>', methods=['DELETE'])
def delete_productid(productid: str):
    result = the_products.delete(int(productid))
    
    if result:
        return no_content()
    else:
        return not_found()
