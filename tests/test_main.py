import pytest
from unittest.mock import patch
from main import global_user_orders
from flask import Flask
from flask.testing import FlaskClient
from main import (
    app,
    initialize_inventory,
    initialize_users,
    sign_up,
    log_in,
    checkout,
    global_inventory,
    user_accounts,
    shopping_carts,
    user_interface
)
from store_item import Table, Chair, Sofa
from shopping_cart import ShoppingCart
from user import User
from order import Order


@pytest.fixture
def client():
    """Creates a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def reset_globals():
    """Resets global state before each test."""
    global_inventory._items.clear()
    global_inventory.set_catalog({})
    user_accounts.clear()
    shopping_carts.clear()
    global_user_orders._orders.clear()



def test_initialize_inventory(reset_globals):
    """Tests that inventory is initialized correctly with catalog items."""
    catalog = {
        101: Table(101, "Dining Table", 250, 75, 150, 30, "A sturdy wooden dining table."),
        102: Chair(102, "Office Chair", 80, 100, 50, 10, "An ergonomic office chair.", material="Leather"),
    }
    initialize_inventory(catalog)
    assert global_inventory.get_quantity(101) == 10
    assert global_inventory.get_quantity(102) == 10


def test_initialize_users(reset_globals):
    """Tests that predefined users are correctly added to the system."""
    initialize_users()
    assert "alice@example.com" in user_accounts
    assert "bob@example.com" in user_accounts
    assert shopping_carts["alice@example.com"]


@patch("builtins.input", side_effect=["new@example.com", "NewUser", "New User", "pass123", "123 St", "555-5555"])
def test_sign_up(mock_input, reset_globals):
    """Tests the sign-up flow by simulating user input."""
    user = sign_up()
    assert user.email == "new@example.com"
    assert user_accounts["new@example.com"] == user


@patch("builtins.input", side_effect=["alice@example.com", "Alice123"])
def test_log_in(mock_input, reset_globals):
    """Tests logging in an existing user."""
    initialize_users()
    user = log_in()
    assert user is not None
    assert user.email == "alice@example.com"


def test_checkout(reset_globals):
    """Tests checkout flow ensuring inventory is updated and order is created."""
    initialize_users()
    user = user_accounts["alice@example.com"]
    shopping_carts[user.email] = ShoppingCart(global_inventory)

    # Add an item to the inventory & shopping cart
    catalog = {101: Table(101, "Dining Table", 250, 75, 150, 30, "A sturdy wooden dining table.")}
    global_inventory.set_catalog(catalog)  # Ensure catalog exists
    global_inventory.add_item(101, 5)

    shopping_carts[user.email].add_furniture(101, 2)
    assert global_inventory.get_quantity(101) == 5

    # Mock `input()` responses for shipping address and payment method
    with patch("builtins.input", side_effect=["123 Test St", "Credit Card"]):
        checkout(user, shopping_carts[user.email])

    assert global_inventory.get_quantity(101) == 3  # Inventory should be reduced


def test_user_interface_add_item(reset_globals):
    """Tests adding an item through the user interface."""
    initialize_users()
    user = user_accounts["alice@example.com"]
    shopping_carts[user.email] = ShoppingCart(global_inventory)

    # Ensure the inventory has an item
    global_inventory.add_item(101, 10)
    catalog = {101: Table(101, "Dining Table", 250, 75, 150, 30, "A sturdy wooden dining table.")}
    global_inventory.set_catalog(catalog)

    with patch("builtins.input", side_effect=["1", "101", "2", "6"]):  # Add item, then log out
        user_interface(user)

    assert shopping_carts[user.email]._cart_items[101] == 2


def test_user_interface_invalid_choice(reset_globals):
    """Tests invalid input handling in the user interface."""
    initialize_users()
    user = user_accounts["alice@example.com"]
    shopping_carts[user.email] = ShoppingCart(global_inventory)

    with patch("builtins.input", side_effect=["invalid", "6"]):  # Invalid choice, then log out
        user_interface(user)

    assert shopping_carts[user.email]._cart_items == {}


def test_user_interface_remove_item(reset_globals):
    """Tests removing an item through the user interface."""
    initialize_users()
    user = user_accounts["alice@example.com"]
    shopping_carts[user.email] = ShoppingCart(global_inventory)

    # Ensure the inventory has an item
    global_inventory.add_item(101, 10)
    catalog = {101: Table(101, "Dining Table", 250, 75, 150, 30, "A sturdy wooden dining table.")}
    global_inventory.set_catalog(catalog)

    shopping_carts[user.email].add_furniture(101, 2)

    with patch("builtins.input", side_effect=["2", "101", "1", "6"]):  # Remove one item, then log out
        user_interface(user)

    assert shopping_carts[user.email]._cart_items[101] == 1

import pytest
from unittest.mock import patch
from flask import Flask
from flask.testing import FlaskClient
from main import (
    app,
    initialize_inventory,
    initialize_users,
    sign_up,
    log_in,
    checkout,
    global_inventory,
    user_accounts,
    shopping_carts,
    user_interface
)
from store_item import Table, Chair, Sofa
from shopping_cart import ShoppingCart
from user import User
from order import Order


@pytest.fixture
def client():
    """Creates a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def reset_globals():
    """Resets global state before each test."""
    global_inventory._items.clear()
    global_inventory.set_catalog({})
    user_accounts.clear()
    shopping_carts.clear()


def test_initialize_inventory(reset_globals):
    """Tests that inventory is initialized correctly with catalog items."""
    catalog = {
        101: Table(101, "Dining Table", 250, 75, 150, 30, "A sturdy wooden dining table."),
        102: Chair(102, "Office Chair", 80, 100, 50, 10, "An ergonomic office chair.", material="Leather"),
    }
    initialize_inventory(catalog)
    assert global_inventory.get_quantity(101) == 10
    assert global_inventory.get_quantity(102) == 10


def test_initialize_users(reset_globals):
    """Tests that predefined users are correctly added to the system."""
    initialize_users()
    assert "alice@example.com" in user_accounts
    assert "bob@example.com" in user_accounts
    assert shopping_carts["alice@example.com"]


@patch("builtins.input", side_effect=["new@example.com", "NewUser", "New User", "pass123", "123 St", "555-5555"])
def test_sign_up(mock_input, reset_globals):
    """Tests the sign-up flow by simulating user input."""
    user = sign_up()
    assert user.email == "new@example.com"
    assert user_accounts["new@example.com"] == user


@patch("builtins.input", side_effect=["alice@example.com", "Alice123"])
def test_log_in(mock_input, reset_globals):
    """Tests logging in an existing user."""
    initialize_users()
    user = log_in()
    assert user is not None
    assert user.email == "alice@example.com"


def test_checkout(reset_globals):
    """Tests checkout flow ensuring inventory is updated and order is created."""
    initialize_users()
    user = user_accounts["alice@example.com"]
    shopping_carts[user.email] = ShoppingCart(global_inventory)

    # Add an item to the inventory & shopping cart
    catalog = {101: Table(101, "Dining Table", 250, 75, 150, 30, "A sturdy wooden dining table.")}
    global_inventory.set_catalog(catalog)  # Ensure catalog exists
    global_inventory.add_item(101, 5)

    shopping_carts[user.email].add_furniture(101, 2)
    assert global_inventory.get_quantity(101) == 5

    # Mock `input()` responses for shipping address and payment method
    with patch("builtins.input", side_effect=["123 Test St", "Credit Card"]):
        checkout(user, shopping_carts[user.email])

    assert global_inventory.get_quantity(101) == 3  # Inventory should be reduced


def test_user_interface_add_item(reset_globals):
    """Tests adding an item through the user interface."""
    initialize_users()
    user = user_accounts["alice@example.com"]
    shopping_carts[user.email] = ShoppingCart(global_inventory)

    # Ensure the inventory has an item
    global_inventory.add_item(101, 10)
    catalog = {101: Table(101, "Dining Table", 250, 75, 150, 30, "A sturdy wooden dining table.")}
    global_inventory.set_catalog(catalog)

    with patch("builtins.input", side_effect=["1", "101", "2", "6"]):  # Add item, then log out
        user_interface(user)

    assert shopping_carts[user.email]._cart_items[101] == 2


def test_user_interface_invalid_choice(reset_globals):
    """Tests invalid input handling in the user interface."""
    initialize_users()
    user = user_accounts["alice@example.com"]
    shopping_carts[user.email] = ShoppingCart(global_inventory)

    with patch("builtins.input", side_effect=["invalid", "6"]):  # Invalid choice, then log out
        user_interface(user)

    assert shopping_carts[user.email]._cart_items == {}


def test_user_interface_remove_item(reset_globals):
    """Tests removing an item through the user interface."""
    initialize_users()
    user = user_accounts["alice@example.com"]
    shopping_carts[user.email] = ShoppingCart(global_inventory)

    # Ensure the inventory has an item
    global_inventory.add_item(101, 10)
    catalog = {101: Table(101, "Dining Table", 250, 75, 150, 30, "A sturdy wooden dining table.")}
    global_inventory.set_catalog(catalog)

    shopping_carts[user.email].add_furniture(101, 2)

    with patch("builtins.input", side_effect=["2", "101", "1", "6"]):  # Remove one item, then log out
        user_interface(user)

    assert shopping_carts[user.email]._cart_items[101] == 1

def test_view_inventory(client, reset_globals):
    """Tests the Flask API endpoint for retrieving inventory data."""
    # Fully reset inventory and users
    global_inventory._items.clear()
    global_inventory.set_catalog({})  # Ensure a clean catalog
    user_accounts.clear()
    shopping_carts.clear()

    # Reinitialize with only one item
    catalog = {
        101: Table(101, "Dining Table", 250, 75, 150, 30, "A sturdy wooden dining table.")
    }
    initialize_inventory(catalog)


    # Call API to get inventory
    response = client.get("/api/inventory")
    assert response.status_code == 200

    # Convert JSON keys back to integers
    inventory_data = {int(k): v for k, v in response.get_json().items()}
    expected_inventory = {101: 10}

    assert inventory_data == expected_inventory, f"Expected {expected_inventory}, but got {inventory_data}"


def test_checkout_empty_cart(reset_globals):
    """Tests that checkout fails when the cart is empty."""
    initialize_users()
    user = user_accounts["alice@example.com"]
    shopping_carts[user.email] = ShoppingCart(global_inventory)

    # Ensure cart is empty before checkout
    assert not shopping_carts[user.email]._cart_items, "Cart should be empty before checkout"

    # Clear any previous orders for this user
    global_user_orders.clear_user_orders(user)

    with patch("builtins.input", side_effect=["123 Test St", "Credit Card"]):
        with patch("builtins.print") as mock_print:  # Capture printed messages
            checkout(user, shopping_carts[user.email])

    # Extract printed messages
    printed_messages = [call.args[0] for call in mock_print.call_args_list]

    # Ensure the function printed that the cart is empty
    assert any("Your cart is empty" in msg for msg in printed_messages), "Expected 'Your cart is empty' message."

    # ✅ Ensure no orders were created
    orders = global_user_orders.get_orders_for_user(user)
    print("Orders After Checkout:", orders)  # Debugging output
    assert not orders, f"Checkout should fail with an empty cart, but got orders: {orders}"


def test_update_cart_item(reset_globals):
    """Tests updating the quantity of an item in the cart."""
    initialize_users()
    user = user_accounts["alice@example.com"]
    shopping_carts[user.email] = ShoppingCart(global_inventory)

    global_inventory.add_item(101, 10)
    catalog = {101: Table(101, "Dining Table", 250, 75, 150, 30, "A sturdy wooden dining table.")}
    global_inventory.set_catalog(catalog)

    shopping_carts[user.email].add_furniture(101, 1)
    assert shopping_carts[user.email]._cart_items[101] == 1  # Initially 1

    shopping_carts[user.email].add_furniture(101, 2)
    assert shopping_carts[user.email]._cart_items[101] == 3  # Updated to 3


def test_checkout_insufficient_inventory(reset_globals):
    """Tests that checkout fails when inventory is insufficient."""
    initialize_users()
    user = user_accounts["alice@example.com"]
    shopping_carts[user.email] = ShoppingCart(global_inventory)

    global_inventory.add_item(101, 1)  # Only 1 in stock
    catalog = {101: Table(101, "Dining Table", 250, 75, 150, 30, "A sturdy wooden dining table.")}
    global_inventory.set_catalog(catalog)

    shopping_carts[user.email].add_furniture(101, 2)  # Try adding 2 when only 1 in stock

    with patch("builtins.input", side_effect=["123 Test St", "Credit Card"]):
        checkout(user, shopping_carts[user.email])

    assert global_inventory.get_quantity(101) == 1  # Stock should remain unchanged
    assert not global_user_orders.get_orders_for_user(user), "Checkout should fail with insufficient stock."


def test_user_interface_view_cart(reset_globals):
    """Tests viewing the shopping cart through the user interface."""
    initialize_users()
    user = user_accounts["alice@example.com"]
    shopping_carts[user.email] = ShoppingCart(global_inventory)

    global_inventory.add_item(101, 10)
    catalog = {101: Table(101, "Dining Table", 250, 75, 150, 30, "A sturdy wooden dining table.")}
    global_inventory.set_catalog(catalog)

    shopping_carts[user.email].add_furniture(101, 3)

    with patch("builtins.input", side_effect=["3", "6"]):  # View cart, then log out
        user_interface(user)

    assert shopping_carts[user.email]._cart_items[101] == 3  # Ensure item is still in cart


def test_remove_nonexistent_item_from_cart(reset_globals):
    """Tests attempting to remove an item that isn’t in the cart."""
    initialize_users()
    user = user_accounts["alice@example.com"]
    shopping_carts[user.email] = ShoppingCart(global_inventory)

    with patch("builtins.input", side_effect=["2", "999", "1", "6"]):  # Try removing non-existent item, then log out
        user_interface(user)

    assert shopping_carts[user.email]._cart_items == {}  # Cart should still be empty


@patch("builtins.input", side_effect=["alice@example.com", "Alice123"])
def test_sign_up_existing_email(mock_input, reset_globals):
    """Tests signing up with an existing email, which should fail."""
    initialize_users()
    user = sign_up()

    assert user is None, "Sign-up should fail when email is already registered."
