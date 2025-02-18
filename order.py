class Order:
    """
    Class representing a user's order.
    Stores user information, items purchased, total price, and order status.
    """

    def __init__(self, user, items: list, total_price: float, status: str = "pending"):
        self._user = user
        self._items = items  # Could be a list of CartItem objects or similar.
        self._total_price = total_price
        self._status = status

    @property
    def user(self):
        """Getter for the user associated with the order."""
        return self._user

    @property
    def items(self):
        """Getter for the list of items in the order."""
        return self._items

    @property
    def total_price(self) -> float:
        """Getter for the total price of the order."""
        return self._total_price

    @property
    def status(self) -> str:
        """Getter for the order status."""
        return self._status

    def update_status(self, new_status: str) -> None:
        """
        Updates the order status (e.g., pending, shipped, delivered).
        """
        self._status = new_status

    def __repr__(self) -> str:
        return (f"Order(user={self._user}, total_price=${self._total_price:.2f}, "
                f"status='{self._status}')")
