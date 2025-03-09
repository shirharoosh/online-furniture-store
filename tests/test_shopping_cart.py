import pytest
from shopping_cart import ShoppingCart
from inventory import Inventory
from store_item import Table, Chair, Closet

@pytest.fixture
def setup_cart():
    """
    Fixture to create an inventory and shopping cart for tests.
    """
    inventory = Inventory()
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

def test_remove_item(setup_cart):
    """
    Test removing an item from cart.
    """
    cart = setup_cart
    cart.add_furniture(2, 1)  # Add 1 bed
    cart.remove_furniture(2, 1)  # Remove 1 bed
    assert 2 not in cart._cart_items
    assert cart._total_price == 0

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

# TODO: adding view cart method to the ShoppingCart class
