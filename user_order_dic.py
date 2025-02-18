from order import Order


class UserOrderDictionary:
    """
    Maintains a dictionary mapping a user's username to a list of their orders.
    Uses an observer pattern: whenever a new order is created, calling update()
    automatically adds the order to the correct user's order history.
    """

    def __init__(self):
        # Dictionary: key = username (str), value = list of Order objects.
        self._user_orders = {}

    def update(self, order: Order) -> None:
        """
        Observer update method. Adds a new order to the dictionary and updates
        the corresponding user's order history.
        """
        username = order.user.username
        if username not in self._user_orders:
            self._user_orders[username] = []
        self._user_orders[username].append(order)
        # Also update the user's own order history.
        order.user.add_order(order)

    def get_orders_for_user(self, user) -> list:
        """
        Returns a list of orders associated with the given user.
        """
        return self._user_orders.get(user.username, [])
