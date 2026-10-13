
class InventoryService:
    def __init__(self):
        self.products = {}
        self.orders = {}

    def add_product(self, product_id, name, price, stock):
        self.products[product_id] = {
            "id": product_id,
            "name": name,
            "price": price,
            "stock": stock,
        }

    def get_product(self, product_id):
        return self.products.get(product_id)

    def update_stock(self, product_id, quantity):
        product = self.products.get(product_id)
        if product is None:
            return False

        if quantity < 0:
            return False

        product["stock"] = quantity
        return True

    def total_inventory_value(self):
        total = 0
        for product in self.products.values():
            total += product["price"] * product["stock"]
        return total

    def reserve_stock(self, product_id, quantity):
        product = self.products.get(product_id)
        if product is None:
            return False

        if quantity <= 0 or product["stock"] < quantity:
            return False

        product["stock"] -= quantity
        return True

    def create_order(self, order_id, items):
        if order_id in self.orders or not items:
            return False
        for item in items:
            id = item["product_id"]
            quantity = item["quantity"]
            if not self.get_product(id) or self.get_product(id)["stock"] < quantity or quantity <= 0:
                return False
        for item in items:
            id = item["product_id"]
            quantity = item["quantity"]
            self.reserve_stock(id, quantity)
        self.orders[order_id] = items
        return True


if __name__ == "__main__":
    inventory = InventoryService()

    inventory.add_product("p1", "Keyboard", 50.00, 10)
    inventory.add_product("p2", "Mouse", 25.00, 20)
    inventory.add_product("p3", "Monitor", 200.00, 5)

    print("Keyboard:", inventory.get_product("p1"))
    print("Total inventory value:", inventory.total_inventory_value())
    assert inventory.total_inventory_value() == 2000.0
    print("Reserve 3 keyboards:", inventory.reserve_stock("p1", 3))
    assert inventory.get_product("p1")["stock"] == 7
    print("Keyboard after reservation:", inventory.get_product("p1"))

    assert not inventory.reserve_stock("p1", 10)
    assert not inventory.reserve_stock("p0", 3)
    assert not inventory.reserve_stock("p3", 0)
    assert not inventory.reserve_stock("p3", -10)

    assert inventory.update_stock("p1", 10)
    assert inventory.get_product("p1")["stock"] == 10
    assert not inventory.update_stock("p0", 3)
    assert inventory.update_stock("p3", 0)
    assert inventory.get_product("p3")["stock"] == 0
    assert not inventory.update_stock("p3", -10)

    inventory.update_stock("p1", 10)
    inventory.update_stock("p2", 10)
    inventory.update_stock("p3", 10)

    test_create_order()