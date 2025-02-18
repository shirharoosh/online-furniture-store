from inventory import Inventory
from shopping_cart import ShoppingCart
from user import User
from order import Order
from user_order_dic import UserOrderDictionary

# Global shared resources (Simulated database)
global_inventory = Inventory()  # Shared inventory across users
global_user_orders = UserOrderDictionary()  # Stores orders for all users
user_accounts = {}  # Simulated user database (email -> User object)
shopping_carts = {}  # Stores active carts per user


def initialize_inventory():
    """Populates the inventory with initial stock."""
    global_inventory.add_item(101, 10)  # 10 Dining Tables
    global_inventory.add_item(102, 15)  # 15 Office Chairs
    global_inventory.add_item(103, 5)  # 5 Sofas
    print("Inventory initialized!")


def sign_up():
    """Handles user sign-up using User.sign_up()."""
    print("\nSign Up")
    email = input("Enter email: ").strip()
    if email in user_accounts:
        print("User already exists. Please log in.")
        return None

    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    full_name = input("Enter full name: ").strip()
    address = input("Enter address: ").strip()
    phone_number = input("Enter phone number: ").strip()

    new_user = User(username, full_name, email, password, address, phone_number)
    print(new_user.sign_up())  # Use existing function

    user_accounts[email] = new_user
    shopping_carts[email] = ShoppingCart(global_inventory)  # Create a new cart for this user
    return new_user


def log_in():
    """Handles user login using User.login()."""
    print("\nLog In")
    email = input("Enter email: ").strip()
    if email not in user_accounts:
        print("User not found. Please sign up first.")
        return None

    password = input("Enter password: ").strip()
    user = user_accounts[email]
    login_result = user.login(email, password)

    if "logged in successfully" in login_result:
        print(login_result)
        return user
    else:
        print(login_result)
        return None


def user_interface(user):
    """Allows the user to interact with their shopping cart."""
    cart = shopping_carts[user.email]  # Retrieve or create the user's cart

    while True:
        print("\nShopping Cart Menu:")
        print("1. Add Item to Cart")
        print("2. Remove Item from Cart")
        print("3. View Cart")
        print("4. Show Total Price")
        print("5. Checkout")
        print("6. Log Out")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            item_id = int(input("Enter item ID: ").strip())
            quantity = int(input("Enter quantity: ").strip())
            cart.add_furniture(item_id, quantity)

        elif choice == "2":
            item_id = int(input("Enter item ID: ").strip())
            quantity = int(input("Enter quantity: ").strip())
            cart.remove_furniture(item_id, quantity)

        elif choice == "3":
            print(cart)

        elif choice == "4":
            cart.show_total_price()

        elif choice == "5":
            checkout(user, cart)

        elif choice == "6":
            print("Logging out...")
            break

        else:
            print("Invalid choice. Please try again.")


def checkout(user, cart):
    """
    Handles the checkout process:
    - Collects payment details.
    - Validates stock availability.
    - Processes payment (mocked).
    - Updates inventory and order history.
    """
    print("\n--- Checkout Process ---")
    if not cart._cart_items:
        print("Your cart is empty. Add items before checking out.")
        return

    # Collect user details
    shipping_address = input("Enter shipping address: ").strip() or user.address
    payment_method = input("Enter payment method (e.g., Credit Card, PayPal): ").strip()

    # Validate inventory availability before proceeding
    for item_id, quantity in cart._cart_items.items():
        if global_inventory.get_quantity(item_id) < quantity:
            print(f"Error: Not enough stock for item {item_id}. Remove items before proceeding.")
            return

    # Mock Payment Processing
    print(f"Processing payment of ${cart._total_price:.2f} using {payment_method}...")
    payment_successful = process_payment(cart._total_price, payment_method)

    if not payment_successful:
        print("Payment failed. Please try again.")
        return

    # Deduct purchased items from inventory
    for item_id, quantity in cart._cart_items.items():
        global_inventory.update_quantity(item_id, global_inventory.get_quantity(item_id) - quantity)

    # Create the order and update the user's order history
    order = Order(user, list(cart._cart_items.keys()), cart._total_price, status="Pending")
    #TODO - update the status through API
    global_user_orders.update(order)

    # Clear the shopping cart after a successful checkout
    shopping_carts[user.email] = ShoppingCart(global_inventory)

    print(f"\nOrder placed successfully for {user.username}!\nOrder Details: {order}")
    print("Thank you for shopping with us!\n")


def process_payment(amount, payment_method):
    """Mock payment processing."""
    print(f"Payment of ${amount:.2f} processed successfully with {payment_method}.")
    return True


def main():
    """Main function to initialize inventory and handle user login/signup."""
    initialize_inventory()

    while True:
        print("\nWelcome to the Online Furniture Store!")
        print("1. Log In")
        print("2. Sign Up")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            user = log_in()
            if user:
                user_interface(user)

        elif choice == "2":
            user = sign_up()
            if user:
                user_interface(user)

        elif choice == "3":
            print("Exiting the application. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
