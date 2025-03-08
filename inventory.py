from typing import Dict, List, Optional
from store_item import StoreItem


class Inventory:
    """
    Manages the store's inventory using a dictionary mapping item ID's to quantity.

    Attributes:
        _items (Dict[int, int]): Dictionary mapping item IDs to their stock quantity.
        _catalog (Optional[Dict[int, StoreItem]]): Reference to the store catalog (maps item_id to StoreItem objects).
    """

    def __init__(self) -> None:
        """
        Initializes an empty inventory.
        """
        self._items: Dict[int, int] = {}  # Maps item_id to stock quantity.
        self._catalog: Optional[Dict[int, StoreItem]] = None # Reference to catalog

    def set_catalog(self, catalog: dict[int, StoreItem]) -> None:
        """
        Sets the catalog reference, ensuring the inventory always reflects catalog updates.

        Args:
            catalog (Dict[int, StoreItem]): Dictionary mapping item_id to StoreItem objects.
        """
        self._catalog = catalog  # Keep a direct Store reference to catalog.

    def get_catalog(self) -> dict[int, StoreItem]:
        """
        Returns a copy of the catalog to prevent direct modifications.

        Returns:
            Dict[int, StoreItem]: A copy of the catalog if available, else an empty dictionary.
        """
        return self._catalog.copy() if self._catalog else {}

    def add_item(self, item_id: int, quantity: int) -> None:
        """
        Adds stock to an existing item or creates a new entry.

        Args:
            item_id (int): The unique ID of the item to add.
            quantity (int): The number of units to add.
        """
        if item_id in self._items:
            self._items[item_id] += quantity
        else:
            self._items[item_id] = quantity

    def remove_item(self, item_id: int) -> None:
        """
        Removes an item from the inventory.

        Args:
            item_id (int): The unique ID of the item to remove.
        """
        if item_id in self._items:
            del self._items[item_id]

    def update_quantity(self, item_id: int, quantity: int) -> None:
        """
        Updates the quantity of an existing item.

        Args:
            item_id (int): The unique ID of the item to update.
            quantity (int): The new quantity to set.
        """
        if item_id in self._items:
            self._items[item_id] = quantity

    def get_quantity(self, item_id: int) -> int:
        """
        Retrieves the stock quantity of an item.

        Args:
            item_id (int): The unique ID of the item.

        Returns:
            int: The number of units in stock (0 if the item is not found).
        """
        return self._items.get(item_id, 0)

    def search_items(self, name: Optional[str] = None, category: Optional[str] = None,
                     min_price: Optional[float] = None, max_price: Optional[float] = None) -> List[StoreItem]:
        """
        Searches for items based on name, category, and price range.

        - Since inventory only stores {item_id: quantity}, we need a separate list of StoreItem objects.
        - Items will be matched using their item_id.

        Args:
            name (Optional[str]): Search term for item name (case insensitive).
            category (Optional[str]): Category (class name) to filter items.
            min_price (Optional[float]): Minimum price filter.
            max_price (Optional[float]): Maximum price filter.

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

        Returns:
            Dict[int, int]: A dictionary mapping item IDs to their quantities.
        """
        return self._items

    def __repr__(self):
        """
        Returns a string representation of the inventory.

        Returns:
            str: A formatted string displaying the inventory.
        """
        return f"Inventory({self._items})"
