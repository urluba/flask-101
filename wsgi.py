from flask import Flask, jsonify
app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"

@app.route('/api/v1/products')
def products():
    the_products = [
        { 'id': 1, 'name': 'Skello' },
        { 'id': 2, 'name': 'Socialive.tv' },
        { 'id': 3, 'name': 'Truc' },
        { 'id': 4, 'name': 'Bidule' },
    ]

    return jsonify(the_products)

