from user import User

def test_user_sign_up():
    user = User("johndoe", "John Doe", "john@example.com", "securepassword", "123 Elm St", "555-1234")
    assert user.sign_up() == "User 'johndoe' signed up successfully."

def test_user_login():
    user = User("johndoe", "John Doe", "john@example.com", "securepassword", "123 Elm St", "555-1234")
    assert user.login("john@example.com", "securepassword") == "User 'johndoe' logged in successfully."
    assert user.login("john@example.com", "wrongpassword") == "Invalid email or password. Try again."

def test_manage_profile():
    user = User("johndoe", "John Doe", "john@example.com", "securepassword", "123 Elm St", "555-1234")
    user.login("john@example.com", "securepassword")
    assert user.manage_profile(full_name="Johnny Doe", address="456 Oak Ave") == "Profile for 'johndoe' updated successfully."
    assert user.full_name == "Johnny Doe"
    assert user.address == "456 Oak Ave"

def test_view_order_history():
    user = User("johndoe", "John Doe", "john@example.com", "securepassword", "123 Elm St", "555-1234")
    user.login("john@example.com", "securepassword")
    assert user.view_order_history() == "No orders found in your history."
    user.order_hist.append({"item": "Chair", "price": 50})
    assert user.view_order_history() == [{"item": "Chair", "price": 50}]