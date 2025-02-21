# 🛋️ Online Furniture Store API & CLI
## A Complete E-Commerce System with FastAPI & CLI Mode

📌 **This project provides a fully functional RESTful API and an interactive CLI for managing an online furniture store.**  

✅ **Key Features:**  
- **REST API** for inventory, users, shopping carts, orders, and checkout.
- **Interactive CLI mode** for user management and shopping cart operations.
- Uses **object-oriented programming (OOP)** and **design patterns**.
- Supports **FastAPI Swagger UI (`/docs`)** for easy API testing.
- Data persistence managed through in-memory dictionaries (**can be extended with a database**).

---

## 📖 **Table of Contents**
1. [Installation & Setup](#-installation--setup)
2. [Usage](#-usage)
   - [Run in CLI Mode](#-run-in-cli-mode)
   - [Run in API Mode](#-run-in-api-mode)
3. [API Documentation](#-api-documentation)
4. [Class Structure & Explanation](#-class-structure--explanation)
5. [Project Structure](#-project-structure)
6. [Future Improvements](#-future-improvements)
7. [Contributing](#-contributing)
8. [License](#-license)

---

## 🚀 **Installation & Setup**
### **Prerequisites**
- Python **3.11+**
- `pip` package manager

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/yourusername/online-furniture-store.git
cd online-furniture-store




2️⃣ Set Up a Virtual Environment
python3.11 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt


🛠️ Usage
This project supports two modes:

CLI Mode: Manage users, shopping cart, and orders manually via terminal input.
API Mode: Provides a REST API for handling store operations.

 Run in CLI Mode
To run in interactive CLI mode, execute:
python main.py


🔹 Run in API Mode
To launch FastAPI mode, use:
python main.py api
or
uvicorn main:app --reload















📌 API Documentation
📍 GET /items - Get All Furniture
🔹 Returns: A list of furniture items with optional filters.
🔹 Parameters:

Name	Type	Description
name	str	Search by name.
category	str	Filter by category.
min_price	float	Minimum price filter.
max_price	float	Maximum price filter.
✅ Example Request:

sh
Copy
Edit
curl -X GET "http://127.0.0.1:8000/items?min_price=100"
✅ Response:

json
Copy
Edit
[
    {"item_id": 1, "title": "Modern Table", "price": 150.0, "description": "A modern table."}
]
📍 POST /users/register - Register a New User
🔹 Registers a new user in the system.

Request Body:

json
Copy
Edit
{
    "username": "user123",
    "full_name": "John Doe",
    "email": "user@example.com",
    "password": "securepassword",
    "address": "123 Main St",
    "phone_number": "555-1234"
}
✅ Example Request:

sh
Copy
Edit
curl -X POST "http://127.0.0.1:8000/users/register" -H "Content-Type: application/json" -d '{"username":"user123","full_name":"John Doe","email":"user@example.com","password":"securepassword","address":"123 Main St","phone_number":"555-1234"}'
📂 Class Structure & Explanation
📌 Inventory
Manages the store’s inventory:

add_item()
remove_item()
update_quantity()
search_items()
📌 StoreItem & Subclasses
Represents different furniture items:

Table
Chair
Bed
Closet
Sofa
📌 ShoppingCart
Handles:

Adding/removing items.
Calculating total price.
Applying discounts.
📌 User
Handles:

Authentication (password hashing).
User profile management.
📌 Order
Manages:

Order creation.
Status tracking.
📂 Project Structure
bash
Copy
Edit
/online-furniture-store
│── /inventory.py        # Manages inventory
│── /store_item.py       # Furniture classes (Table, Chair, etc.)
│── /shopping_cart.py    # Handles shopping cart logic
│── /user.py             # User authentication & management
│── /order.py            # Order processing
│── /user_order_dic.py   # Tracks orders per user
│── main.py              # CLI & API entry point
│── requirements.txt     # Dependencies
│── README.md            # Documentation
🛠️ Future Improvements
🚀 Planned Features:

Database Integration: Replace in-memory storage with SQLite/MySQL.
Authentication System: Implement JWT-based user authentication.
Payment Processing: Integrate with Stripe or PayPal.
👨‍💻 Contributing
Contributions are welcome! Feel free to:

Fork the repository
Create a feature branch
Submit a pull request
📜 License
This project is MIT Licensed. You are free to modify and distribute it under the terms of the license.


