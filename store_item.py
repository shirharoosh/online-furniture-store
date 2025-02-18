from abc import ABC, abstractmethod


class StoreItem(ABC):
    """
    Abstract base class representing an item in the store.
    This enforces that all furniture items must be implemented as a subclass.
    """

    def __init__(self, item_id: int, title: str, price: float, quantity: int,
                 height: int, width: int, weight: float, description: str):
        self._item_id = item_id
        self._title = title
        self._price = price
        self._quantity = quantity
        self._height = height
        self._width = width
        self._weight = weight
        self._description = description

    @property
    def item_id(self) -> int:
        """Getter for the item ID."""
        return self._item_id

    @property
    def title(self) -> str:
        """Getter for the item title."""
        return self._title

    @property
    def price(self) -> float:
        """Getter for the item price."""
        return self._price

    @property
    def quantity(self) -> int:
        """Getter for the item quantity."""
        return self._quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        """Setter for the item quantity."""
        self._quantity = value

    @property
    def description(self) -> str:
        """Getter for the item description."""
        return self._description

    def get_description(self) -> str:
        """
        Returns the description of the item.
        """
        return self._description

    def apply_discount(self, discount: float) -> float:
        """
        Applies a discount to the item price and returns the discounted price.
        """
        return self._price * (1 - discount)

    def check_availability(self) -> bool:
        """
        Checks if the item is available based on its quantity.
        """
        return self._quantity > 0


class Table(StoreItem):
    """
    Represents a Table item.
    Inherits all methods from StoreItem.
    """
    pass


class Bed(StoreItem):
    """
    Represents a Bed item with an additional attribute for pillow count.
    """

    def __init__(self, *args, pillow_count: int, **kwargs):
        super().__init__(*args, **kwargs)
        self._pillow_count = pillow_count

    @property
    def pillow_count(self) -> int:
        """Getter for the pillow count."""
        return self._pillow_count


class Closet(StoreItem):
    """
    Represents a Closet item with an attribute indicating if it has a mirror.
    """

    def __init__(self, *args, with_mirror: bool, **kwargs):
        super().__init__(*args, **kwargs)
        self._with_mirror = with_mirror

    @property
    def with_mirror(self) -> bool:
        """Getter for the mirror presence flag."""
        return self._with_mirror


class Chair(StoreItem):
    """
    Represents a Chair item.
    Added a new attribute 'material' to indicate the chair's material.
    """

    def __init__(self, *args, material: str, **kwargs):
        super().__init__(*args, **kwargs)
        self._material = material

    @property
    def material(self) -> str:
        """Getter for the chair material."""
        return self._material


class Sofa(StoreItem):
    """
    Represents a Sofa item.
    Added a new attribute 'seating_capacity' to denote how many people it can seat.
    """

    def __init__(self, *args, seating_capacity: int, **kwargs):
        super().__init__(*args, **kwargs)
        self._seating_capacity = seating_capacity

    @property
    def seating_capacity(self) -> int:
        """Getter for the sofa's seating capacity."""
        return self._seating_capacity
