# 🛋️ Online Furniture Store API & CLI
## A Complete E-Commerce System with FastAPI & CLI Mode

## Group Members: Gal Greenwald, Shir Harouche, Elie Hallermaier, Yonatan Samuel

📌 **This project provides a fully functional RESTful API and an interactive CLI for managing an online furniture store.**  

✅ **Key Features:**  
- **REST API** for inventory, users, shopping carts, orders, and checkout.
- **Interactive CLI mode** for user management and shopping cart operations.
- Uses **object-oriented programming (OOP)** and **design patterns**.
- Supports **FastAPI Swagger UI (`/docs`)** for easy API testing.
- Data persistence managed through in-memory dictionaries (**can be extended with a database**).
- **CI/CD Pipeline** with automated testing, linting, and **80%+ test coverage enforcement**.

---

## 📖 **Table of Contents**
1. [Installation & Setup](#-installation--setup)
2. [Project Usage](#-project-usage)
   - [Run in CLI Mode](#-run-in-cli-mode)
   - [Run in API Mode](#-run-in-api-mode)
3. [API Documentation](#-api-documentation)
    - [Example API Calls](#-example-api-calls)
4. [Class Structure & Explanation](#-class-structure--explanation)
5. [Project Structure](#-project-structure)
6. [Testing & CI/CD](#-testing--cicd)
7. [Future Improvements](#-future-improvements)
8. [Contributing](#-contributing)
9. [License](#-license)

---
## 🚀 **Installation & Setup**

### **Prerequisites**
- Python **3.11+**
- `pip` package manager

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/yourusername/online-furniture-store.git
cd online-furniture-store
```

### 2️⃣ Set Up a Virtual Environment
```sh
python3.11 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```
---

## 🛠️ **Project Usage**
This project supports two modes:

1. CLI Mode: Manage users, shopping cart, and orders manually via terminal input.
2. API Mode: Provides a REST API for handling store operations.

##  🔹Run in CLI Mode
To run in interactive CLI mode, execute:
```sh
python main.py
```

##  🔹Run in API Mode
To launch FastAPI mode, use:
```sh
python main.py api
```
or use `uvicorn`:
```sh
uvicorn main:app --reload
```

---

## 📌 **API Documentation**

## Example API Calls

1. 📍 GET /items - Get All Furniture
🔹 Returns: A list of furniture items with optional filters.
🔹 Parameters:

    | Name       | Type   | Description               |
    |-----------|--------|---------------------------|
    | name      | str    | Search by name.           |
    | category  | str    | Filter by category.       |
    | min_price | float  | Minimum price filter.     |
    | max_price | float  | Maximum price filter.     |


    ✅ Example Request:
    ```sh
    curl -X GET "http://127.0.0.1:8000/items?min_price=100"
    ```
    
    ✅ Example Response:
    ```json
    [
        {"item_id": 1, "title": "Modern Table", "price": 150.0, "description": "A modern table."}
    ]
    ```

2. 📍 POST /users/register - Register a New User
    🔹 Registers a new user in the system.
    🔹 Request Body:

    ```json
    {
        "username": "user123",
        "full_name": "John Doe",
        "email": "user@example.com",
        "password": "securepassword",
        "address": "123 Main St",
        "phone_number": "555-1234"
    }
    ```
    ✅ Example Request:
    ```sh
    curl -X POST "http://127.0.0.1:8000/users/register" -H "Content-Type: application/json" -d '{"username":"user123","full_name":"John Doe","email":"user@example.com","password":"securepassword","address":"123 Main St","phone_number":"555-1234"}'
    ```

3. 📍 POST /cart/items - Add Item to Cart
    🔹 Adds an item to the shopping cart.
    🔹 Request Body:

    ```json
    {
    "item_id": 1,
    "quantity": 2
    }
    ```

    ✅ Example Request:
    ```sh
    curl -X POST "http://127.0.0.1:8000/cart/items" -H "Content-Type: application/json" -d '{"item_id": 1, "quantity": 2}'
    ```

4. 📍 POST /checkout - Checkout
    🔹 Finalizes an order from the shopping cart.
    🔹 Parameters:

    | Name     | Type | Description            |
    |----------|------|------------------------|
    | username | str  | The user checking out. |

    ✅ Example Request:
    ```sh
    curl -X POST "http://127.0.0.1:8000/checkout?username=user123"
    ```
    ---


## 📂 **Class Structure & Explanation**

### 📌 Inventory
Manages the store’s inventory with the following methods:
add_item()
remove_item()
update_quantity()
search_items()

### 📌 StoreItem & Subclasses
Represents different furniture items:
Table
Chair
Bed
Closet
Sofa


### 📌 ShoppingCart
Handles:
Adding/removing items.
Calculating total price.
Applying discounts.

### 📌 User
Handles:
Authentication (password hashing).
User profile management.

### 📌 Order
Manages:
Order creation.
Status tracking.

### 📌 UserOrderDictionary
Maintains a dictionary mapping a user's username to a list of their orders.
Obtaining an Observer Pattern.

---

## 📂 **Project Structure**
```bash
/online-furniture-store
│── Design - Final.pdf  # Design Architechture
│── inventory.py        # Manages inventory
│── store_item.py       # Furniture classes (Table, Chair, etc.)
│── shopping_cart.py    # Handles shopping cart logic
│── user.py             # User authentication & management
│── order.py            # Order processing
│── user_order_dic.py   # Tracks orders per user
│── api.py              # FastAPI implementation
│── main.py             # CLI & API entry point
│── requirements.txt    # Dependencies
│── README.md           # Documentation
│── .github/workflows/  # GitHub Actions CI/CD
    │── ci.yml
└── tests/              # Unit and Integration Tests
    │── test_api.py
    │── test_inventory.py
    │── test_main.py
    │── test_regression.py
    │── test_shopping_cart.py
    │── test_user.py
    │── test_user_order_dic.py
    │── test_orders.py
```
---
## ✅ **Testing & CI/CD**

### Running Tests
```sh
pytest --cov=.
```

### GitHub Actions CI/CD
A CI/CD pipeline automatically runs on each push and PR to main, ensuring:
* ✅ Tests run with 80%+ coverage.
* ✅ Linting passes (black & ruff).
* ✅ No breaking changes are introduced.

---
## 🛠️  **Future Improvements**
🚀 Planned Features:
* Database Integration: Replace in-memory storage with SQLite/MySQL.
* JWT Authentication: Implement secure login with tokens.
* Payment Processing: Integrate with Stripe or PayPal.

---

## 👨‍💻 **Contributing**
Contributions are welcome! Feel free to:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---
## 📜 **License**
This project is MIT Licensed. You are free to modify and distribute it under the terms of the license.

