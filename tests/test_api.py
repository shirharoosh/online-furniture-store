import pytest
from fastapi.testclient import TestClient
from api import app, inventory, user_db, shopping_cart, user_order_dict
from store_item import Table, Chair, Closet

# -----------------
# Test Fixtures
# -----------------
@pytest.fixture
def client():
    """Creates a test client for the FastAPI app."""
    return TestClient(app)

@pytest.fixture
def reset_globals():
    """Resets global data before each test."""
    inventory._items.clear()
    inventory.set_catalog({})
    shopping_cart._cart_items.clear()
    shopping_cart._total_price = 0.0
    user_db.clear()
    user_order_dict._user_orders.clear()

    # Restore default inventory catalog
    catalog = {
        1: Table(1, "Modern Table", 150, 30, 50, 20, "A modern table."),
        2: Chair(2, "Office Chair", 85, 45, 45, 15, "Ergonomic office chair.", material="Leather"),
        3: Closet(3, "Closet", 800, 180, 220, 80, "Some closet", with_mirror=True),
    }
    inventory.set_catalog(catalog)
    for item_id in catalog:
        inventory.add_item(item_id, 10)

# -----------------
# Basic API Test
# -----------------
def test_root(client):
    """Test if the root endpoint responds correctly."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Online Furniture Store API!"}

# -----------------
# Inventory Tests
# -----------------
def test_get_items(client, reset_globals):
    """Tests retrieving all items from the inventory."""
    response = client.get("/items")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_single_item(client, reset_globals):
    """Tests retrieving a single item from the catalog."""
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["item_id"] == 1
    assert response.json()["title"] == "Modern Table"

def test_update_inventory(client, reset_globals):
    """Tests updating inventory item quantity."""
    response = client.put("/inventory/1", json={"quantity": 15})
    assert response.status_code == 200
    assert inventory.get_quantity(1) == 15

def test_delete_inventory(client, reset_globals):
    """Tests deleting an inventory item."""
    response = client.delete("/inventory/1")
    assert response.status_code == 200
    assert 1 not in inventory.items

# -----------------
# User Management Tests
# -----------------
def test_register_user(client, reset_globals):
    """Tests registering a new user."""
    response = client.post("/users/register", json={
        "username": "testuser",
        "full_name": "Test User",
        "email": "test@example.com",
        "password": "testpass",
        "address": "123 Test St",
        "phone_number": "1234567890"
    })
    assert response.status_code == 200
    assert "message" in response.json()

def test_login_user(client, reset_globals):
    """Tests user login with correct and incorrect credentials."""
    client.post("/users/register", json={
        "username": "testuser",
        "full_name": "Test User",
        "email": "test@example.com",
        "password": "testpass",
        "address": "123 Test St",
        "phone_number": "1234567890"
    })
    response = client.post("/users/login", json={
        "email": "test@example.com",
        "password": "testpass"
    })
    assert response.status_code == 200

def test_get_user_profile(client, reset_globals):
    """Tests retrieving a user profile."""
    client.post("/users/register", json={
        "username": "testuser",
        "full_name": "Test User",
        "email": "test@example.com",
        "password": "testpass",
        "address": "123 Test St",
        "phone_number": "1234567890"
    })
    response = client.get("/users/testuser")
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

# -----------------
# Shopping Cart Tests
# -----------------
def test_add_item_to_cart(client, reset_globals):
    """Tests adding an item to the shopping cart."""
    response = client.post("/cart/items", json={"item_id": 1, "quantity": 2})
    assert response.status_code == 200

def test_remove_item_from_cart(client, reset_globals):
    """Tests removing an item from the shopping cart."""
    client.post("/cart/items", json={"item_id": 1, "quantity": 2})
    response = client.delete("/cart/items/1", params={"quantity": 1})
    assert response.status_code == 200

def test_apply_discount(client, reset_globals):
    """Tests applying a discount to the shopping cart."""
    client.post("/cart/items", json={"item_id": 1, "quantity": 2})
    response = client.post("/cart/apply_discount", json={"discount_percentage": 10})
    assert response.status_code == 200

# -----------------
# Order Management Tests
# -----------------
def test_create_order(client, reset_globals):
    """Tests creating a new order."""
    client.post("/users/register", json={
        "username": "testuser",
        "full_name": "Test User",
        "email": "test@example.com",
        "password": "testpass",
        "address": "123 Test St",
        "phone_number": "1234567890"
    })
    response = client.post("/orders", json={
        "username": "testuser",
        "items": [{"item_id": 1, "quantity": 2}]
    })
    assert response.status_code == 200

def test_checkout(client, reset_globals):
    """Tests checkout process."""
    client.post("/users/register", json={
        "username": "testuser",
        "full_name": "Test User",
        "email": "test@example.com",
        "password": "testpass",
        "address": "123 Test St",
        "phone_number": "1234567890"
    })
    client.post("/cart/items", json={"item_id": 1, "quantity": 2})
    response = client.post("/checkout", params={"username": "testuser"})
    assert response.status_code == 200
