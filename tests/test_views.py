# tests/test_views.py
from flask_testing import TestCase
from wsgi import app, the_products, ProductDb

class TestViews(TestCase):
    def setUp(self):
        the_products.db = [
                { 'id': 1, 'name': 'Skello' },
                { 'id': 2, 'name': 'Socialive.tv' },
                { 'id': 3, 'name': 'Truc' },
        ]

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_productdb_add(self):
        result = the_products.add({'name': 'Bidule'})
        self.assertTrue(result)

        product = the_products.search(key='name', value='Bidule')
        self.assertIsInstance(product, dict)
        self.assertEquals(product['name'], 'Bidule')

    def test_post_product(self):
        payload = {'name': 'test_post'}
        response = self.client.post(
            "/api/v1/products",
            json=payload
        )
        product = response.json

        self.assertEquals(response.status_code, 201)

        product = the_products.search(key='name', value='test_post')
        self.assertIsInstance(product, dict)
        self.assertEquals(product['name'], 'test_post')

    def test_delete_missing_product(self):
        response = self.client.delete("/api/v1/products/666")
        self.assertEquals(response.status_code, 404)

    def test_delete_product(self):
        response = self.client.delete("/api/v1/products/1")
        self.assertEquals(response.status_code, 204)

        response = self.client.get("/api/v1/products/1")
        self.assertEquals(response.status_code, 404)

    def test_get_existing_product_by_id(self):
        response = self.client.get("/api/v1/products/1")
        product = response.json
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(product, dict)
        self.assertEquals(product['id'], 1)

    def test_get_missing_product_by_id(self):
        response = self.client.get("/api/v1/products/666")
        self.assertEquals(response.status_code, 404)

    def test_products_json(self):
        the_products.add({'name': 'Bidule'})
        the_products.add({'name': 'Bidule'})

        response = self.client.get("/api/v1/products")
        products = response.json
        self.assertIsInstance(products, list)
        self.assertGreater(len(products), 3) # 3 is not a mistake here.