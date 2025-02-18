import bcrypt


class User:
    """
    Class representing a user of the online furniture store.
    Handles authentication and profile management.
    """

    def __init__(self, username: str, full_name: str, email: str,
                 password: str, address: str, phone_number: str):
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
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def verify_password(self, password: str) -> bool:
        """
        Verifies that the provided password matches the stored hash.
        """
        return bcrypt.checkpw(password.encode('utf-8'), self._password_hash)

    def sign_up(self) -> str:
        """
        Simulates the user sign-up process.
        """
        # Here you would normally save the user to a database.
        return f"User '{self._username}' signed up successfully."

    def login(self, email: str, password: str) -> str:
        """
        Simulates user login.
        """
        if self._email == email and self.verify_password(password):
            self._is_logged = True
            return f"User '{self._username}' logged in successfully."
        else:
            return "Invalid email or password."

    def manage_profile(self, full_name: str = None, address: str = None,
                       phone_number: str = None) -> str:
        """
        Allows the user to update profile information.
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

    def view_order_history(self):
        """
        Returns the user's order history.
        """
        if not self._is_logged:
            return "You must log in to view your order history."
        if not self._order_hist:
            return "No orders found in your history."
        return self._order_hist

    def add_order(self, order) -> None:
        """
        Adds an order to the user's order history.
        """
        self._order_hist.append(order)

    @property
    def username(self) -> str:
        """Getter for the username."""
        return self._username

    @property
    def email(self) -> str:
        """Getter for the email."""
        return self._email

    @property
    def full_name(self) -> str:
        """Getter for the full name."""
        return self._full_name

    def __repr__(self) -> str:
        return f"User(username='{self._username}', email='{self._email}', full_name='{self._full_name}')"
