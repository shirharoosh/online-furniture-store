import pytest
from user import User
from order import Order

@pytest.fixture
def test_user():
    """Creates a test User instance."""
    return User("johndoe", "John Doe", "john@example.com", "securepassword", "123 Elm St", "555-1234")

def test_user_sign_up(test_user):
    """Tests user sign-up process."""
    assert test_user.sign_up() == "User 'johndoe' signed up successfully."

def test_user_login(test_user):
    """Tests user login with correct and incorrect credentials."""
    assert test_user.login("john@example.com", "securepassword") == "User 'johndoe' logged in successfully."
    assert test_user.login("john@example.com", "wrongpassword") == "Invalid email or password."
    assert test_user.login("wrongemail@example.com", "securepassword") == "Invalid email or password."

def test_password_hashing(test_user):
    """Ensures password hashing works and plaintext passwords are not stored."""
    assert isinstance(test_user._password_hash, bytes)  # Password hash should be stored as bytes
    assert test_user._password_hash != "securepassword"  # Ensure plaintext password is not stored

def test_password_verification(test_user):
    """Checks that password verification works properly."""
    assert test_user.verify_password("securepassword") is True
    assert test_user.verify_password("wrongpassword") is False

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

def test_user_repr(test_user):
    """Tests user string representation."""
    expected_repr = "User(username='johndoe', email='john@example.com', full_name='John Doe')"
    assert repr(test_user) == expected_repr