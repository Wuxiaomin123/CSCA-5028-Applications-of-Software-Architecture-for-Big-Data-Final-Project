import unittest
from flask_testing import TestCase
from app import exec_stock_strategy
from app import app


class STOCK():
    def __init__(self, open_price) -> None:
        self.open = open_price

class test_tool(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_unit_positive_strategy(self):
        code = 'test'
        open_prices = [1,0,1,0,1]
        stock_info = []
        for price in open_prices:
            stock_info.append(STOCK(price))
        response = exec_stock_strategy(code, stock_info)
        self.assertEqual(response, f'{code} is recommend!!!<br>')
    
    def test_unit_negitive_strategy(self):
        code = 'test'
        open_prices = [1,1,1,0,1]
        stock_info = []
        for price in open_prices:
            stock_info.append(STOCK(price))
        response = exec_stock_strategy(code, stock_info)
        self.assertEqual(response, f'{code} is not recommend<br>')
    
    def test_Integration_connection(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_Integration_collection(self):
        response = self.client.post('/collect',
                    data = {
                        'user_input': 'goog'
                    })
        self.assertEqual(response.data, b"message sent !")


if __name__ == '__main__':
    unittest.main()