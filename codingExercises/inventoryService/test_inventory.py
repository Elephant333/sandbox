
import unittest

from inventory import InventoryService


class TestInventoryService(unittest.TestCase):
    def setUp(self):
        self.inventory = InventoryService()
        self.inventory.add_product("p1", "Keyboard", 50.00, 10)
        self.inventory.add_product("p2", "Mouse", 25.00, 20)
        self.inventory.add_product("p3", "Monitor", 200.00, 5)

    # add_product and get_product

    def test_get_existing_product(self):
        product = self.inventory.get_product("p1")
        self.assertEqual(product["name"], "Keyboard")
        self.assertEqual(product["price"], 50.00)
        self.assertEqual(product["stock"], 10)

    def test_get_nonexistent_product(self):
        self.assertIsNone(self.inventory.get_product("missing"))

    # update_stock

    def test_update_stock_success(self):
        self.assertTrue(self.inventory.update_stock("p1", 15))
        self.assertEqual(self.inventory.get_product("p1")["stock"], 15)

    def test_update_stock_to_zero(self):
        self.assertTrue(self.inventory.update_stock("p1", 0))
        self.assertEqual(self.inventory.get_product("p1")["stock"], 0)

    def test_update_stock_rejects_negative_quantity(self):
        self.assertFalse(self.inventory.update_stock("p1", -1))
        self.assertEqual(self.inventory.get_product("p1")["stock"], 10)

    def test_update_stock_rejects_missing_product(self):
        self.assertFalse(self.inventory.update_stock("missing", 5))

    # total_inventory_value

    def test_total_inventory_value(self):
        self.assertEqual(
            self.inventory.total_inventory_value(),
            2000.00,
        )

    def test_inventory_value_after_stock_update(self):
        self.inventory.update_stock("p1", 5)
        self.assertEqual(
            self.inventory.total_inventory_value(),
            1750.00,
        )

    # reserve_stock

    def test_reserve_stock_success(self):
        self.assertTrue(self.inventory.reserve_stock("p1", 3))
        self.assertEqual(self.inventory.get_product("p1")["stock"], 7)

    def test_reserve_stock_exact_available_quantity(self):
        self.assertTrue(self.inventory.reserve_stock("p1", 10))
        self.assertEqual(self.inventory.get_product("p1")["stock"], 0)

    def test_reserve_stock_rejects_insufficient_stock(self):
        self.assertFalse(self.inventory.reserve_stock("p1", 11))
        self.assertEqual(self.inventory.get_product("p1")["stock"], 10)

    def test_reserve_stock_rejects_zero_quantity(self):
        self.assertFalse(self.inventory.reserve_stock("p1", 0))
        self.assertEqual(self.inventory.get_product("p1")["stock"], 10)

    def test_reserve_stock_rejects_negative_quantity(self):
        self.assertFalse(self.inventory.reserve_stock("p1", -2))
        self.assertEqual(self.inventory.get_product("p1")["stock"], 10)

    def test_reserve_stock_rejects_missing_product(self):
        self.assertFalse(self.inventory.reserve_stock("missing", 1))

    # create_order

    def test_create_order_success(self):
        items = [
            {"product_id": "p1", "quantity": 2},
            {"product_id": "p2", "quantity": 3},
        ]

        self.assertTrue(self.inventory.create_order("o1", items))
        self.assertEqual(self.inventory.get_product("p1")["stock"], 8)
        self.assertEqual(self.inventory.get_product("p2")["stock"], 17)
        self.assertIn("o1", self.inventory.orders)

    def test_create_order_saves_items(self):
        items = [{"product_id": "p1", "quantity": 2}]

        self.inventory.create_order("o1", items)

        self.assertEqual(self.inventory.orders["o1"], items)

    def test_create_order_rejects_duplicate_id(self):
        items = [{"product_id": "p1", "quantity": 2}]
        self.assertTrue(self.inventory.create_order("o1", items))

        self.assertFalse(
            self.inventory.create_order(
                "o1",
                [{"product_id": "p2", "quantity": 1}],
            )
        )
        self.assertEqual(self.inventory.get_product("p1")["stock"], 8)
        self.assertEqual(self.inventory.get_product("p2")["stock"], 20)

    def test_create_order_rejects_empty_items(self):
        self.assertFalse(self.inventory.create_order("o1", []))
        self.assertNotIn("o1", self.inventory.orders)

    def test_create_order_rejects_missing_product(self):
        items = [{"product_id": "missing", "quantity": 1}]

        self.assertFalse(self.inventory.create_order("o1", items))
        self.assertNotIn("o1", self.inventory.orders)
        self.assertEqual(self.inventory.get_product("p1")["stock"], 10)

    def test_create_order_rejects_zero_quantity(self):
        items = [{"product_id": "p1", "quantity": 0}]

        self.assertFalse(self.inventory.create_order("o1", items))
        self.assertEqual(self.inventory.get_product("p1")["stock"], 10)
        self.assertNotIn("o1", self.inventory.orders)

    def test_create_order_rejects_negative_quantity(self):
        items = [{"product_id": "p1", "quantity": -2}]

        self.assertFalse(self.inventory.create_order("o1", items))
        self.assertEqual(self.inventory.get_product("p1")["stock"], 10)
        self.assertNotIn("o1", self.inventory.orders)

    def test_create_order_rejects_insufficient_stock(self):
        items = [{"product_id": "p1", "quantity": 11}]

        self.assertFalse(self.inventory.create_order("o1", items))
        self.assertEqual(self.inventory.get_product("p1")["stock"], 10)
        self.assertNotIn("o1", self.inventory.orders)

    def test_create_order_is_atomic_when_later_item_fails(self):
        items = [
            {"product_id": "p1", "quantity": 2},
            {"product_id": "p2", "quantity": 21},
        ]

        self.assertFalse(self.inventory.create_order("o1", items))

        # Neither product should be changed.
        self.assertEqual(self.inventory.get_product("p1")["stock"], 10)
        self.assertEqual(self.inventory.get_product("p2")["stock"], 20)
        self.assertNotIn("o1", self.inventory.orders)

    def test_create_order_rejects_missing_product_after_valid_item(self):
        items = [
            {"product_id": "p1", "quantity": 2},
            {"product_id": "missing", "quantity": 1},
        ]

        self.assertFalse(self.inventory.create_order("o1", items))
        self.assertEqual(self.inventory.get_product("p1")["stock"], 10)
        self.assertNotIn("o1", self.inventory.orders)

    def test_create_order_rejects_invalid_quantity_after_valid_item(self):
        items = [
            {"product_id": "p1", "quantity": 2},
            {"product_id": "p2", "quantity": 0},
        ]

        self.assertFalse(self.inventory.create_order("o1", items))
        self.assertEqual(self.inventory.get_product("p1")["stock"], 10)
        self.assertEqual(self.inventory.get_product("p2")["stock"], 20)
        self.assertNotIn("o1", self.inventory.orders)


if __name__ == "__main__":
    unittest.main()