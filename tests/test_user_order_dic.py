import pytest
from user_order_dic import UserOrderDictionary
from order import Order


class MockUser:
    """Mock user class for testing."""

    def __init__(self, username):
        self.username = username
        self.orders = []

    def add_order(self, order):
        """Adds an order to the user's order history."""
        self.orders.append(order)


@pytest.fixture
def sample_user_orders():
    """Creates a sample UserOrderDictionary instance."""
    return UserOrderDictionary()


@pytest.fixture
def mock_users():
    """Creates mock users for testing."""
    return {
        "alice": MockUser("alice"),
        "bob": MockUser("bob"),
        "charlie": MockUser("charlie"),
    }


def test_update_order(sample_user_orders, mock_users):
    """Tests adding multiple orders for a user."""
    order1 = Order(mock_users["alice"], [], 100.0, "pending")
    order2 = Order(mock_users["alice"], [], 150.0, "shipped")

    sample_user_orders.update(order1)
    sample_user_orders.update(order2)

    assert len(sample_user_orders.get_orders_for_user(mock_users["alice"])) == 2
    assert mock_users["alice"].orders == [order1, order2]


def test_get_orders_for_nonexistent_user(sample_user_orders, mock_users):
    """Tests retrieving orders for a user who has not placed any orders."""
    assert sample_user_orders.get_orders_for_user(mock_users["charlie"]) == []


def test_multiple_users_orders(sample_user_orders, mock_users):
    """Tests order management for multiple users."""
    order1 = Order(mock_users["alice"], [], 200.0, "delivered")
    order2 = Order(mock_users["bob"], [], 250.0, "pending")
    order3 = Order(mock_users["alice"], [], 300.0, "shipped")

    sample_user_orders.update(order1)
    sample_user_orders.update(order2)
    sample_user_orders.update(order3)

    assert len(sample_user_orders.get_orders_for_user(mock_users["alice"])) == 2
    assert len(sample_user_orders.get_orders_for_user(mock_users["bob"])) == 1
    assert mock_users["alice"].orders == [order1, order3]
    assert mock_users["bob"].orders == [order2]


def test_order_history_integrity(sample_user_orders, mock_users):
    """Ensures that modifying retrieved order lists does not affect the original dictionary."""
    order1 = Order(mock_users["alice"], [], 300.0, "shipped")
    sample_user_orders.update(order1)

    orders = sample_user_orders.get_orders_for_user(mock_users["alice"])
    orders.append(Order(mock_users["alice"], [], 400.0, "pending"))

    assert len(sample_user_orders.get_orders_for_user(mock_users["alice"])) == 1


def test_updating_same_order_multiple_times(sample_user_orders, mock_users):
    """Tests adding the same order multiple times for a user."""
    order = Order(mock_users["alice"], [], 100.0, "pending")
    sample_user_orders.update(order)
    sample_user_orders.update(order)

    assert len(sample_user_orders.get_orders_for_user(mock_users["alice"])) == 2


def test_empty_order_list_for_new_user(sample_user_orders, mock_users):
    """Tests that a newly created user with no orders returns an empty list."""
    assert sample_user_orders.get_orders_for_user(mock_users["charlie"]) == []


def test_large_number_of_orders(sample_user_orders, mock_users):
    """Tests handling a large number of orders for a user."""
    for i in range(1000):
        sample_user_orders.update(Order(mock_users["alice"], [], i * 10, "pending"))

    assert len(sample_user_orders.get_orders_for_user(mock_users["alice"])) == 1000


def test_removing_orders_does_not_affect_user_orders(sample_user_orders, mock_users):
    """Ensures that deleting an order reference externally does not remove it from the dictionary."""
    order = Order(mock_users["alice"], [], 200.0, "shipped")
    sample_user_orders.update(order)
    del order

    assert len(sample_user_orders.get_orders_for_user(mock_users["alice"])) == 1

def test_clear_user_orders(sample_user_orders, mock_users):
    """Tests clearing a user's order history."""
    order1 = Order(mock_users["alice"], [], 300.0, "shipped")
    sample_user_orders.update(order1)

    sample_user_orders.clear_user_orders(mock_users["alice"])
    assert sample_user_orders.get_orders_for_user(mock_users["alice"]) == []

def test_orders_are_stored_correctly(sample_user_orders, mock_users):
    """Ensures that user orders persist after retrieval."""
    order1 = Order(mock_users["alice"], [], 500.0, "processing")
    sample_user_orders.update(order1)

    retrieved_orders = sample_user_orders.get_orders_for_user(mock_users["alice"])
    assert retrieved_orders[0] is order1  # Ensure the reference is the same
    assert retrieved_orders[0].total_price == 500.0