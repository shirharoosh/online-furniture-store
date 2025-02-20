import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

# ------------------------------
# User Management Tests
# ------------------------------

def test_signup():
    response = client.post("/signup", json={
        "username": "testuser",
        "full_name": "Test User",
        "email": "test@example.com",
        "password": "testpass",
        "address": "123 Test St",
        "phone_number": "1234567890"
    })
    assert response.status_code == 200
    assert "message" in response.json()

def test_signup_existing_user():
    client.post("/signup", json={
        "username": "existinguser",
        "full_name": "Existing User",
        "email": "existing@example.com",
        "password": "password",
        "address": "123 Test St",
        "phone_number": "1234567890"
    })
    response = client.post("/signup", json={
        "username": "existinguser",
        "full_name": "Existing User",
        "email": "existing@example.com",
        "password": "password",
        "address": "123 Test St",
        "phone_number": "1234567890"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"

def test_login():
    client.post("/signup", json={
        "username": "loginuser",
        "full_name": "Login User",
        "email": "login@example.com",
        "password": "password",
        "address": "123 Test St",
        "phone_number": "1234567890"
    })
    response = client.post("/login", json={
        "email": "login@example.com",
        "password": "password"
    })
    assert response.status_code == 200
    assert "message" in response.json()

def test_get_user_profile():
    response = client.get("/users/test@example.com")
    assert response.status_code == 200
    assert "email" in response.json()

def test_update_user_profile():
    response = client.put("/users/test@example.com", json={
        "full_name": "Updated User",
        "address": "456 New St",
        "phone_number": "9876543210"
    })
    assert response.status_code == 200
    assert "message" in response.json()

# ------------------------------
# Furniture Items Tests
# ------------------------------

def test_get_all_items():
    response = client.get("/items")
    assert response.status_code == 200
    assert "items" in response.json()
    assert isinstance(response.json()["items"], list)

# ------------------------------
# Shopping Cart Tests
# ------------------------------

def test_add_item_to_cart():
    response = client.post("/cart/add", params={"email": "test@example.com"}, json={
        "item_id": 101,
        "quantity": 2
    })
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Item added to cart"

def test_update_cart_item():
    response = client.put("/cart/update", params={"email": "test@example.com"}, json={
        "item_id": 101,
        "quantity": 5
    })
    assert response.status_code == 200
    assert "message" in response.json()

def test_delete_cart_item():
    response = client.delete("/cart/delete/101", params={"email": "test@example.com", "quantity": 1})
    assert response.status_code == 200
    assert "message" in response.json()

def test_view_cart():
    response = client.get("/cart/view", params={"email": "test@example.com"})
    assert response.status_code == 200
    assert "cart" in response.json()

# ------------------------------
# Inventory Tests
# ------------------------------

def test_update_inventory():
    response = client.put("/inventory/update/101", params={"quantity": 50})
    assert response.status_code == 200
    assert "message" in response.json()

def test_delete_inventory_item():
    response = client.delete("/inventory/delete/101")
    assert response.status_code == 200
    assert "message" in response.json()

# ------------------------------
# Orders Tests
# ------------------------------

def test_get_orders():
    response = client.get("/orders", params={"email": "test@example.com"})
    assert response.status_code == 200
    assert "orders" in response.json()


def test_checkout():
    # Step 1: Register user
    client.post("/signup", json={
        "username": "testuser",
        "full_name": "Test User",
        "email": "test@example.com",
        "password": "testpass",
        "address": "123 Test St",
        "phone_number": "1234567890"
    })

    # Step 2: Clear the cart before adding new items
    response_clear_cart = client.get("/cart/view", params={"email": "test@example.com"})
    cart_data = response_clear_cart.json().get("cart", {})

    # If cart is not empty, remove all items
    for item_id, quantity in cart_data.items():
        client.delete(f"/cart/delete/{item_id}", params={"email": "test@example.com", "quantity": quantity})

    # Step 3: Get updated inventory
    response_inventory = client.get("/items")
    print("Inventory Before Adding to Cart:", response_inventory.json())  # Debugging

    available_items = {
        item["item_id"]: item["available_quantity"]
        for item in response_inventory.json()["items"]
        if item["available_quantity"] > 0
    }

    assert available_items, "No items available to add to cart!"

    # Step 4: Add the first available item to cart
    item_id, available_qty = next(iter(available_items.items()))
    quantity_to_add = min(available_qty, 2)  # Ensure we don't exceed stock

    response_cart = client.post("/cart/add", params={"email": "test@example.com"}, json={
        "item_id": item_id,
        "quantity": quantity_to_add
    })
    assert response_cart.status_code == 200
    assert response_cart.json()["message"] == "Item added to cart"

    # Step 5: Print cart before checkout
    response_view_cart = client.get("/cart/view", params={"email": "test@example.com"})
    print("Cart Before Checkout:", response_view_cart.json())  # Debugging

    # Step 6: Proceed with checkout
    response_checkout = client.post("/checkout", json={
        "email": "test@example.com",
        "payment_method": "credit_card"
    })

    print("Checkout Response:", response_checkout.json())  # Debugging
    assert response_checkout.status_code == 200
    assert "message" in response_checkout.json()
    assert "Order placed successfully" in response_checkout.json()["message"]





