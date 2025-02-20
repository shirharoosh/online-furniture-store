from typing import Dict, List
from store_item import StoreItem


class Inventory:
    """
    Manages the store's inventory with only item_id and quantity.
    Uses a dictionary: {item_id: quantity}
    """

    def __init__(self):
        self._items: Dict[int, int] = {}  # item_id -> quantity
        self._catalog = None

    def set_catalog(self, catalog: dict) -> None:
        """
        Sets the catalog reference, ensuring inventory always reflects catalog updates
        """
        self._catalog = catalog  # Keep a direct reference to the original

    def get_catalog(self) -> dict:
        """Returns a copy of the catalog to prevent modifications."""
        return self._catalog.copy() if self._catalog else {}

    def add_item(self, item_id: int, quantity: int) -> None:
        """
        Adds stock to an existing item or creates a new entry.
        """
        if item_id in self._items:
            self._items[item_id] += quantity
        else:
            self._items[item_id] = quantity

    def remove_item(self, item_id: int) -> None:
        """
        Removes an item from the inventory.
        """
        if item_id in self._items:
            del self._items[item_id]

    def update_quantity(self, item_id: int, quantity: int) -> None:
        """
        Updates the quantity of an existing item.
        """
        if item_id in self._items:
            self._items[item_id] = quantity

    def get_quantity(self, item_id: int) -> int:
        """
        Returns the quantity of an item.
        """
        return self._items.get(item_id, 0)

    def search_items(self, name: str = None, category: str = None,
                     min_price: float = None, max_price: float = None) -> List[StoreItem]:
        """
        Searches for items based on name, category, and price range.
        - Since inventory only stores {item_id: quantity}, we need a separate list of StoreItem objects.
        - Items will be matched using their item_id.

        Args:
            name (str): Search by name.
            category (str): Search by category (class name).
            min_price (float): Minimum price filter.
            max_price (float): Maximum price filter.

        Returns:
            List[StoreItem]: List of matching StoreItem objects.
        """
        available_items = self.get_catalog().values() # returns a list of SroreItems
        results = []
        for item in available_items:
            # Ensure the item exists in inventory (by checking item_id)
            if item.item_id not in self._items:
                continue

            if name and name.lower() not in item.title.lower():
                continue
            if category and category.lower() != item.__class__.__name__.lower():
                continue
            if min_price and item.price < min_price:
                continue
            if max_price and item.price > max_price:
                continue

            results.append(item)

        return results

    @property
    def items(self) -> Dict[int, int]:
        """
        Provides read-only access to the inventory dictionary.
        """
        return self._items

    def __repr__(self):
        return f"Inventory({self._items})"
