from collections import defaultdict
from typing import Dict
from inventory import Inventory
from store_item import StoreItem

class ShoppingCart:
    def __init__(self, inventory: Inventory) -> None:
        """
        Initialize a shopping cart with reference to inventory.
        """
        self.inventory = inventory #link to store's inventory
        self.cart_items: Dict[int, int] = defaultdict(int) #stores item_id -> quantity
        self.total_price: float = 0.0
        self.discount: float = 0.0

    def add_item(self, item_id: int, quantity: int = 1) -> None:
        """
        Add an item to cart and update store inventory.
        """
        if item_id not in self.inventory.items:
            print("Item not found in inventory")
            return
        
        item = self.inventory.items[item_id]

        if item.quantity < quantity:
            print(f"Not enough stock available for {item.item_title}. Only {item.quantity} left.")
            return
        
        #Add item to cart
        self.cart_items[item_id] += quantity
        self.total_price += (item.price * quantity)

        #Update inventory stock
        self.inventory.update_quantity(item_id, item.quantity - quantity)

        print(f"Added {quantity}x {item.item_title} to cart. Total: ${self.total_price:.2f}")

    def remove_item(self, item_id: int, quantity: int = 1) -> None:
        """
        Remove item from cart and update store inventory.
        """
        if item_id not in self.cart_items:
            print("Item not found")
            return
        
        item = self.inventory.items[item_id]

        if self.cart_items[item_id] < quantity:
            print("Not enough quantity in cart to remove.")
            return
        
        #Remove item from cart
        self.cart_items[item_id] -= quantity
        self.total_price -= (item.price * quantity)

        if self.cart_items == 0:
            del self.cart_items[item_id]

        #Restore quantity back to store inventory
        self.inventory.update_quantity(item_id, item.quantity + quantity)

        print(f"Removed {quantity}x {item.item_title} from cart. Total: ${self.total_price:.2f}")

    def apply_discount(self, discount_percentage: float) -> None:
        """
        Apply a discount to the total cart price.
        """
        if discount_percentage <= 0 or discount_percentage > 100:
            print("Invalid discount percentage.")
            return
        
        self.discount = (discount_percentage / 100) * self.total_price
        discounted_price: float = self.total_price - self.discount
        print(f"Discount applied: ${self.discount:.2f}, New Total: ${discounted_price:.2f}")


    def view_cart(self) -> None:
        """
        Display items in the cart and Total price..
        """
        if not self.cart_items:
            print("Your cart is currently empty.")
            return
        
        print("\nShopping Cart:")
        for item_id, quantity in self.cart_items.items():
            item = self.inventory.items[item_id]
            print(f"- {item.item_title}: {quantity} @ ${item.price:.2f} each")
        print(f"Total Price: ${self.total_price:.2f}")


    def show_price(self) -> float:
        """
        Returns the current total price of items in the cart.
        """
        print(f"Total price for your cart before discounts: ${self.total_price:.2f}")

