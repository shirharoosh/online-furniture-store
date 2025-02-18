Online Furniture Store
Overview
The Online Furniture Store project is a full-stack simulation of an e-commerce platform for furniture. The project demonstrates advanced object-oriented design, effective inventory management, secure user authentication, a dynamic shopping cart system, and a complete checkout process. A RESTful API powered by FastAPI exposes the application's functionality to clients.

Features
Domain Model
Implements a rich set of classes to represent various furniture items (e.g., Table, Chair, Sofa, Bed, Closet).

Each furniture item includes attributes such as title, price, dimensions, weight, and description.
Methods support discount calculations and other business logic.
Inventory Management
Manages stock levels using an Inventory class which supports adding, updating, removing items, and searching by various attributes.

User Management & Authentication
A secure User class handles registration, login, profile management, and password hashing with bcrypt.

Users can view their order history.
Shopping Cart
The ShoppingCart class allows users to add or remove items, view total pricing, and apply discounts.

It interfaces with the inventory for stock verification without modifying stock until checkout.
Checkout & Order Management
A comprehensive checkout process validates cart contents, mocks payment processing, and updates both inventory and order history.

The Order class encapsulates the details of each purchase.
The Observer pattern (via UserOrderDictionary) is used to update user order histories automatically.
RESTful API
FastAPI powers the API which exposes endpoints for:

User registration, login, profile management
Viewing and managing shopping carts and inventory
Retrieving product information and order history
Processing checkouts and orders
Architecture & Design
The project is organized into several modules:

Domain Models:

store_item.py: Abstract class StoreItem and concrete furniture classes.
inventory.py: Manages item stock levels.
shopping_cart.py: Manages cart operations.
order.py: Represents an order.
user.py: Handles user information and authentication.
user_order_dic.py: Implements the Observer pattern to manage user orders.
API Module:

api.py: Contains FastAPI endpoints that integrate the domain models with HTTP methods.
Design Patterns Employed:

Observer Pattern: Used in UserOrderDictionary to update a user's order history automatically.
Composite Pattern (conceptual): The shopping cart can manage multiple item types.
Factory/Abstraction: The use of an abstract StoreItem class to define common behavior across different furniture types.
Setup & Installation
Prerequisites
Python 3.8 or above
pip
Virtual environment (recommended)
Installation Steps
Clone the Repository:

bash
Copy
Edit
git clone https://github.com/your-username/online-furniture-store.git
cd online-furniture-store
Create a Virtual Environment and Activate It:

bash
Copy
Edit
python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
Install Dependencies:

bash
Copy
Edit
pip install -r requirements.txt
(Ensure that the requirements.txt includes FastAPI, uvicorn, bcrypt, and any other necessary packages.)

Run the Application:

bash
Copy
Edit
uvicorn api:app --reload
The API will be accessible at http://127.0.0.1:8000.

API Documentation
FastAPI automatically generates interactive documentation. Once the server is running, you can access:

Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc
Key Endpoints
User Management

POST /signup – Register a new user.
POST /login – Authenticate and log in a user.
GET /users/{email} – Retrieve a user profile.
PUT /users/{email} – Update user profile information.
Furniture Items

GET /items – Get all furniture items with available quantities.
Shopping Cart

POST /cart/add – Add an item to the shopping cart.
PUT /cart/update – Update item quantities in the shopping cart.
DELETE /cart/delete/{item_id} – Remove an item from the shopping cart.
GET /cart/view – View current cart contents and total price.
Inventory Management

PUT /inventory/update/{item_id} – Update inventory for a specific item.
DELETE /inventory/delete/{item_id} – Remove an item from the inventory.
Orders & Checkout

GET /orders – Retrieve orders for a user.
POST /checkout – Process checkout and create an order.
Testing
Unit & Integration Tests:
The project includes comprehensive tests to cover business logic and API endpoints.
Code Coverage:
Aim for at least 80% test coverage.
Continuous Integration:
CI workflows (using GitHub Actions) run tests and lint checks on each pull request.
CI/CD & Collaboration
Version Control:
The project uses Git with feature branches, pull requests, and code reviews for collaboration.
GitHub Actions:
Automated workflows for testing, linting (using tools such as Black, flake8), and coverage reporting are configured to ensure code quality.
Future Enhancements
Extend support for additional furniture types and accessories.
Integrate real payment processing with external APIs.
Implement a front-end UI using a modern framework (e.g., React or Angular).
Enhance security with JWT-based authentication.
Incorporate more detailed logging and error monitoring.
Conclusion
The Online Furniture Store project demonstrates the application of advanced programming techniques, clean code practices, and modern API design principles. This project is designed to be both a robust backend system and a foundation for further enhancements and integrations.

Team Members
Yonatan
Shir
Elie
Gal












# Online Furniture Store - Detailed Documentation

## Overview
The **Online Furniture Store** is a fully functional backend system designed to manage an inventory of furniture items, user accounts, shopping carts, and orders. This documentation provides an in-depth explanation of each class, their purpose, interactions, and how they function together within the system.

## Class Descriptions and Interactions

### 1. **StoreItem (Abstract Class)**
- **Purpose:** Represents a generic furniture item with common attributes.
- **Attributes:**
  - `item_id` (int) - Unique identifier for the item.
  - `title` (str) - Name of the furniture piece.
  - `price` (float) - Cost of the item.
  - `height`, `width` (int) - Dimensions of the item.
  - `weight` (float) - Weight of the item.
  - `description` (str) - Text description of the item.
- **Methods:**
  - `apply_discount(discount: float) -> float`: Returns the discounted price.
  - `__repr__()`: Returns a string representation of the object.
- **Usage:**
  - This is an abstract class that is inherited by specific furniture items.

### 2. **Concrete Furniture Classes**
Each furniture type extends `StoreItem` and may have additional attributes:
- `Table` - Inherits directly from `StoreItem`.
- `Chair` - Includes `material` (e.g., Leather, Wood, Plastic).
- `Sofa` - Includes `seating_capacity`.
- `Bed` - Includes `pillow_count`.
- `Closet` - Includes `with_mirror` (boolean).

### 3. **Inventory Class**
- **Purpose:** Manages the store’s stock of items.
- **Attributes:**
  - `_items` (Dict[int, int]) - Maps `item_id` to available `quantity`.
- **Methods:**
  - `add_item(item_id: int, quantity: int)`: Adds stock to an item.
  - `remove_item(item_id: int)`: Removes an item from the inventory.
  - `update_quantity(item_id: int, quantity: int)`: Sets a new quantity for an item.
  - `get_quantity(item_id: int) -> int`: Retrieves stock level of an item.
  - `search_items(...)`: Finds items based on filters.
- **Usage:**
  - Central storage system that interacts with `ShoppingCart`, `Order`, and the API.

### 4. **ShoppingCart Class**
- **Purpose:** Manages a user's shopping cart before checkout.
- **Attributes:**
  - `_cart_items` (Dict[int, int]) - Maps `item_id` to quantity.
  - `_total_price` (float) - Tracks total cost of the cart.
- **Methods:**
  - `add_furniture(catalog, item_id: int, quantity: int)`: Adds an item if stock is available.
  - `remove_furniture(catalog, item_id: int, quantity: int)`: Removes an item from the cart.
  - `apply_discount(discount_percentage: float)`: Applies a percentage discount.
- **Usage:**
  - Before checkout, users add/remove items via the cart. Stock levels are only checked, not updated.

### 5. **Order Class**
- **Purpose:** Represents a completed purchase by a user.
- **Attributes:**
  - `_user` (User) - The customer making the order.
  - `_items` (List[int]) - A list of item IDs in the order.
  - `_total_price` (float) - Final cost of the order.
  - `_status` (str) - Order status (Pending, Shipped, Delivered).
- **Methods:**
  - `update_status(new_status: str)`: Changes order status.
- **Usage:**
  - Created when a user completes checkout. Also updates the user’s order history.

### 6. **User Class**
- **Purpose:** Represents a store customer with authentication.
- **Attributes:**
  - `_username`, `_email`, `_password_hash`, `_address`, `_phone_number`
  - `_is_logged` (bool) - Tracks login status.
  - `_order_hist` (List[Order]) - Stores past orders.
- **Methods:**
  - `sign_up()`: Registers the user.
  - `login(email: str, password: str)`: Authenticates the user.
  - `manage_profile(...)`: Allows updates to user info.
  - `view_order_history()`: Retrieves past purchases.
  - `add_order(order: Order)`: Adds an order to history.
- **Usage:**
  - Essential for authentication, order tracking, and profile management.

### 7. **UserOrderDictionary (Observer Pattern)**
- **Purpose:** Manages mapping of users to their orders.
- **Attributes:**
  - `_user_orders` (Dict[str, List[Order]]) - Maps usernames to their orders.
- **Methods:**
  - `update(order: Order)`: Automatically adds a new order to the user's history.
  - `get_orders_for_user(user: User) -> List[Order]`: Retrieves a user’s orders.
- **Usage:**
  - Ensures each order is automatically added to the user’s history upon checkout.

## How These Classes Work Together
1. **User Interaction:**
   - A user signs up and logs in via the API (`User` class).
   - The user receives an empty `ShoppingCart`.

2. **Shopping Process:**
   - The user adds items to the cart (`ShoppingCart`).
   - The cart checks inventory availability (`Inventory`).
   - The user applies discounts if needed.

3. **Checkout & Order Processing:**
   - The user proceeds to checkout, which:
     - Validates stock.
     - Mocks payment processing.
     - Deducts items from `Inventory`.
     - Creates an `Order` and updates `UserOrderDictionary`.
     - Clears the `ShoppingCart`.

4. **Order Tracking:**
   - Users retrieve their past orders (`UserOrderDictionary`).
   - The `Order` status updates as it progresses (Pending → Shipped → Delivered).

## API Integration
- The **FastAPI API** (`api.py`) interacts with these classes to provide RESTful endpoints.
- Users send HTTP requests to manage carts, check inventory, process orders, and handle authentication.
- The API ensures proper validation and security using FastAPI’s request validation features.

## Summary
This system provides:
1. A modular, object-oriented structure.
2. Secure user authentication.
3. A dynamic inventory and shopping cart system.
4. A complete order management flow.
5. RESTful API endpoints for easy interaction.

This documentation should help developers understand how the classes interact and how they contribute to the overall architecture of the Online Furniture Store.


