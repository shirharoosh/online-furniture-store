from order import Order
from user import User
from typing import Dict, List


class UserOrderDictionary:
    """
    Maintains a dictionary mapping a user's username to a list of their orders.

    Implements an observer pattern: whenever a new order is created, calling 'update()'
    automatically adds the order to the correct user's order history.
    """

    def __init__(self) -> None:
        """
        Initializes an empty dictionary to store user orders.

        The dictionary structure:
        - Key: str (username)
        - Value: List[Order] (list of the user's past orders)
        """
        self._user_orders: Dict[str, List[Order]] = {}

    def update(self, order: Order) -> None:
        """
        Adds a new order to the user's order history.

        Implements an observer update method. Adds a new order to the dictionary and updates
        the corresponding user's order history.

        Args:
            order (Order): The new order to be added.

        Returns:
            None
        """
        username: str = order.user.username
        if username not in self._user_orders:
            self._user_orders[username] = []
        self._user_orders[username].append(order)

        # Also update the user's own order history.
        order.user.add_order(order)

    def get_orders_for_user(self, user: User) -> list[Order]:
        """
        Retrieves the list of orders associated with the given user.

        Args:
            user (User): The user whose order history is being requested.

        Returns:
            List[Order]: A list of the user's past orders. If the user has no orders, returns an empty list.
        """
        return list(self._user_orders.get(user.username, []))

    def clear_user_orders(self, user: User) -> None:
        """
        Clears all orders associated with the given user, resetting their order list.

        Args:
            user (User): The user whose order history should be cleared.

        Returns:
            None
        """
        self._user_orders[user.username] = []
