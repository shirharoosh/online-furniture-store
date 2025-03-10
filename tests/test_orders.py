import pytest
from order import Order
from store_item import Table, Bed, Closet, Chair, Sofa, StoreItem

@pytest.fixture
def sample_orders():
    """Creates sample orders with different StoreItem objects"""
    item1 = Table(1, "Dining Table", 150.0, 75, 120, 50.0, "A wooden dining table")
    item2 = Bed(2, "King Bed", 300.0, 60, 80, 70.0, "A king-sized bed", pillow_count=4)
    item3 = Closet(3, "Wardrobe", 200.0, 180, 100, 80.0, "A wardrobe with mirror", with_mirror=True)
    item4 = Chair(4, "Office Chair", 100.0, 50, 50, 30.0, "A comfortable office chair", material="leather")
    item5 = Sofa(5, "Living Room Sofa", 500.0, 200, 80, 90.0, "A large comfortable sofa", seating_capacity=3)

    return [
        Order("user1", [item1, item2], 450.0, "pending"),
        Order("user2", [item3, item4], 300.0, "shipped"),
        Order("user3", [item5], 500.0, "delivered"),
        Order("user4", [item1, item3, item5], 850.0, "processing"),
        Order("user5", [], 0.0, "pending"),
    ]

@pytest.mark.parametrize(
    "user, items, total_price, status",
    [
        (
            "user1",
            [
                Table(1, "Dining Table", 150.0, 75, 120, 50.0, "A wooden dining table"),
                Bed(2, "King Bed", 300.0, 60, 80, 70.0, "A king-sized bed", pillow_count=4),
            ],
            450.0,
            "pending",
        ),
        (
            "user2",
            [
                Closet(3, "Wardrobe", 200.0, 180, 100, 80.0, "A wardrobe with mirror", with_mirror=True),
                Chair(4, "Office Chair", 100.0, 50, 50, 30.0, "A comfortable office chair", material="leather"),
            ],
            300.0,
            "shipped",
        ),
        (
            "user3",
            [
                Sofa(5, "Living Room Sofa", 500.0, 200, 80, 90.0, "A large comfortable sofa", seating_capacity=3)
            ],
            500.0,
            "delivered",
        ),
    ],
)

def test_order_initialization(user, items, total_price, status):
    """Tests if the Order Initializes correctly."""
    order = Order(user, items, total_price, status)
    assert order.user == user
    assert isinstance(order.items, list)
    assert all(isinstance(item, StoreItem) for item in order.items)
    assert order.total_price == total_price
    assert order.status == status

def test_status_update(sample_orders):
    """Tests updating order status"""
    sample_orders[0].update_status("shipped")
    assert sample_orders[0].status == "shipped"

    sample_orders[1].update_status("delivered")
    assert sample_orders[1].status == "delivered"

    sample_orders[2].update_status("processing")
    assert sample_orders[2].status == "processing"

    sample_orders[3].update_status("canceled")
    assert sample_orders[3].status == "canceled"

def test_invalid_status_update(sample_orders):
    """Tests if updating to an invalid status doesn't break functionality"""
    invalid_status = "nonexistent_status"
    sample_orders[0].update_status(invalid_status)
    assert sample_orders[0].status == invalid_status  # Assuming no validation in `update_status`

def test_total_price_calculation():
    """Ensures the total price matches the sum of item prices."""
    items = [
        Table(1, "Dining Table", 150.0, 75, 120, 50.0, "A wooden dining table"),
        Bed(2, "King Bed", 300.0, 60, 80, 70.0, "A king-sized bed", pillow_count=4)
    ]
    order = Order("user_test", items, sum(item.price for item in items))
    assert order.total_price == 450.0

def test_repr_method(sample_orders):
    """Tests the __repr__ method of Order class"""
    expected_reprs = [
        "Order(user=user1, total_price=$450.00, status='pending')",
        "Order(user=user2, total_price=$300.00, status='shipped')",
        "Order(user=user3, total_price=$500.00, status='delivered')",
        "Order(user=user4, total_price=$850.00, status='processing')",
        "Order(user=user5, total_price=$0.00, status='pending')",
    ]
    for order, expected in zip(sample_orders, expected_reprs):
        assert repr(order) == expected

def test_empty_order():
    """Tests creating an order with no items"""
    empty_order = Order("test_user", [], 0.0)
    assert isinstance(empty_order.items, list)
    assert empty_order.items == []
    assert empty_order.total_price == 0.0
    assert empty_order.status == "pending"

def test_custom_status_initialization():
    """Tests initializing order with a custom status"""
    custom_order = Order(
        "test_user",
        [Table(4, "Coffee Table", 80.0, 40, 60, 20.0, "A small coffee table")],
        80.0,
        "shipped",
    )
    assert custom_order.status == "shipped"

def test_items_are_store_items(sample_orders):
    """Checks that all order items are instances of StoreItem"""
    for order in sample_orders:
        for item in order.items:
            assert isinstance(item, StoreItem), f"Item {item} is not an instance of StoreItem"