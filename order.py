class Order:
    def __init__(self, user: User, items: list, total_price: float, status: str):
        self.user = user
        self.items = items
        self.total_price = total_price
        self.status = status

    def update_status(self, new_status: str):
        self.status = new_status