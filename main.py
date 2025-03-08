import sys
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict

# Import our project modules.
from inventory import Inventory
from store_item import Table, Bed, Closet, Chair, Sofa, StoreItem
from shopping_cart import ShoppingCart
from user import User
from order import Order
from user_order_dic import UserOrderDictionary

# ----------------------
# FastAPI App Setup
# ----------------------
app = FastAPI(title="Online Furniture Store API")

# Global shared resources (Simulated database)
inventory = Inventory()  # Shared inventory across users
shopping_cart = ShoppingCart(inventory)
user_db: Dict[str, User] = {}  # username -> User
orders: List[Order] = []  # List of orders
user_order_dict = UserOrderDictionary()

# Additional storage:
user_accounts: Dict[str, User] = {}  # email -> User
shopping_carts: Dict[str, ShoppingCart] = {}  # email -> ShoppingCart

# Sample catalog of store items.
catalog: Dict[int, StoreItem] = {
    1: Table(item_id=1, title="Modern Table", price=150.00, height=30, width=50, weight=20.0, description="A modern table."),
    2: Bed(item_id=2, title="Queen Bed", price=300.00, height=40, width=60, weight=50.0,
           description="A comfortable queen bed.", pillow_count=2),
    3: Closet(item_id=3, title="Spacious Closet", price=250.00, height=80, width=100, weight=100.0,
              description="A spacious closet.", with_mirror=True),
    4: Chair(item_id=4, title="Office Chair", price=85.00, height=45, width=45, weight=15.0,
             description="Ergonomic office chair.", material="leather"),
    5: Sofa(item_id=5, title="Family Sofa", price=400.00, height=35, width=80, weight=70.0,
            description="Comfortable family sofa.", seating_capacity=4)
}

# Populate the inventory with a default quantity (e.g., 10 each)
for item_id in catalog:
    inventory.add_item(item_id, 10)

# Global shopping cart instance linked to the inventory.
shopping_cart = ShoppingCart(inventory)

# Dictionaries to store users and orders.
user_db: Dict[str, User] = {}  # username -> User
orders: List[Order] = []         # List of orders
user_order_dict = UserOrderDictionary()


# --------------------------
# Pydantic Models for Routes
# --------------------------
class UserRegister(BaseModel):
    """Request model for user registration."""
    username: str
    full_name: str
    email: str
    password: str
    address: str
    phone_number: str

class UserLogin(BaseModel):
    """Request model for user login."""
    email: str
    password: str

class UpdateProfile(BaseModel):
    """Request model for updating user profile."""
    full_name: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None

class CartItem(BaseModel):
    """Request model for adding/removing items from the cart."""
    item_id: int
    quantity: int

class InventoryUpdate(BaseModel):
    """Request model for updating inventory quantity."""
    quantity: int

class OrderItem(BaseModel):
    """Request model for an item in an order."""
    item_id: int
    quantity: int

class OrderCreate(BaseModel):
    """Request model for creating a new order."""
    username: str
    items: List[OrderItem]

class Discount(BaseModel):
    """Request model for applying a discount to the shopping cart."""
    discount_percentage: float

# ---------------------------
# API Endpoints (Routes)
# ---------------------------

@app.get("/")
def read_root():
    """Root endpoint for debugging."""

    return {"message": "Welcome to the Online Furniture Store API!"}

@app.get("/items", response_model=List[Dict])
def get_items(name: Optional[str] = None, category: Optional[str] = None,
              min_price: Optional[float] = None, max_price: Optional[float] = None):
    """
    Retrieve a list of store items (with optional filters).

    Query Parameters:
        name (str, optional): Filter by item name.
        category (str, optional): Filter by category.
        min_price (float, optional): Minimum price filter.
        max_price (float, optional): Maximum price filter.

    Returns:
        List[Dict]: A list of matching store items.    
    """
    matching_items = inventory.search_items(name, category, min_price, max_price)
    items_list = []
    for item in matching_items:
        items_list.append({
            "item_id": item.item_id,
            "title": item.title,
            "price": item.price,
            "description": item.get_description()
        })
    return items_list

@app.get("/items/{item_id}", response_model=Dict)
def get_item(item_id: int):
    """
    Retrieve details of a single item by its item_id.

    Path Parameters:
        item_id (int): The unique ID of the item.

    Returns:
        Dict: Item details.

    Raises:
        HTTPException: If the item is not found.
    """
    if item_id not in catalog:
        raise HTTPException(status_code=404, detail="Item not found.")
    item = catalog[item_id]
    return {
        "item_id": item.item_id,
        "title": item.title,
        "price": item.price,
        "description": item.get_description()
    }

@app.post("/users/register")
def register_user(user: UserRegister):
    """Register a new user."""
    if user.username in user_db:
        raise HTTPException(status_code=400, detail="Username already exists.")
    new_user = User(user.username, user.full_name, user.email, user.password, user.address, user.phone_number)
    user_db[user.username] = new_user
    return {"message": new_user.sign_up()}

@app.post("/users/login")
def login_user(login: UserLogin):
    """Log in a user."""
    user = next((u for u in user_db.values() if u.email == login.email), None)
    if user is None or not user.verify_password(login.password):
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    result = user.login(login.email, login.password)
    return {"message": result}

@app.put("/users/{username}")
def update_user_profile(username: str, profile: UpdateProfile):
    """Update an existing user's profile."""
    if username not in user_db:
        raise HTTPException(status_code=404, detail="User not found.")
    user = user_db[username]
    result = user.manage_profile(profile.full_name, profile.address, profile.phone_number)
    return {"message": result}

@app.get("/users/{username}")
def get_user_profile(username: str):
    """Retrieve a user's profile information."""
    if username not in user_db:
        raise HTTPException(status_code=404, detail="User not found.")
    user = user_db[username]
    return {
        "username": user.username,
        "full_name": user.full_name,
        "email": user.email
    }

@app.get("/orders")
def get_all_orders():
    """Retrieve all orders."""
    orders_list = []
    for order in orders:
        orders_list.append({
            "user": order.user.username,
            "total_price": order.total_price,
            "status": order.status,
            "items": order.items
        })
    return orders_list

@app.post("/orders")
def create_order(order_data: OrderCreate):
    """Create a new order for a user."""
    if order_data.username not in user_db:
        raise HTTPException(status_code=404, detail="User not found.")
    user = user_db[order_data.username]
    order_items = []
    total_price = 0.0
    for item in order_data.items:
        if item.item_id not in catalog:
            raise HTTPException(status_code=404, detail=f"Item {item.item_id} not found.")
        available_qty = inventory.get_quantity(item.item_id)
        if available_qty < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for item {item.item_id}.")
        order_items.append((catalog[item.item_id], item.quantity))
        total_price += catalog[item.item_id].price * item.quantity
        inventory.update_quantity(item.item_id, available_qty - item.quantity)
    new_order = Order(user, order_items, total_price)
    orders.append(new_order)
    user_order_dict.update(new_order)
    return {"message": "Order created successfully.", "order": repr(new_order)}

@app.post("/cart/items")
def add_item_to_cart(cart_item: CartItem):
    """Add an item to the shopping cart."""
    if cart_item.item_id not in catalog:
        raise HTTPException(status_code=404, detail="Item not found in catalog.")
    shopping_cart.add_furniture(cart_item.item_id, cart_item.quantity)
    return {"message": "Item added to cart.", "cart": repr(shopping_cart)}

@app.delete("/cart/items/{item_id}")
def remove_item_from_cart(item_id: int, quantity: int = 1):
    """Remove an item from the shopping cart."""
    if item_id not in catalog:
        raise HTTPException(status_code=404, detail="Item not found in catalog.")
    shopping_cart.remove_furniture(item_id, quantity)
    return {"message": "Item removed from cart.", "cart": repr(shopping_cart)}

@app.put("/inventory/{item_id}")
def update_inventory_item(item_id: int, inv_update: InventoryUpdate):
    """Update the quantity of an inventory item."""
    if item_id not in inventory.items:
        raise HTTPException(status_code=404, detail="Item not found in inventory.")
    inventory.update_quantity(item_id, inv_update.quantity)
    return {"message": "Inventory updated.", "inventory": inventory.items}

@app.delete("/inventory/{item_id}")
def remove_inventory_item(item_id: int):
    """Remove an item from the inventory."""
    if item_id not in inventory.items:
        raise HTTPException(status_code=404, detail="Item not found in inventory.")
    inventory.remove_item(item_id)
    return {"message": "Item removed from inventory.", "inventory": inventory.items}

@app.post("/cart/apply_discount")
def apply_cart_discount(discount: Discount):
    """Apply a discount to the shopping cart's total price."""
    shopping_cart.apply_discount(discount.discount_percentage)
    return {"message": "Discount applied.", "cart": repr(shopping_cart)}

@app.post("/checkout")
def checkout_api(username: str):
    """Process checkout: create an order from the shopping cart, update inventory, and clear the cart."""
    if username not in user_db:
        raise HTTPException(status_code=404, detail="User not found.")
    user = user_db[username]
    if not shopping_cart._cart_items:
        raise HTTPException(status_code=400, detail="Shopping cart is empty.")

    order_items = []
    total_price = shopping_cart._total_price
    for item_id, quantity in shopping_cart._cart_items.items():
        order_items.append((catalog[item_id], quantity))
        available_qty = inventory.get_quantity(item_id)
        if available_qty < quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for item {item_id} during checkout.")
        inventory.update_quantity(item_id, available_qty - quantity)
    new_order = Order(user, order_items, total_price)
    orders.append(new_order)
    user_order_dict.update(new_order)
    # Clear the shopping cart.
    shopping_cart._cart_items.clear()
    shopping_cart._total_price = 0.0
    return {"message": "Checkout successful.", "order": repr(new_order)}


# ---------------------------
# CLI INTERFACE (Interactive Mode)
# ---------------------------
def initialize_inventory(catalog):
    """Populates the inventory using predefined catalog items."""
    for item_id in catalog:
        quantity = 10
        inventory.add_item(item_id, quantity)
    inventory.set_catalog(catalog)
    print("Inventory initialized:")
    print(inventory)

def initialize_users():
    global user_accounts, shopping_carts  # Ensure these are global variables

    """Create pre-generated users."""
    pre_generated_users = [
        ("alice@example.com", "Alice123", "Alice", "Alice Wonderland", "456 Elm St", "123456789"),
        ("bob@example.com", "Bob456", "Bob", "Bob Builder", "789 Oak St", "987654321"),
        ("charlie@example.com", "Charlie789", "Charlie", "Charlie Brown", "321 Pine St", "555555555"),
        ("f", "f", "David", "David Davis", "101112 Elm St", "098765432"),
    ]
    for email, password, username, full_name, address, phone_number in pre_generated_users:
        new_user = User(username, full_name, email, password, address, phone_number)
        user_accounts[email] = new_user
        shopping_carts[email] = ShoppingCart(inventory)

def sign_up():
    """Allow a new user to sign up via CLI."""
    print("\nSign Up")
    email = input("Enter email: ").strip()
    if email in user_accounts:
        print("Error: Email already exists. Try logging in.")
        return None
    username = input("Enter username: ").strip()
    full_name = input("Enter full name: ").strip()
    password = input("Enter password: ").strip()
    address = input("Enter address: ").strip()
    phone_number = input("Enter phone number: ").strip()
    new_user = User(username, full_name, email, password, address, phone_number)
    user_accounts[email] = new_user
    shopping_carts[email] = ShoppingCart(inventory)
    print(f"User {username} registered successfully! You can now log in.")
    return new_user

def log_in():
    """Handle user login via CLI."""
    print("\nLog In")
    email = input("Enter email: ").strip()
    if email not in user_accounts:
        print("User not found. Please sign up first.")
        return None
    password = input("Enter password: ").strip()
    user = user_accounts[email]
    login_result = user.login(email, password)
    if "logged in successfully" in login_result:
        print(login_result)
        return user
    else:
        print(login_result)
        return None

def user_interface(user):
    """Provide a CLI shopping cart menu for the logged-in user."""
    cart = shopping_carts[user.email]
    while True:
        print("\nShopping Cart Menu:")
        print("1. Add Item to Cart")
        print("2. Remove Item from Cart")
        print("3. View Cart")
        print("4. Show Total Price")
        print("5. Checkout")
        print("6. Log Out")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            try:
                item_id = int(input("Enter item ID: ").strip())
                quantity = int(input("Enter quantity: ").strip())
            except ValueError:
                print("Invalid input. Please enter numeric values.")
                continue
            if item_id not in catalog:
                print("Error: Invalid item ID.")
                continue

            cart.add_furniture(item_id, quantity)

        elif choice == "2":
            try:
                item_id = int(input("Enter item ID: ").strip())
                quantity = int(input("Enter quantity: ").strip())
            except ValueError:
                print("Invalid input. Please enter numeric values.")
                continue
            cart.remove_furniture(item_id, quantity)
        elif choice == "3":
            print("Current Cart:", cart)
        elif choice == "4":
            cart.show_total_price()
        elif choice == "5":
            checkout_cli(user, cart)
        elif choice == "6":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def checkout_cli(user, cart):
    """Handle the checkout process via CLI."""
    print("\n--- Checkout Process ---")
    if not cart._cart_items:
        print("Your cart is empty. Add items before checking out.")
        return
    shipping_address = input("Enter shipping address (leave blank to use default): ").strip() or user.address
    payment_method = input("Enter payment method (Credit Card, PayPal): ").strip()
    for item_id, quantity in cart._cart_items.items():
        if inventory.get_quantity(item_id) < quantity:
            print(f"Error: Not enough stock for item {item_id}. Remove items before proceeding.")
            return
    print(f"Processing payment of ${cart._total_price:.2f} using {payment_method}...")
    print(f"Payment of ${cart._total_price:.2f} processed successfully.")
    for item_id, quantity in cart._cart_items.items():
        inventory.update_quantity(item_id, inventory.get_quantity(item_id) - quantity)
    order = Order(user, list(cart._cart_items.keys()), cart._total_price, status="Pending")
    user_order_dict.update(order)
    shopping_carts[user.email] = ShoppingCart(inventory)
    print(f"\nOrder placed successfully for {user.username}!\nOrder Details: {order}")
    print("Thank you for shopping with us!\n")

def main():
    """CLI main function to initialize the application and start interactive mode."""
    initialize_inventory(catalog)
    initialize_users()
    while True:
        print("\nWelcome to the Online Furniture Store!")
        print("1. Log In")
        print("2. Sign Up")
        print("3. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            user = log_in()
            if user:
                user_interface(user)
        elif choice == "2":
            user = sign_up()
            if user:
                user_interface(user)
        elif choice == "3":
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


# ---------------------------
# Execution: API vs. CLI Mode
# ---------------------------
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        print("Starting FastAPI Server...")
        uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    else:
        main()
