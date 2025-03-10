import pytest
from api import app, inventory, shopping_cart, user_db, orders, user_order_dict
from store_item import Table, Closet, Chair
from fastapi.testclient import TestClient

client = TestClient(app)

@pytest.fixture
def reset_state():
    """Resets the global state before each test."""
    inventory._items.clear()
    shopping_cart._cart_items.clear()
    shopping_cart._total_price = 0.0
    user_db.clear()
    orders.clear()
    user_order_dict._user_orders.clear()
    inventory.set_catalog({
        1: Table(1, "Table", 200, 120, 75, 30, "Some table"),
        2: Chair(2, "Office Chair", 80, 100, 50, 10, "An ergonomic office chair.", material="Leather"),
        3: Closet(3, "Closet", 800, 180, 220, 80, "Some closet", with_mirror=True)
    })
    for item_id in inventory.get_catalog():
        inventory.add_item(item_id, 10)


def test_order_process_updates_all_components(reset_state):
    """Tests that processing an order updates the inventory, user order history, and clears the cart."""

    # Step 1: Register a user
    user_data = {
        "username": "testuser",
        "full_name": "Test User",
        "email": "test@example.com",
        "password": "securepassword",
        "address": "123 Test St",
        "phone_number": "555-1234"
    }
    response = client.post("/users/register", json=user_data)
    assert response.status_code == 200

    # Step 2: Add item to shopping cart
    cart_item = {"item_id": 1, "quantity": 2}
    response = client.post("/cart/items", json=cart_item)
    assert response.status_code == 200
    assert "Item added to cart." in response.json()["message"]

    # Step 3: Check inventory before checkout
    initial_stock = inventory.get_quantity(1)
    assert initial_stock == 10  # Since we reset to 10

    # Step 4: Process checkout
    response = client.post("/checkout", params={"username": "testuser"})
    assert response.status_code == 200
    assert "Checkout successful." in response.json()["message"]

    # Step 5: Validate Inventory was Updated
    updated_stock = inventory.get_quantity(1)
    assert updated_stock == 8, f"Expected inventory to be reduced to 8, but got {updated_stock}"

    # Step 6: Validate Shopping Cart is Cleared
    assert not shopping_cart._cart_items, "Shopping cart should be empty after checkout."
    assert shopping_cart._total_price == 0.0, "Shopping cart total price should reset to 0."

    # Step 7: Validate Order is Recorded
    assert len(orders) == 1, "An order should have been created."
    assert orders[0].user.username == "testuser", "Order should belong to testuser."
    assert orders[0].total_price == 400, "Order total should match 2 * $200."

    # Step 8: Validate Order History in User Data
    user_orders = user_order_dict.get_orders_for_user(user_db["testuser"])
    assert len(user_orders) == 1, "User order history should have one order."
    assert user_orders[0].total_price == 400, "User order total should match the processed order."

    print("Regression test passed: All components updated correctly after order processing.")

