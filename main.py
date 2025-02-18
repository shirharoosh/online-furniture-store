from inventory import Inventory
from shopping_cart import ShoppingCart
from user import User
from order import Order
from user_order_dic import UserOrderDictionary
from store_item import Table, Chair, Sofa

# Global shared resources (Simulated database)
global_inventory = Inventory()  # Shared inventory across users
global_user_orders = UserOrderDictionary()  # Stores orders for all users
user_accounts = {}  # Simulated user database (email -> User object)
shopping_carts = {}  # Stores active carts per user

# Predefined catalog of furniture items (will be added to inventory)
catalog = {
    101: Table(101, "Dining Table", 250, 75, 150, 30, "A sturdy wooden dining table."),
    102: Chair(102, "Office Chair", 80, 100, 50, 10, "An ergonomic office chair.", material="Leather"),
    103: Sofa(103, "Luxury Sofa", 500, 40, 200, 50, "A comfortable luxury sofa.", seating_capacity=3)
}


def initialize_inventory():
    """Populates the inventory with initial stock using predefined catalog items."""
    for item_id in catalog:
        quantity = 10  # Set initial stock for each item
        global_inventory.add_item(item_id, quantity)
    print("Inventory initialized!")


def initialize_users():
    """Creates three pre-generated users to allow easy login."""
    pre_generated_users = [
        ("alice@example.com", "Alice123", "Alice", "Alice Wonderland", "456 Elm St", "123456789"),
        ("bob@example.com", "Bob456", "Bob", "Bob Builder", "789 Oak St", "987654321"),
        ("charlie@example.com", "Charlie789", "Charlie", "Charlie Brown", "321 Pine St", "555555555")
    ]

    for email, password, username, full_name, address, phone_number in pre_generated_users:
        new_user = User(username, full_name, email, password, address, phone_number)
        user_accounts[email] = new_user
        shopping_carts[email] = ShoppingCart(global_inventory)

    print("Users initialized! You can log in with:")
    for email, password, username, _, _, _ in pre_generated_users:
        print(f"Username: {username}, Email: {email}, Password: {password}")


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
    cart = shopping_carts[user.email]  # Retrieve the user's cart

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
    """Main function to initialize inventory, create test users, and handle user login/signup."""
    initialize_inventory()
    initialize_users()  # Generate 3 users for easy login

    while True:
        print("\nWelcome to the Online Furniture Store!")
        print("1. Log In")
        print("2. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            user = log_in()
            if user:
                user_interface(user)

        elif choice == "2":
            print("Exiting the application. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
