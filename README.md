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
