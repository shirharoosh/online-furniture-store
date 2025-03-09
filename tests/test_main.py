import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import (
    app,
    initialize_inventory,
    initialize_users,
    sign_up,
    log_in,
    checkout_cli,
    inventory,
    user_accounts,
    shopping_carts,
    user_order_dict,
    catalog
)
from shopping_cart import ShoppingCart
from store_item import Table, Chair, Closet

@pytest.fixture
def client():
    """Fixture to create a test client for FastAPI."""
    return TestClient(app)

@pytest.fixture
def reset_globals():
    """Resets global state before each test."""
    inventory._items.clear()
    inventory.set_catalog({})
    user_accounts.clear()
    shopping_carts.clear()
    user_order_dict._user_orders.clear()

def test_initialize_inventory(reset_globals):
    """Tests that inventory is correctly initialized with catalog items."""
    initialize_inventory(catalog)
    for item_id in catalog:
        assert inventory.get_quantity(item_id) == 10

def test_initialize_users(reset_globals):
    """Tests that predefined users are correctly initialized."""
    initialize_users()
    assert "alice@example.com" in user_accounts
    assert isinstance(shopping_carts["alice@example.com"], ShoppingCart)

@patch("builtins.input", side_effect=["new@example.com", "NewUser", "New User", "pass123", "123 St", "555-5555"])
def test_sign_up(mock_input, reset_globals):
    """Tests the sign-up process."""
    user = sign_up()
    assert user.email == "new@example.com"
    assert user_accounts["new@example.com"] == user

@patch("builtins.input", side_effect=["alice@example.com", "Alice123"])
def test_log_in(mock_input, reset_globals):
    """Tests user login."""
    initialize_users()
    user = log_in()
    assert user is not None
    assert user.email == "alice@example.com"

def test_get_items(client, reset_globals):
    """Tests retrieving all items from the inventory."""
    initialize_inventory(catalog)
    response = client.get("/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_get_single_item(client, reset_globals):
    """Tests retrieving a specific item."""
    initialize_inventory(catalog)
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Modern Table"

def test_register_user(client, reset_globals):
    """Tests registering a new user via API."""
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
    """Tests user login via API."""
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
    assert "message" in response.json()

def test_update_inventory(client, reset_globals):
    """Tests updating inventory item quantity."""
    initialize_inventory(catalog)
    response = client.put("/inventory/1", json={"quantity": 20})
    assert response.status_code == 200
    assert inventory.get_quantity(1) == 20

def test_remove_inventory_item(client, reset_globals):
    """Tests removing an inventory item."""
    initialize_inventory(catalog)
    response = client.delete("/inventory/1")
    assert response.status_code == 200
    assert 1 not in inventory.items

def test_add_item_to_cart(client, reset_globals):
    """Tests adding an item to the shopping cart."""
    initialize_inventory(catalog)
    response = client.post("/cart/items", json={"item_id": 1, "quantity": 2})
    assert response.status_code == 200
    assert "message" in response.json()

def test_remove_item_from_cart(client, reset_globals):
    """Tests removing an item from the shopping cart."""
    initialize_inventory(catalog)
    client.post("/cart/items", json={"item_id": 1, "quantity": 2})
    response = client.delete("/cart/items/1", params={"quantity": 1})
    assert response.status_code == 200

def test_checkout_api(client, reset_globals):
    """Tests the API checkout process."""
    initialize_users()
    client.post("/users/register", json={
        "username": "testuser",
        "full_name": "Test User",
        "email": "test@example.com",
        "password": "testpass",
        "address": "123 Test St",
        "phone_number": "1234567890"
    })
    response = client.post("/checkout", params={"username": "testuser"})
    assert response.status_code == 400  # Cart is empty, should fail

@patch("builtins.input", side_effect=["123 Test St", "Credit Card"])
def test_checkout_insufficient_inventory(mock_input, reset_globals):
    """Tests checkout failing due to insufficient inventory."""
    initialize_users()
    user = user_accounts["alice@example.com"]
    shopping_carts[user.email] = ShoppingCart(inventory)
    inventory.add_item(1, 1)
    shopping_carts[user.email].add_furniture(1, 2)

    checkout_cli(user, shopping_carts[user.email])
    assert inventory.get_quantity(1) == 1  # Stock should remain unchanged
    assert not user_order_dict.get_orders_for_user(user), "Checkout should fail with insufficient stock."

@patch("builtins.input", side_effect=["123 Test St", "Credit Card"])
def test_checkout_cli(mock_input, reset_globals):
    """Tests the CLI checkout process."""
    initialize_users()
    user = user_accounts["alice@example.com"]
    shopping_carts[user.email] = ShoppingCart(inventory)

    # Ensure catalog is set before adding items
    catalog = {
        1: Table(1, "Table", 200, 120, 75, 30, "Some table"),
        2: Chair(2, "Office Chair", 80, 100, 50, 10, "An ergonomic office chair.", material="Leather"),
        3: Closet(3, "Closet", 800, 180, 220, 80, "Some closet", with_mirror=True)
    }
    inventory.set_catalog(catalog)
    inventory.add_item(1, 5)

    shopping_carts[user.email].add_furniture(1, 2)  # Should now work

    with patch("builtins.print") as mock_print:  # Capture printed messages
        checkout_cli(user, shopping_carts[user.email])

    # Ensure checkout messages were printed
    printed_messages = [call.args[0] for call in mock_print.call_args_list]
    assert any("Order placed successfully" in msg for msg in printed_messages), "Checkout should be successful."
    assert user_order_dict.get_orders_for_user(user), "Order should exist after checkout."

