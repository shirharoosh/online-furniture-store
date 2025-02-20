# api.py
"""
This API file implements a RESTful API for the online furniture store using FastAPI.
It exposes endpoints for:
 - Retrieving furniture items, orders, and user profiles (GET)
 - Registering users and logging in (POST)
 - Adding, updating, and removing items from the shopping cart and inventory (POST, PUT, DELETE)
 - Checking out to create orders

All data is stored in global (simulated) databases using dictionaries.
"""

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel
from typing import List, Optional
from inventory import Inventory
from shopping_cart import ShoppingCart
from user import User
from order import Order
from user_order_dic import UserOrderDictionary
from store_item import Table, Chair, Sofa

# Create a simulated "catalog" of furniture items.
# Our inventory will use only item IDs and quantities.
catalog = {
    101: Table(101, "Dining Table", 250, 75, 150, 30, "A sturdy wooden dining table."),
    102: Chair(102, "Office Chair", 80, 100, 50, 10, "An ergonomic office chair.", material="Leather"),
    103: Sofa(103, "Luxury Sofa", 500, 40, 200, 50, "A comfortable luxury sofa.", seating_capacity=3)
}

# Global simulated "databases"
global_inventory = Inventory()  # Manages stock as {item_id: quantity}
global_user_orders = UserOrderDictionary()  # Stores orders per user
user_accounts = {}  # Stores User objects indexed by email
shopping_carts = {}  # Stores ShoppingCart objects indexed by user email

# Initialize inventory with stock for items in our catalog.
global_inventory.add_item(101, 10)  # 10 Dining Tables
global_inventory.add_item(102, 15)  # 15 Office Chairs
global_inventory.add_item(103, 5)  # 5 Sofas
global_inventory.set_catalog(catalog)  # setting catalog as required in the updated inv

# Create FastAPI app instance
app = FastAPI(
    title="Online Furniture Store API",
    description="A RESTful API for managing furniture items, user profiles, shopping carts, and orders.",
    version="1.0.0"
)


# ------------------------------
# Pydantic Models for Request Data
# ------------------------------

class SignUpRequest(BaseModel):
    username: str
    full_name: str
    email: str
    password: str
    address: str
    phone_number: str


class LoginRequest(BaseModel):
    email: str
    password: str


class CartItemRequest(BaseModel):
    item_id: int
    quantity: int


class CheckoutRequest(BaseModel):
    email: str
    payment_method: str
    shipping_address: Optional[str] = None


class ProfileUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None


# ------------------------------
# Helper Functions
# ------------------------------

def get_user_by_email(email: str) -> User:
    if email not in user_accounts:
        raise HTTPException(status_code=404, detail="User not found")
    return user_accounts[email]


def get_cart_by_email(email: str) -> ShoppingCart:
    if email not in shopping_carts:
        raise HTTPException(status_code=404, detail="Shopping cart not found")
    return shopping_carts[email]


# ------------------------------
# API Endpoints
# ------------------------------

# --- User Management Endpoints ---
@app.post("/signup", summary="Register a new user", response_description="User registered")
def signup(user_data: SignUpRequest):
    """
    Register a new user. Uses the existing User.sign_up() method.
    """
    if user_data.email in user_accounts:
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = User(
        user_data.username,
        user_data.full_name,
        user_data.email,
        user_data.password,
        user_data.address,
        user_data.phone_number
    )
    # Call the sign_up method from the User class.
    message = new_user.sign_up()
    user_accounts[user_data.email] = new_user
    # Create a new shopping cart for the user.
    shopping_carts[user_data.email] = ShoppingCart(global_inventory)
    return {"message": message}


@app.post("/login", summary="Log in a user", response_description="User logged in")
def login(login_data: LoginRequest):
    """
    Log in an existing user. Uses the User.login() method.
    """
    if login_data.email not in user_accounts:
        raise HTTPException(status_code=404, detail="User not found. Please sign up.")
    user = user_accounts[login_data.email]
    result = user.login(login_data.email, login_data.password)
    if "logged in successfully" not in result:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"message": result}


@app.get("/users/{email}", summary="Get user profile", response_description="User profile")
def get_user_profile(email: str = Path(..., description="The email of the user")):
    """
    Retrieve the profile of a user.
    """
    user = get_user_by_email(email)
    # For security, we only return non-sensitive profile data.
    return {
        "username": user.username,
        "full_name": user.full_name,
        "email": user.email,
        "address": user._address,
        "phone_number": user._phone_number,
        "order_history": user.view_order_history()
    }


@app.put("/users/{email}", summary="Update user profile", response_description="Profile updated")
def update_user_profile(email: str, profile: ProfileUpdateRequest):
    """
    Update user profile information.
    """
    user = get_user_by_email(email)
    result = user.manage_profile(profile.full_name, profile.address, profile.phone_number)
    return {"message": result}


# --- Furniture Items Endpoints ---
@app.get("/items", summary="Get all furniture items", response_description="List of furniture items")
def get_all_items():
    """
    Retrieve a list of all furniture items from the catalog, along with available quantities.
    """
    items_list = []
    for item_id, item in catalog.items():
        available = global_inventory.get_quantity(item_id)
        items_list.append({
            "item_id": item_id,
            "title": item.title,
            "price": item.price,
            "description": item.description,
            "available_quantity": available
        })
    return {"items": items_list}


# --- Shopping Cart Endpoints ---
@app.post("/cart/add", summary="Add item to shopping cart", response_description="Item added to cart")
def add_item_to_cart(cart_item: CartItemRequest, email: str = Query(..., description="User email")):
    """
    Add an item to the shopping cart. Checks inventory to ensure enough stock exists.
    (Note: Inventory is only checked, not updated, until checkout.)
    """
    cart = get_cart_by_email(email)
    cart.add_furniture(cart_item.item_id, cart_item.quantity)
    return {"message": "Item added to cart", "cart": cart._cart_items, "total_price": cart._total_price}


@app.put("/cart/update", summary="Update item quantity in cart", response_description="Cart updated")
def update_cart_item(cart_item: CartItemRequest, email: str = Query(..., description="User email")):
    """
    Update the quantity of an item in the shopping cart.
    For simplicity, we remove the item and add it with the new quantity.
    """
    cart = get_cart_by_email(email)
    # Remove the item completely first
    if cart_item.item_id in cart._cart_items:
        current_quantity = cart._cart_items[cart_item.item_id]
        cart.remove_furniture(cart_item.item_id, current_quantity)
    # Add the item with new quantity
    cart.add_furniture(cart_item.item_id, cart_item.quantity)
    return {"message": "Cart updated", "cart": cart._cart_items, "total_price": cart._total_price}


@app.delete("/cart/delete/{item_id}", summary="Remove item from cart", response_description="Item removed")
def delete_cart_item(item_id: int = Path(..., description="Item ID to remove"),
                     quantity: int = Query(1, description="Quantity to remove"),
                     email: str = Query(..., description="User email")):
    """
    Remove an item from the shopping cart.
    """
    cart = get_cart_by_email(email)
    cart.remove_furniture(item_id, quantity)
    return {"message": "Item removed from cart", "cart": cart._cart_items, "total_price": cart._total_price}


@app.get("/cart/view", summary="View shopping cart", response_description="Cart details")
def view_cart(email: str = Query(..., description="User email")):
    """
    Retrieve the contents of the shopping cart along with the total price.
    """
    cart = get_cart_by_email(email)
    return {"cart": cart._cart_items, "total_price": cart._total_price}


# --- Inventory Endpoints ---
@app.put("/inventory/update/{item_id}", summary="Update inventory quantity", response_description="Inventory updated")
def update_inventory(item_id: int = Path(..., description="Item ID to update"),
                     quantity: int = Query(..., description="New quantity")):
    """
    Update the quantity of an item in the inventory.
    """
    if item_id not in global_inventory.items:
        raise HTTPException(status_code=404, detail="Item not found in inventory")
    global_inventory.update_quantity(item_id, quantity)
    return {"message": "Inventory updated", "inventory": global_inventory.items}


@app.delete("/inventory/delete/{item_id}", summary="Delete item from inventory", response_description="Item deleted")
def delete_inventory_item(item_id: int = Path(..., description="Item ID to delete")):
    """
    Remove an item from the inventory.
    """
    if item_id not in global_inventory.items:
        raise HTTPException(status_code=404, detail="Item not found in inventory")
    global_inventory.remove_item(item_id)
    return {"message": "Item removed from inventory", "inventory": global_inventory.items}


# --- Orders Endpoints ---
@app.get("/orders", summary="Get orders for a user", response_description="List of orders")
def get_orders(email: str = Query(..., description="User email")):
    """
    Retrieve all orders placed by a user.
    """
    user = get_user_by_email(email)
    orders = global_user_orders.get_orders_for_user(user)
    return {"orders": [order.__repr__() for order in orders]}


@app.post("/checkout", summary="Checkout and create an order", response_description="Order placed")
def checkout(checkout_data: CheckoutRequest):
    """
    Process checkout:
      - Validates that the cart has items and sufficient stock.
      - Mocks payment processing.
      - Deducts purchased items from inventory.
      - Creates a new order and updates the order history.
      - Clears the user's shopping cart.
    """
    user = get_user_by_email(checkout_data.email)
    cart = get_cart_by_email(checkout_data.email)

    if not cart._cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # Validate inventory availability
    for item_id, qty in cart._cart_items.items():
        if global_inventory.get_quantity(item_id) < qty:
            raise HTTPException(status_code=400, detail=f"Not enough stock for item {item_id}")

    # Process payment (mocked)
    print(f"Processing payment of ${cart._total_price:.2f} using {checkout_data.payment_method}...")
    payment_successful = process_payment(cart._total_price, checkout_data.payment_method)
    if not payment_successful:
        raise HTTPException(status_code=400, detail="Payment failed")

    # Deduct purchased items from inventory
    for item_id, qty in cart._cart_items.items():
        new_qty = global_inventory.get_quantity(item_id) - qty
        global_inventory.update_quantity(item_id, new_qty)

    # Create and store the order
    order = Order(user, list(cart._cart_items.keys()), cart._total_price, status="Completed")
    global_user_orders.update(order)

    # Clear shopping cart (create a new empty cart)
    shopping_carts[checkout_data.email] = ShoppingCart(global_inventory)

    return {"message": "Order placed successfully", "order": order.__repr__()}


def process_payment(amount: float, payment_method: str) -> bool:
    """
    Simulate payment processing. Always returns True for this mock.
    """
    print(f"Payment of ${amount:.2f} processed successfully with {payment_method}.")
    return True
