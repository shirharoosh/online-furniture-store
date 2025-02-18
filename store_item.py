from abc import ABC, abstractmethod


class StoreItem(ABC):
    """
    Abstract base class representing an item in the store.
    """

    def __init__(self, item_id: int, title: str, price: float, height: int, width: int, weight: float, description: str):
        self._item_id = item_id
        self._title = title
        self._price = price
        self._height = height
        self._width = width
        self._weight = weight
        self._description = description

    @property
    def item_id(self) -> int:
        return self._item_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def price(self) -> float:
        return self._price

    @property
    def description(self) -> str:
        return self._description

    def get_description(self) -> str:
        return self._description

    def apply_discount(self, discount: float) -> float:
        return self._price * (1 - discount)

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self._item_id}, title='{self._title}', price=${self._price:.2f})"


class Table(StoreItem):
    pass


class Bed(StoreItem):
    def __init__(self, *args, pillow_count: int, **kwargs):
        super().__init__(*args, **kwargs)
        self._pillow_count = pillow_count

    def __repr__(self):
        return super().__repr__() + f", pillow_count={self._pillow_count}"


class Closet(StoreItem):
    def __init__(self, *args, with_mirror: bool, **kwargs):
        super().__init__(*args, **kwargs)
        self._with_mirror = with_mirror

    def __repr__(self):
        return super().__repr__() + f", with_mirror={self._with_mirror}"


class Chair(StoreItem):
    def __init__(self, *args, material: str, **kwargs):
        super().__init__(*args, **kwargs)
        self._material = material

    def __repr__(self):
        return super().__repr__() + f", material='{self._material}'"


class Sofa(StoreItem):
    def __init__(self, *args, seating_capacity: int, **kwargs):
        super().__init__(*args, **kwargs)
        self._seating_capacity = seating_capacity

    def __repr__(self):
        return super().__repr__() + f", seating_capacity={self._seating_capacity}"
