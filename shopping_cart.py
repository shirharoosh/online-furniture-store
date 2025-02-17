class ShoppingCart:
    def __init__(self):
        self.cart_items = {}  # item_id: quantity
        self.total_price = 0.0

    def add_item(self, inventory: Inventory, item_id: int, quantity: int):
        if item_id in inventory.items:
            self.cart_items[item_id] = quantity
            self.total_price += inventory.items[item_id].price * quantity

    def remove_item(self, item_id: int):
        if item_id in self.cart_items:
            del self.cart_items[item_id]

