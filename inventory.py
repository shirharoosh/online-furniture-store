from store_item import StoreItem
class Inventory:
    def __init__(self):
        self.items = {}  # Dictionary with item_id as keys and StoreItem objects as values

    def add_item(self, item: StoreItem):
        self.items[item.item_id] = item

    def remove_item(self, item_id: int):
        if item_id in self.items:
            del self.items[item_id]

    def update_quantity(self, item_id: int, quantity: int):
        if item_id in self.items:
            self.items[item_id].quantity = quantity

    def search_items(self, criteria: dict) -> list:
        # Implement search logic based on criteria
        pass