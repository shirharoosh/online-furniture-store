from user import User
from order import Order

def test_user_sign_up():
    """Tests user sign-up process."""
    user = User("johndoe", "John Doe", "john@example.com", "securepassword", "123 Elm St", "555-1234")
    assert user.sign_up() == "User 'johndoe' signed up successfully."

def test_user_login():
    """Tests user login with correct and incorrect credentials."""
    user = User("johndoe", "John Doe", "john@example.com", "securepassword", "123 Elm St", "555-1234")
    assert user.login("john@example.com", "securepassword") == "User 'johndoe' logged in successfully."
    assert user.login("john@example.com", "wrongpassword") == "Invalid email or password."

def test_manage_profile():
    user = User("johndoe", "John Doe", "john@example.com", "securepassword", "123 Elm St", "555-1234")
    user.login("john@example.com", "securepassword")
    assert user.manage_profile(full_name="Johnny Doe", address="456 Oak Ave") == "Profile for 'johndoe' updated successfully."
    assert user.full_name == "Johnny Doe"
    assert user._address == "456 Oak Ave"

def test_view_order_history():
    """Tests viewing order history for a user."""
    user = User("johndoe", "John Doe", "john@example.com", "securepassword", "123 Elm St", "555-1234")
    user.login("john@example.com", "securepassword")  # Ensure user is logged in

    assert user.view_order_history() == "No orders found in your history."  # Empty history

    # Simulate adding an order
    order = Order(user, items=[1], total_price=50, status="Completed")
    user.add_order(order)

    assert len(user.view_order_history()) == 1  # Ensure order was added
    assert user.view_order_history()[0].total_price == 50  # Check order price