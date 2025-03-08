from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
import uvicorn

# Import our project classes.
from inventory import Inventory
from store_item import Table, Bed, Closet, Chair, Sofa, StoreItem
from shopping_cart import ShoppingCart
from user import User
from order import Order
from user_order_dic import UserOrderDictionary

app = FastAPI(title="Online Furniture Store API")

# ----------------------
# Global Instances Setup
# ----------------------

# Create an inventory instance.
inventory = Inventory()

# Create a sample catalog of store items.
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

# Populate the inventory with a default quantity (e.g. 10 each).
for item_id in catalog:
    inventory.add_item(item_id, 10)
inventory.set_catalog(catalog) # setting catalog as required in the updated inv

# Create a global shopping cart instance linked to the inventory.
shopping_cart = ShoppingCart(inventory)

# Dictionaries to store users and orders.
user_db: Dict[str, User] = {}  # Stores users by username
orders: List[Order] = []  # List of orders
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

@app.get("/", response_model=Dict[str, str])
def read_root():
    """
    Root endpoint for debugging.

    Returns:
        dict: Welcome message.
    """
    return {"message": "Welcome to the Online Furniture Store API!"}

@app.get("/items", response_model=List[Dict])
def get_items(name: Optional[str] = None, category: Optional[str] = None,
              min_price: Optional[float] = None, max_price: Optional[float] = None):
    """
    Retrieve a list of store items.

    Query Parameters:
        name (str, optional): Search by name.
        category (str, optional): Filter by category.
        min_price (float, optional): Minimum price filter.
        max_price (float, optional): Maximum price filter.

    Returns:
        List[Dict]: List of matching items.
    """
    # Use the Inventory.search_items() to filter available items.
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
    Retrieve item details by ID.

    Path Parameters:
        item_id (int): The ID of the item.

    Returns:
        dict: Item details.

    Raises:
        HTTPException: If item is not found.
    """
    catalog_copy = inventory.get_catalog()
    if item_id not in catalog_copy:
        raise HTTPException(status_code=404, detail="Item not found.")
    
    item = catalog_copy[item_id]
    return {
        "item_id": item.item_id,
        "title": item.title,
        "price": item.price,
        "description": item.get_description()
    }

@app.post("/users/register", response_model=Dict[str, str])
def register_user(user: UserRegister):
    """
    Register a new user.

    Request Body:
        user (UserRegister): User details.

    Returns:
        dict: Registration confirmation.

    Raises:
        HTTPException: If username already exists.
    """
    if user.username in user_db:
        raise HTTPException(status_code=400, detail="Username already exists.")
    
    new_user = User(user.username, user.full_name, user.email, user.password, user.address, user.phone_number)
    user_db[user.username] = new_user
    return {"message": new_user.sign_up()}

@app.post("/users/login", response_model=Dict[str, str])
def login_user(login: UserLogin):
    """
    Log in a user.

    Request Body:
        login (UserLogin): User credentials.

    Returns:
        dict: Login status.

    Raises:
        HTTPException: If email or password is incorrect.
    """
    # Find user by email.
    user = next((u for u in user_db.values() if u.email == login.email), None)
    if user is None or not user.verify_password(login.password):
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    
    result = user.login(login.email, login.password)
    return {"message": result}

@app.put("/users/{username}", response_model=Dict[str, str])
def update_user_profile(username: str, profile: UpdateProfile):
    """
    Update an existing user's profile.

    Path Parameters:
        username (str): The username of the user whose profile is to be updated.
    
    Request Body:
        profile (UpdateProfile): The updated user profile details.
            - full_name (Optional[str]): Updated full name.
            - address (Optional[str]): Updated address.
            - phone_number (Optional[str]): Updated phone number.

    Returns:
        dict: A message confirming profile update.

    Raises:
        HTTPException: if the user is not found.
    """
    if username not in user_db:
        raise HTTPException(status_code=404, detail="User not found.")
    
    user = user_db[username]
    result = user.manage_profile(profile.full_name, profile.address, profile.phone_number)
    return {"message": result}

@app.get("/users/{username}", response_model=Dict[str, str])
def get_user_profile(username: str):
    """
    Retrieve a user's profile information.

    Path Parameters:
        username (str): The username of the user whose profile is being requested.

    Returns:
        dict: A dictionary containing the user's profile information.
            - username (str): The user's username.
            - full_name (str): The user's full name.
            - email (str): The user's email address.

    Raises:
        HTTPException: if the user is not found.
    """
    if username not in user_db:
        raise HTTPException(status_code=404, detail="User not found.")
    
    user = user_db[username]

    return {
        "username": user.username,
        "full_name": user.full_name,
        "email": user.email
    }

@app.get("/orders", response_model=List[Dict])
def get_all_orders():
    """
    Retrieve all orders.

    Returns:
        List[Dict]: A list of dictionaries, each containing order details:
            - user (str): The username of the customer who placed the order.
            - total_price (float): The total price of the order.
            - status (str): The current status of the order (e.g., "pending", "shipped").
            - items (List[Tuple[StoreItem, int]]): List of purchased items and their quantities.
    """
    orders_list = []
    for order in orders:
        orders_list.append({
            "user": order.user.username,
            "total_price": order.total_price,
            "status": order.status,
            "items": order.items
        })
    return orders_list

@app.post("/orders", response_model=Dict[str, str])
def create_order(order_data: OrderCreate):
    """
    Create a new order for a user.

     Request Body:
        order_data (OrderCreate): A dictionary containing:
            - username (str): The username of the user placing the order.
            - items (List[OrderItem]): A list of item IDs and their quantities.

    Returns:
        Dict[str, str]: A confirmation message and order details.

    Raises:
        HTTPException:
            - 404 if the user is not found.
            - 404 if an item in the order is not found in inventory.
            - 400 if there is insufficient stock for any item.
    """
    if order_data.username not in user_db:
        raise HTTPException(status_code=404, detail="User not found.")
    
    user = user_db[order_data.username]
    order_items = []
    total_price = 0.0
    catalog_copy = inventory.get_catalog()

    # Process each order item.
    for item in order_data.items:
        if item.item_id not in catalog_copy:
            raise HTTPException(status_code=404, detail=f"Item {item.item_id} not found.")
        
        available_qty = inventory.get_quantity(item.item_id)
        if available_qty < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for item {item.item_id}.")

        order_items.append((catalog_copy[item.item_id], item.quantity))
        total_price += catalog_copy[item.item_id].price * item.quantity

        # Update inventory: reduce the quantity.
        inventory.update_quantity(item.item_id, available_qty - item.quantity)

    new_order = Order(user, order_items, total_price)
    orders.append(new_order)
    user_order_dict.update(new_order)

    return {"message": "Order created successfully.", "order": repr(new_order)}

@app.post("/cart/items", response_model=Dict[str, str])
def add_item_to_cart(cart_item: CartItem):
    """
    Add an item to the shopping cart.

    Request Body:
        cart_item (CartItem): A dictionary containing:
            - item_id (int): The ID of the item to be added.
            - quantity (int): The number of units to add to the cart.

    Returns:
        Dict[str, str]: A confirmation message with the updated cart.

    Raises:
        HTTPException:
            - 404 if the item is not found in the catalog.
    """
    catalog_copy = inventory.get_catalog()

    if cart_item.item_id not in catalog_copy:
        raise HTTPException(status_code=404, detail="Item not found in catalog.")
    
    shopping_cart.add_furniture(cart_item.item_id, cart_item.quantity)
    return {"message": "Item added to cart.", "cart": repr(shopping_cart)}

@app.delete("/cart/items/{item_id}", response_model=Dict[str, str])
def remove_item_from_cart(item_id: int, quantity: int = 1):
    """
    Remove an item from the shopping cart.

    Path Parameters:
        item_id (int): The ID of the item to be removed from the cart.

    Query Parameters:
        quantity (int, optional): The number of units to remove (default is 1).

    Returns:
        Dict[str, str]: A confirmation message with the updated cart.

    Raises:
        HTTPException:
            - 404 if the item is not found in the catalog.
    """
    catalog_copy = inventory.get_catalog()

    if item_id not in catalog_copy:
        raise HTTPException(status_code=404, detail="Item not found in catalog.")
    
    shopping_cart.remove_furniture(item_id, quantity)

    return {"message": "Item removed from cart.", "cart": repr(shopping_cart)}

@app.put("/inventory/{item_id}", response_model=Dict[str, str])
def update_inventory_item(item_id: int, inv_update: InventoryUpdate):
    """
    Update the quantity of an inventory item.

    Path Parameters:
        item_id (int): The ID of the item whose quantity is to be updated.

    Request Body:
        inv_update (InventoryUpdate): A dictionary containing:
            - quantity (int): The new quantity to be set for the item.

    Returns:
        Dict[str, str]: A confirmation message with the updated inventory.

    Raises:
        HTTPException:
            - 404 if the item is not found in inventory.
    """
    if item_id not in inventory.items:
        raise HTTPException(status_code=404, detail="Item not found in inventory.")
    
    inventory.update_quantity(item_id, inv_update.quantity)
    return {"message": "Inventory updated.", "inventory": inventory.items}

@app.delete("/inventory/{item_id}", response_model=Dict[str, str])
def remove_inventory_item(item_id: int):
    """
    Remove an item from the inventory.

    Path Parameters:
        item_id (int): The ID of the item to be removed from inventory.

    Returns:
        Dict[str, str]: A confirmation message with the updated inventory.

    Raises:
        HTTPException:
            - 404 if the item is not found in inventory.
    """
    if item_id not in inventory.items:
        raise HTTPException(status_code=404, detail="Item not found in inventory.")
    
    inventory.remove_item(item_id)
    return {"message": "Item removed from inventory.", "inventory": inventory.items}

@app.post("/cart/apply_discount", response_model=Dict[str, str])
def apply_cart_discount(discount: Discount):
    """
    Apply a discount percentage to the shopping cart's total price.

    Request Body:
        discount (Discount): A dictionary containing:
            - discount_percentage (float): The percentage of discount to be applied (0-100).
    
    Returns:
        Dict[str, str]: A confirmation message with the updated cart total.
    """
    shopping_cart.apply_discount(discount.discount_percentage)
    return {"message": "Discount applied.", "cart": repr(shopping_cart)}

@app.post("/checkout", response_model=Dict[str, str])
def checkout(username: str):
    """
    Process checkout: creates an order from the shopping cart,
    updates the inventory, and clears the shopping cart.

    Query Parameters:
        username (str): The username of the user completing the checkout.

    Returns:
        Dict[str, str]: A confirmation message with the order details.

    Raises:
        HTTPException:
            - 404 if the user is not found.
            - 400 if the shopping cart is empty.
            - 400 if stock is insufficient for any item in the cart.
    """
    if username not in user_db:
        raise HTTPException(status_code=404, detail="User not found.")
    
    user = user_db[username]
    if not shopping_cart._cart_items:
        raise HTTPException(status_code=400, detail="Shopping cart is empty.")
    
    catalog_copy = inventory.get_catalog()
    order_items = []
    total_price = shopping_cart._total_price
    for item_id, quantity in shopping_cart._cart_items.items():
        order_items.append((catalog_copy[item_id], quantity))
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
# How to Run the API
# ---------------------------
# 1. Install dependencies:
#    pip install fastapi uvicorn bcrypt
#
# 2. Run the API with:
#    uvicorn main:app --reload
#
# The --reload flag is useful during development as it auto-restarts the server
# whenever you make changes to the code.



# ---------------------------
# Running the API
# ---------------------------

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)