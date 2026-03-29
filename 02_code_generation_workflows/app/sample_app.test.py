# sample_app.test.py - Tests for inventory management module
import unittest

from sample_app import get_product, update_stock, calculate_order_total


class TestGetProduct(unittest.TestCase):
    def test_existing_product(self):
        result = get_product("PROD-001")
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "Wireless Headphones")

    def test_missing_product(self):
        result = get_product("PROD-999")
        self.assertIsNone(result)


class TestUpdateStock(unittest.TestCase):
    def test_add_stock(self):
        result = update_stock("PROD-001", 10)
        self.assertIsNotNone(result)

    def test_invalid_product(self):
        result = update_stock("PROD-999", 5)
        self.assertIsNone(result)

    def test_negative_result(self):
        result = update_stock("PROD-003", -5)
        self.assertIsNone(result)


class TestCalculateOrderTotal(unittest.TestCase):
    def test_single_item(self):
        items = [{"product_id": "PROD-001", "quantity": 2}]
        result = calculate_order_total(items)
        self.assertEqual(result["total"], 159.98)

    def test_multiple_items(self):
        items = [
            {"product_id": "PROD-001", "quantity": 1},
            {"product_id": "PROD-002", "quantity": 1},
        ]
        result = calculate_order_total(items)
        self.assertEqual(result["total"], 129.98)

    def test_empty_order(self):
        result = calculate_order_total([])
        self.assertEqual(result["total"], 0)


if __name__ == "__main__":
    unittest.main()
