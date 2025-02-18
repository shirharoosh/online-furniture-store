from typing import List, Dict
from store_item import StoreItem


class Inventory:
    """
    Manages the store's inventory of items.
    """

    def __init__(self):
        self._items: Dict[int, StoreItem] = {}

    def add_item(self, item: StoreItem) -> None:
        self._items[item.item_id] = item

    def remove_item(self, item_id: int) -> None:
        if item_id in self._items:
            del self._items[item_id]

    def update_quantity(self, item_id: int, quantity: int) -> None:
        if item_id in self._items:
            self._items[item_id].quantity = quantity

    def search_items(self, criteria: dict) -> List[StoreItem]:
        results = []
        for item in self._items.values():
            if 'name' in criteria and criteria['name'].lower() not in item.title.lower():
                continue
            if 'category' in criteria and criteria['category'].lower() != item.__class__.__name__.lower():
                continue
            if 'min_price' in criteria and item.price < criteria['min_price']:
                continue
            if 'max_price' in criteria and item.price > criteria['max_price']:
                continue
            results.append(item)
        return results

    @property
    def items(self) -> Dict[int, StoreItem]:
        return self._items

    def __repr__(self):
        return f"Inventory({list(self._items.values())})"
