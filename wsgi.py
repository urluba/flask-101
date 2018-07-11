from flask import Flask, jsonify, request
import logging

app = Flask(__name__)

the_products = [
    { 'id': 1, 'name': 'Skello' },
    { 'id': 2, 'name': 'Socialive.tv' },
    { 'id': 3, 'name': 'Truc' },
    { 'id': 4, 'name': 'Bidule' },
]

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
    return jsonify(the_products)

@app.route('/api/v1/products/<productid>')
def get_productid(productid: str):
    productid = int(productid)

    for product in the_products:
        if product['id'] == productid:
            logging.debug('Found product %s: "%s"', productid, product)
            return jsonify(product)

    return not_found(error='Product id not found')
