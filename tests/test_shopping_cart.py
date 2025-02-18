import pytest
from shopping_cart import ShoppingCart
from inventory import Inventory
from store_item import StoreItem

@pytest.fixture
def setup_cart():
    """
    Fixture to create an inventory and shopping cart for tests.
    """
    inventory = Inventory()
    inventory.add_item(StoreItem(
        item_id=1, title="Table", price=200, quantity=5, width=120, height=75, weight=30, description="Some table"
    ))
    inventory.add_item(StoreItem(
        item_id=2, title="Bed", price=500, quantity=3, width=200, height=60, weight=50, description="Some bed"
    ))
    inventory.add_item(StoreItem(
        item_id=3, title="Closet", price=800, quantity=2, width=180, height=220, weight=80, description="Some closet"
    ))
    
    cart = ShoppingCart(inventory)
    return cart

def test_add_item(setup_cart):
    """
    Test adding an item to cart.
    """
    cart = setup_cart
    cart.add_item(1, 2) #2 tables
    assert cart.cart_items[1] == 2
    assert cart.total_price == 400 #2 * 200

def test_remove_item(setup_cart):
    """
    Test removing an item from cart.
    """
    cart = setup_cart
    cart.add_item(2, 1) # 1 bed
    cart.remove_item(2, 1)
    assert 2 not in cart.cart_items
    assert cart.total_price == 0

def test_apply_discount(setup_cart):
    """
    Test applying a discount to cart.
    """
    cart = setup_cart
    cart.add_item(1, 2) #total should be 400$
    cart.apply_discount(10) #apply 10% discount
    assert cart.discount == 40 #10% of 400
    assert cart.total_price - cart.discount == 360

def test_show_price(setup_cart, capsys):
    """
    Test the total price display method.
    """

    cart = setup_cart
    cart.add_item(1, 2) #2 tables - 400$
    cart.add_item(3, 1) #1 closet - 800$
    cart.show_price()

    captured = capsys.readouterr()
    assert "Total price for your cart before discounts: $1200.00" in captured.out

def test_view_cart(setup_cart, capsys):
    cart = setup_cart
    cart.add_item(1, 1) # 1 table
    cart.add_item(2, 1) # 1 bed
    cart.add_item(3, 1) # 1 closet

    cart.view_cart()

    captured = capsys.readouterr()

    assert "Shopping Cart:" in captured.out
    assert "- Table: 1 @ $200.00 each" in captured.out
    assert "- Bed: 1 @ $500.00 each" in captured.out
    assert "- Closet: 1 @ $800.00 each" in captured.out
    assert "Total Price: $1500.00" in captured.out
