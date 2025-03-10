import pytest
from shopping_cart import ShoppingCart
from inventory import Inventory
from store_item import Table, Chair, Closet

@pytest.fixture
def setup_cart():
    """
    Fixture to create an inventory and shopping cart for tests.
    Ensures Inventory is reset before each test.
    """
    inventory = Inventory()

    # Reset inventory before each test
    inventory._items.clear()
    inventory.set_catalog(None)
    
    catalog = {
        1: Table(1, "Table", 200, 120, 75, 30, "Some table"),
        2: Chair(102, "Office Chair", 80, 100, 50, 10, "An ergonomic office chair.", material="Leather"),
        3: Closet(3, "Closet", 800, 180, 220, 80, "Some closet", with_mirror=True)
    }
    inventory.set_catalog(catalog)
    inventory.add_item(1, 5)  # 5 Tables
    inventory.add_item(2, 3)  # 3 Beds
    inventory.add_item(3, 2)  # 2 Closets

    cart = ShoppingCart(inventory)
    return cart

def test_add_item(setup_cart):
    """
    Test adding an item to cart.
    """
    cart = setup_cart
    cart.add_furniture(1, 2)  # Adding 2 tables
    assert cart._cart_items[1] == 2
    assert cart._total_price == 400 #2 * 200

def test_add_nonexistent_item(setup_cart, capsys):
    """Tests trying to add an item that does not exist in inventory."""
    cart = setup_cart
    cart.add_furniture(99, 1)  # Item ID 99 does not exist
    captured = capsys.readouterr()
    assert "Item not found in inventory." in captured.out

def test_add_exceeding_stock(setup_cart, capsys):
    """Tests adding more items than available stock."""
    cart = setup_cart
    cart.add_furniture(1, 10)  # Only 5 tables in stock
    captured = capsys.readouterr()
    assert "Not enough stock available. Only 5 left." in captured.out

def test_remove_item(setup_cart):
    """
    Test removing an item from cart.
    """
    cart = setup_cart
    cart.add_furniture(2, 1)  # Add 1 bed
    cart.remove_furniture(2, 1)  # Remove 1 bed
    assert 2 not in cart._cart_items
    assert cart._total_price == 0

def test_remove_nonexistent_item(setup_cart, capsys):
    """Tests removing an item that is not in the cart."""
    cart = setup_cart
    cart.remove_furniture(99, 1)  # Item ID 99 was never added
    captured = capsys.readouterr()
    assert "Item not found in cart." in captured.out

def test_remove_more_than_in_cart(setup_cart, capsys):
    """Tests removing more items than are in the cart."""
    cart = setup_cart
    cart.add_furniture(1, 2)  # Add 2 tables
    cart.remove_furniture(1, 5)  # Attempt to remove 5
    captured = capsys.readouterr()
    assert "Not enough quantity in cart to remove." in captured.out

def test_apply_discount(setup_cart):
    """
    Test applying a discount to cart.
    """
    cart = setup_cart
    cart.add_furniture(1, 2)  # Total = 400
    old_price = cart._total_price
    print(old_price)
    cart.apply_discount(10)  # Apply 10% discount
    assert cart._total_price == 360
    assert old_price - cart._total_price == 40

def test_apply_invalid_discount(setup_cart, capsys):
    """Tests applying an invalid discount (too high or negative)."""
    cart = setup_cart
    cart.add_furniture(1, 2)  # Total = 400
    cart.apply_discount(150)  # Invalid (over 100%)
    captured = capsys.readouterr()
    assert "Invalid discount percentage." in captured.out

    cart.apply_discount(-10)  # Invalid (negative)
    captured = capsys.readouterr()
    assert "Invalid discount percentage." in captured.out

def test_show_price(setup_cart, capsys):
    """
    Test the total price display method.
    """

    cart = setup_cart
    cart.add_furniture(1, 2) #2 tables - 400$
    cart.add_furniture(3, 1) #1 closet - 800$
    cart.show_total_price()

    captured = capsys.readouterr()
    assert "Total price for your cart: $1200.00" in captured.out

def test_cart_representation(setup_cart):
    """Tests string representation of a shopping cart."""
    cart = setup_cart
    cart.add_furniture(1, 2)
    expected_repr = "ShoppingCart(items={1: 2}, total_price=$400.00)"
    assert repr(cart) == expected_repr