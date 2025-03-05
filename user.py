import bcrypt
from order import Order
from typing import List, Union

class User:
    """
    Class representing a user of the online furniture store.

    Handles authentication, profile management and order history.
    """

    def __init__(self, username: str, full_name: str, email: str,
                 password: str, address: str, phone_number: str):
        """
        Initializes a new User instance.

        Args:
            username (str): The unique username of the user.
            full_name (str): The full name of the user.
            email (str): The user's email address.
            password (str): The plain-text password (hashed internally).
            address (str): The user's physical address.
            phone_number (str): The user's phone number.
        """
        self._username = username
        self._full_name = full_name
        self._email = email
        self._address = address
        self._phone_number = phone_number
        self._password_hash = self._hash_password(password)
        self._is_logged = False
        self._order_hist = []  # List of Order objects representing the user's purchase history

    def _hash_password(self, password: str) -> bytes:
        """
        Hashes the password using bcrypt.

        Args:
            password (str): The plain-text password.

        Returns:
            bytes: The hashed password.
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def verify_password(self, password: str) -> bool:
        """
        Verifies that the provided password matches the stored hash password.

        Args:
            password (str): The plain-text password to check.

        Returns:
            bool: True if the password is correct, False otherwise.
        """
        return bcrypt.checkpw(password.encode('utf-8'), self._password_hash)

    def sign_up(self) -> str:
        """
        Simulates the user sign-up process.
        Note: This does not actually store the user in a database.

        Returns:
            str: Confirmation message indicating successful sign-up.
        """
        # Here you would normally save the user to a database.
        return f"User '{self._username}' signed up successfully."

    def login(self, email: str, password: str) -> str:
        """
        Simulates user login by checking credentials.

        Args:
            email (str): The user's email address.
            password (str): The user's password.

        Returns:
            str: A message indicating success or failure.
        """
        if self._email == email and self.verify_password(password):
            self._is_logged = True
            return f"User '{self._username}' logged in successfully."
        else:
            return "Invalid email or password."

    def manage_profile(self, full_name: str = None, address: str = None,
                       phone_number: str = None) -> str:
        """
        Updates the user's profile information.

        Args:
            full_name (str, optional): The updated full name.
            address (str, optional): The updated address.
            phone_number (str, optional): The updated phone number.

        Returns:
            str: A message indicating the profile update status.

        Raises:
            ValueError: If the user is not logged in.
        """
        if not self._is_logged:
            return "You must log in to manage your profile."
        if full_name:
            self._full_name = full_name
        if address:
            self._address = address
        if phone_number:
            self._phone_number = phone_number
        return f"Profile for '{self._username}' updated successfully."

    def view_order_history(self) -> Union[List[Order], str]:
        """
        Retrieves the user's order history.

        Returns:
            list: A list of past orders.

        Raises:
            ValueError: If the user is not logged in.
        """
        if not self._is_logged:
            return "You must log in to view your order history."
        if not self._order_hist:
            return "No orders found in your history."
        return self._order_hist # Returns a list of Order objects

    def add_order(self, order) -> None:
        """
        Adds an order to the user's order history.

        Args:
            order (Order): The order to be added.
        """
        self._order_hist.append(order)

    @property
    def username(self) -> str:
        """
        A getter for user's username.

        Returns:
            str: The username of the user.
        """
        return self._username

    @property
    def email(self) -> str:
        """
        A getter for the user's email.

        Returns:
            str: The email address of the user.
        """
        return self._email

    @property
    def full_name(self) -> str:
        """
        A getter for the user's full name.

        Returns:
            str: The full name of the user.
        """
        return self._full_name

    def __repr__(self) -> str:
        """
        Returns a string representation of the user.

        Returns:
            str: A formatted string with the username, email, and full name.
        """
        return f"User(username='{self._username}', email='{self._email}', full_name='{self._full_name}')"
