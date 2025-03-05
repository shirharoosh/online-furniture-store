from typing import Dict
from inventory import Inventory
from store_item import StoreItem


class ShoppingCart:
    """
    Manages a shopping cart for users.

    Attributes:
        _inventory (Inventory): Reference to the store's inventory.
        _cart_items (Dict[int, int]): Dictionary mapping item IDs to quantities.
        _total_price (float): Total cost of the items in the cart.

    Notes:
        - This class does NOT modify inventory stock until checkout.
        - Uses an internal dictionary to track item quantities.
    """

    def __init__(self, inventory: Inventory) -> None:
        """
        Initializes the shopping cart.

        Args:
            inventory (Inventory): The store inventory for checking item availability.
        """
        self._inventory = inventory  # Reference to store inventory
        self._cart_items: Dict[int, int] = {}  # Stores {item_id: quantity}
        self._total_price: float = 0.0  # Tracks total price of items in the cart

    def add_furniture(self, item_id: int, quantity: int = 1) -> None:
        """
        Adds furniture to the shopping cart.

        - Checks inventory to ensure enough stock is available.
        - Updates cart dictionary.
        - Adjusts total price dynamically.

        Args:
            item_id (int): The ID of the item to add.
            quantity (int, optional): The quantity to add (default is 1).

        Returns:
            None

        """
        catalog = self._inventory.get_catalog()

        # Check if item exists in inventory
        if item_id not in self._inventory.items:
            print("Item not found in inventory.")
            return

        # Check if requested quantity is available (but do NOT modify inventory)
        available_quantity = self._inventory.get_quantity(item_id)
        if item_id in self._cart_items.keys():
            if available_quantity < (quantity + self._cart_items[item_id]):
                print(f"Not enough stock available. Only {available_quantity} left.")
                return
        else:
            if available_quantity < quantity:
                print(f"Not enough stock available. Only {available_quantity} left.")
                return

        # Add item to cart
        self._cart_items[item_id] = self._cart_items.get(item_id, 0) + quantity

        # Update total price
        store_item = self.get_item_by_id(item_id, catalog)
        self._total_price += store_item.price * quantity

        print(f"Added {quantity}x {store_item.title} to cart. Total: ${self._total_price:.2f}")

    def remove_furniture(self, item_id: int, quantity: int = 1) -> None:
        """
        Removes furniture from the shopping cart.

        - Updates total price dynamically.
        - Does NOT modify inventory.

        Args:
            item_id (int): The ID of the item to remove.
            quantity (int, optional): The quantity to remove (default is 1).

        Returns:
            None
        """
        catalog = self._inventory.get_catalog()
        # Check if item is in the cart
        if item_id not in self._cart_items:
            print("Item not found in cart.")
            return

        # Ensure valid quantity to remove
        if self._cart_items[item_id] < quantity:
            print("Not enough quantity in cart to remove.")
            return

        # Retrieve item details
        store_item = self.get_item_by_id(item_id, catalog = catalog)

        # Update cart
        self._cart_items[item_id] -= quantity
        if self._cart_items[item_id] == 0:
            del self._cart_items[item_id]  # Remove item if quantity reaches 0

        # Update total price
        self._total_price -= store_item.price * quantity

        print(f"Removed {quantity}x {store_item.title} from cart. Total: ${self._total_price:.2f}")

    def show_total_price(self) -> None:
        """
        Displays the current total price of items in the cart.

        Returns:
            None
        """
        print(f"Total price for your cart: ${self._total_price:.2f}")

    def apply_discount(self, discount_percentage: float) -> None:
        """
        Applies a discount to the total cart price.

        - Ensures the discount is between 0% and 100%.
        - Adjusts the total price dynamically.

        Args:
            discount_percentage (float): Discount percentage (e.g., 10 for 10%).

        Returns:
            None
        """
        if discount_percentage <= 0 or discount_percentage > 100:
            print("Invalid discount percentage.")
            return

        discount_amount = (discount_percentage / 100) * self._total_price
        discounted_price = self._total_price - discount_amount

        self._total_price = discounted_price

        print(f"Discount applied: ${discount_amount:.2f}, New Total: ${discounted_price:.2f}")

    def get_item_by_id(self, item_id: int, catalog: Dict[int, StoreItem]) -> StoreItem:
        """
        Retrieves an item from the catalog by its ID.

        Args:
            item_id (int): The ID of the item to retrieve.
            catalog (Dict[int, StoreItem]): The store's catalog.

        Returns:
            StoreItem: The requested item.
        """
        return catalog[item_id]

    def __repr__(self):
        """
        Returns a string representation of the shopping cart.

        Returns:
            str: A formatted string displaying cart contents and total price.
        """
        return f"ShoppingCart(items={self._cart_items}, total_price=${self._total_price:.2f})"



