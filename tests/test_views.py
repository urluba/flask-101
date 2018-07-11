# tests/test_views.py
from flask_testing import TestCase
from wsgi import app, ProductDb

class TestViews(TestCase):
    # def setUp(self):

    #     the_products = ProductDb(
    #         [
    #             { 'id': 1, 'name': 'Skello' },
    #             { 'id': 2, 'name': 'Socialive.tv' },
    #             { 'id': 3, 'name': 'Truc' },
    #             { 'id': 4, 'name': 'Bidule' },
    #         ]
    #     )

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_delete_missing_product(self):
        response = self.client.delete("/api/v1/products/666")
        self.assertEquals(response.status_code, 404)

    def test_delete_product(self):
        response = self.client.delete("/api/v1/products/4")
        self.assertEquals(response.status_code, 204)

        response = self.client.get("/api/v1/products/4")
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
        response = self.client.get("/api/v1/products")
        products = response.json
        self.assertIsInstance(products, list)
        self.assertGreater(len(products), 3) # 3 is not a mistake here.