class StoreItem:
    def __init__(self, item_id: int, title: str, price: float, quantity: int, height: int,
                 width: int, weight: float, description: str):
        self.item_id = item_id
        self.title = title
        self.price = price
        self.quantity = quantity
        self.height = height
        self.width = width
        self.weight = weight
        self.description = description

    def get_description(self) -> str:
        return self.description

    def apply_discount(self, discount: float) -> float:
        return self.price * (1 - discount)

    def check_availability(self) -> bool:
        return self.quantity > 0

class Table(StoreItem):
    pass

class Bed(StoreItem):
    def __init__(self, *args, pillow_count: int):
        super().__init__(*args)
        self.pillow_count = pillow_count

class Closet(StoreItem):
    def __init__(self, *args, with_mirror: bool):
        super().__init__(*args)
        self.with_mirror = with_mirror

