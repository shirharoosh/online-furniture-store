from typing import Dict
from inventory import Inventory
from store_item import StoreItem


class ShoppingCart:
    """
    Manages a shopping cart for users.
    - Uses a dictionary: {item_id: quantity}
    - Keeps track of total price dynamically.
    - Does NOT modify inventory until checkout.
    """

    def __init__(self, inventory: Inventory) -> None:
        """
        Initializes the shopping cart.
        - Links to inventory for stock verification.
        - Uses a dictionary to store cart items (item_id -> quantity).
        - Tracks total cart price.
        """
        self._inventory = inventory  # Reference to store inventory
        self._cart_items: Dict[int, int] = {}  # Stores {item_id: quantity}
        self._total_price: float = 0.0  # Tracks total price of items in the cart

    def add_furniture(self, catalog, item_id: int, quantity: int = 1) -> None:
        """
        Adds furniture to the shopping cart.
        - Checks inventory to ensure enough stock exists.
        - Updates cart dictionary.
        - Adjusts total price accordingly.
        """
        # Check if item exists in inventory
        if item_id not in self._inventory.items:
            print("Item not found in inventory.")
            return

        # Check if requested quantity is available (but do NOT modify inventory)
        available_quantity = self._inventory.get_quantity(item_id)
        if available_quantity < quantity:
            print(f"Not enough stock available. Only {available_quantity} left.")
            return

        # Add item to cart
        self._cart_items[item_id] = self._cart_items.get(item_id, 0) + quantity

        # Update total price
        store_item = self.get_item_by_id(item_id, catalog)
        self._total_price += store_item.price * quantity

        print(f"Added {quantity}x {store_item.title} to cart. Total: ${self._total_price:.2f}")

    def remove_furniture(self, catalog, item_id: int, quantity: int = 1) -> None:
        """
        Removes furniture from the shopping cart.
        - Updates total price dynamically.
        - Does NOT modify inventory.
        """
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
        """
        print(f"Total price for your cart: ${self._total_price:.2f}")

    def apply_discount(self, discount_percentage: float) -> None:
        """
        Applies a discount to the total cart price.
        - Ensures discount is valid (0-100%).
        """
        if discount_percentage <= 0 or discount_percentage > 100:
            print("Invalid discount percentage.")
            return

        discount_amount = (discount_percentage / 100) * self._total_price
        discounted_price = self._total_price - discount_amount

        self._total_price = discounted_price

        print(f"Discount applied: ${discount_amount:.2f}, New Total: ${discounted_price:.2f}")

    def get_item_by_id(self, item_id, catalog):
        return catalog[item_id]



    def __repr__(self):
        return f"ShoppingCart(items={self._cart_items}, total_price=${self._total_price:.2f})"



