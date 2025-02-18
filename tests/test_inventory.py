import pytest
from inventory import Inventory
from store_item import Table, Bed, Closet, Chair, Sofa


@pytest.fixture
def sample_inventory():
    """Creates a sample inventory with predefined stock levels."""
    inventory = Inventory()
    inventory.add_item(1, 10)  # Table
    inventory.add_item(2, 5)  # Bed
    inventory.add_item(3, 0)  # Closet (out of stock but still in inventory)
    return inventory


def test_add_item(sample_inventory):
    """Tests adding a new item to the inventory."""
    sample_inventory.add_item(4, 7)  # Add a new Chair
    assert sample_inventory.get_quantity(4) == 7


def test_update_quantity(sample_inventory):
    """Tests updating the quantity of an existing item."""
    sample_inventory.update_quantity(1, 15)
    assert sample_inventory.get_quantity(1) == 15


def test_remove_item(sample_inventory):
    """Tests removing an item from the inventory."""
    sample_inventory.remove_item(2)
    assert sample_inventory.get_quantity(2) == 0  # Should return 0 since item no longer exists


def test_get_quantity(sample_inventory):
    """Tests retrieving item quantity from the inventory."""
    assert sample_inventory.get_quantity(1) == 10
    assert sample_inventory.get_quantity(3) == 0  # Item exists but is out of stock
    assert sample_inventory.get_quantity(99) == 0  # Nonexistent item


def test_remove_nonexistent_item(sample_inventory):
    """Tests removing an item that isn't in inventory."""
    sample_inventory.remove_item(99)
    assert sample_inventory.get_quantity(99) == 0


def test_update_quantity_below_zero(sample_inventory):
    """Tests updating an item's quantity to a negative value."""
    sample_inventory.update_quantity(1, -5)
    assert sample_inventory.get_quantity(1) == -5  # Currently allows negative values, might need validation


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



# More tests are needed for the search!
