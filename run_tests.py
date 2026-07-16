import unittest
from price_comparator import compare_prices, STATUS_ABOVE_THRESHOLD, STATUS_WITHIN_THRESHOLD, VARIANCE_THRESHOLD

class TestPriceComparator(unittest.TestCase):
    def setUp(self):
        self.master = {"WidgetA": 5.0, "GadgetB": 12.0}

    def test_all_within_threshold(self):
        items = [
            {"supplier_name": "TestSupplier", "item": "WidgetA", "price": 5.0},
            {"supplier_name": "TestSupplier", "item": "GadgetB", "price": 12.0}
        ]
        result = compare_prices(items, self.master)
        self.assertEqual(result["status"], STATUS_WITHIN_THRESHOLD)
        self.assertEqual(result["title"], "TestSupplier")

    def test_one_above_threshold(self):
        items = [
            {"supplier_name": "TestSupplier", "item": "WidgetA", "price": 6.0},
            {"supplier_name": "TestSupplier", "item": "GadgetB", "price": 12.0}
        ]
        result = compare_prices(items, self.master)
        self.assertEqual(result["status"], STATUS_ABOVE_THRESHOLD)
        diff = result["variances"][0]["diff_percent"]
        self.assertAlmostEqual(diff, 0.2)

    def test_missing_item_in_master(self):
        items = [
            {"supplier_name": "TestSupplier", "item": "WidgetA", "price": 5.0},
            {"supplier_name": "TestSupplier", "item": "UnknownItem", "price": 10.0}
        ]
        result = compare_prices(items, self.master)
        self.assertEqual(result["status"], STATUS_ABOVE_THRESHOLD)
        self.assertIsNone(result["variances"][1]["master_price"])
        self.assertIsNone(result["variances"][1]["diff_percent"])

    def test_empty_master(self):
        items = [
            {"supplier_name": "TestSupplier", "item": "WidgetA", "price": 5.0}
        ]
        result = compare_prices(items, {})
        self.assertEqual(result["status"], STATUS_ABOVE_THRESHOLD)
        self.assertIsNone(result["variances"][0]["master_price"])

if __name__ == "__main__":
    unittest.main()
