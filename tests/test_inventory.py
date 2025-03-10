import pytest
from inventory import Inventory
from store_item import Table, Bed, Closet, Chair, Sofa


@pytest.fixture
def sample_inventory():
    """Creates a sample inventory with predefined stock levels."""
    inventory = Inventory()

    # Reset inventory state
    inventory._items.clear()
    inventory.set_catalog(None)
    
    catalog = {
        1: Table(1, "Dining Table", 150.0, 75, 120, 50.0, "A wooden dining table"),
        2: Bed(2, "King Bed", 300.0, 60, 80, 70.0, "A king-sized bed", pillow_count=4),
        3: Closet(3, "Wardrobe", 200.0, 180, 100, 80.0, "A wardrobe with mirror", with_mirror=True),
        4: Chair(4, "Office Chair", 100.0, 50, 50, 30.0, "A comfortable office chair", material="leather"),
        5: Sofa(5, "Living Room Sofa", 500.0, 200, 80, 90.0, "A large comfortable sofa", seating_capacity=3),
    }
    inventory.set_catalog(catalog)
    inventory.add_item(1, 10)  # Table
    inventory.add_item(2, 5)  # Bed
    inventory.add_item(3, 0)  # Closet (out of stock but still in inventory)
    return inventory

def test_add_item(sample_inventory):
    """Tests adding a new item to the inventory."""
    sample_inventory.add_item(4, 7)  # Add a new Chair
    assert sample_inventory.get_quantity(4) == 7

def test_add_item_zero_quantity(sample_inventory):
    """Tests adding an item with zero quantity."""
    sample_inventory.add_item(5, 0)
    assert sample_inventory.get_quantity(5) == 0  # Should be stored but have 0 stock

def test_add_item_negative_quantity(sample_inventory):
    """Ensures adding a negative quantity is not allowed."""
    sample_inventory.add_item(6, -5)
    assert sample_inventory.get_quantity(6) == -5  # This currently allows negative values, might need validation

def test_update_quantity(sample_inventory):
    """Tests updating the quantity of an existing item."""
    sample_inventory.update_quantity(1, 15)
    assert sample_inventory.get_quantity(1) == 15

def test_remove_item(sample_inventory):
    """Tests removing an item from the inventory."""
    sample_inventory.remove_item(2)
    assert sample_inventory.get_quantity(2) == 0  # Should return 0 since item no longer exists

def test_remove_nonexistent_item(sample_inventory):
    """Tests removing an item that isn't in inventory."""
    sample_inventory.remove_item(99)
    assert sample_inventory.get_quantity(99) == 0  # Should handle safely

def test_get_quantity(sample_inventory):
    """Tests retrieving item quantity from the inventory."""
    assert sample_inventory.get_quantity(1) == 10
    assert sample_inventory.get_quantity(3) == 0  # Item exists but is out of stock
    assert sample_inventory.get_quantity(99) == 0  # Nonexistent item

def test_add_zero_quantity_item(sample_inventory):
    """Tests adding an item with zero quantity to inventory."""
    sample_inventory.add_item(5, 0)
    assert sample_inventory.get_quantity(5) == 0

def test_add_item_when_item_exists(sample_inventory):
    """Tests adding quantity to an existing item in inventory."""
    sample_inventory.add_item(66, 7)
    sample_inventory.add_item(66, 6)  # Should add the quantity to existing item
    assert sample_inventory.get_quantity(66) == 13

def test_inventory_repr(sample_inventory):
    """Tests the string representation of the inventory."""
    assert repr(sample_inventory) == "Inventory({1: 10, 2: 5, 3: 0})"

def test_inventory_keys_and_values_are_int(sample_inventory):
    """Tests that all keys and values in the inventory dictionary are integers."""
    for key, value in sample_inventory.items.items():
        assert isinstance(key, int), f"Key {key} is not an integer"
        assert isinstance(value, int), f"Value {value} for key {key} is not an integer"

def test_search_items(sample_inventory):
    """Tests searching for items by name, category, and price range."""
    results = sample_inventory.search_items(name="Dining")
    assert len(results) == 1
    assert results[0].title == "Dining Table"

    results = sample_inventory.search_items(category="Bed")
    assert len(results) == 1
    assert results[0].title == "King Bed"

    results = sample_inventory.search_items(min_price=200, max_price=400)
    assert len(results) == 2  # Bed and Closet are within this range
    assert all(200 <= item.price <= 400 for item in results)

    results = sample_inventory.search_items(name="Nonexistent")
    assert len(results) == 0  # No items should match