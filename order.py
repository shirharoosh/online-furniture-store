from typing import List
from user import User
from store_item import StoreItem


class Order:
    """
    Class representing a user's order.
    
    Attributes:
        _user (User): The user who placed the order.
        _items (List[StoreItem]): The list of items purchased in the order.
        _total_price (float): The total cost of the order.
        _status (str): The current status of the order (default is "pending").
    """

    def __init__(self, user: User, items: List[StoreItem], total_price: float, status: str = "pending") -> None:
        """
        Initializes an Order instance.

        Args:
            user (User): The user who placed the order.
            items (List[StoreItem]): The list of items in the order.
            total_price (float): The total price of the order.
            status (str, optional): The status of the order (default is "pending").
        """
        self._user = user
        self._items = items  # a list of CartItem objects.
        self._total_price = total_price
        self._status = status

    @property
    def user(self) -> User:
        """
        Returns the user associated with the order.

        Returns:
            User: The user who placed the order.
        """
        return self._user

    @property
    def items(self) -> list[StoreItem]:
        """
        Returns the list of items in the order.

        Returns:
            List[StoreItem]: A list of StoreItem objects.
        """
        return self._items

    @property
    def total_price(self) -> float:
        """
        Returns the total price of the order.

        Returns:
            float: The total price of the order.
        """
        return self._total_price

    @property
    def status(self) -> str:
        """
        Returns the current status of the order.

        Returns:
            str: The status of the order (e.g., "pending", "shipped", "delivered").
        """
        return self._status

    def update_status(self, new_status: str) -> None:
        """
        Updates the status of the order.

        Args:
            new_status (str): The new status of the order (e.g., "shipped", "delivered").

        Returns:
            None
        """
        self._status = new_status

    def __repr__(self) -> str:
        """
        Returns a string representation of the order.

        Returns:
            str: A formatted string displaying order details.
        """
        return (f"Order(user={self._user}, total_price=${self._total_price:.2f}, "
                f"status='{self._status}')")
