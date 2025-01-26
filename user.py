import bcrypt

class User:
    def __init__(self, username, full_name, email, password, address, phone_number):
        self.username = username
        self.full_name = full_name
        self.email = email
        self.address = address
        self.phone_number = phone_number
        self.password_hash = self._hash_password(password)
        self.is_logged = False
        self.order_hist = []  # UserOrders list, mock with a simple list for now

    def _hash_password(self, password):
        """Hashes the password using bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def verify_password(self, password):
        """Verifies the provided password against the stored hash."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)

    def sign_up(self):
        """Simulate user sign-up process."""
        # Save user to a database (mock this process for now)
        return f"User '{self.username}' signed up successfully."

    def login(self, email, password):
        """Simulates user login."""
        if self.email == email and self.verify_password(password):
            self.is_logged = True
            return f"User '{self.username}' logged in successfully."
        else:
            return "Invalid email or password."

    def manage_profile(self, full_name=None, address=None, phone_number=None):
        """Allows the user to update their profile."""
        if not self.is_logged:
            return "You must log in to manage your profile."
        if full_name:
            self.full_name = full_name
        if address:
            self.address = address
        if phone_number:
            self.phone_number = phone_number
        return f"Profile for '{self.username}' updated successfully."

    def view_order_history(self):
        """Displays the user's order history."""
        if not self.is_logged:
            return "You must log in to view your order history."
        if not self.order_hist:
            return "No orders found in your history."
        return self.order_hist

    def __repr__(self):
        return f"User(username='{self.username}', email='{self.email}', full_name='{self.full_name}')"
