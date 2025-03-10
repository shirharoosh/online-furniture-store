from abc import ABC, abstractmethod
from typing import Any

class StoreItem(ABC):
    """
    Abstract base class representing an item in the store.

    Attributes:
        _item_id (int): Unique identifier for the item.
        _title (str): The name/title of the item.
        _price (float): The price of the item.
        _height (int): The height of the item (in cm).
        _width (int): The width of the item (in cm).
        _weight (float): The weight of the item (in kg).
        _description (str): A textual description of the item.
    """

    def __init__(self, item_id: int, title: str, price: float, height: int, width: int, weight: float, description: str):
        """
        Initializes a StoreItem instance.

        Args:
            item_id (int): Unique identifier for the item.
            title (str): The name/title of the item.
            price (float): The price of the item.
            height (int): The height of the item (in cm).
            width (int): The width of the item (in cm).
            weight (float): The weight of the item (in kg).
            description (str): A textual description of the item.
        """
        self._item_id = item_id
        self._title = title
        self._price = price
        self._height = height
        self._width = width
        self._weight = weight
        self._description = description

    @property
    def item_id(self) -> int:
        """
        Returns the unique item ID.

        Returns:
            int: The item ID.
        """
        return self._item_id

    @property
    def title(self) -> str:
        """
        Returns the title of the item.

        Returns:
            str: The item's title.
        """
        return self._title

    @property
    def price(self) -> float:
        """
        Returns the price of the item.

        Returns:
            float: The item's price.
        """
        return self._price

    @property
    def description(self) -> str:
        """
        Returns the description of the item.

        Returns:
            str: The item's description.
        """
        return self._description

    @abstractmethod
    def get_description(self) -> str:
        """
        Abstract method to be implemented in subclasses.

        Returns:
            a detailed description of the store item.
        """
        pass

    def apply_discount(self, discount: float) -> float:
        """
        Applies a discount to the item's price.

        Args:
            discount (float): Discount percentage (e.g., 0.10 for 10%).

        Returns:
            float: The discounted price.

        Raises:
            ValueError: If the discount is not between 0 and 1.
        """
        if not (0 <= discount <= 1):
            raise ValueError("Discount must be between 0 and 1.")
        return self._price * (1 - discount)

    def __repr__(self) -> str:
        """
        Returns a string representation of the item.

        Returns:
            str: A formatted string with the item's details.
        """
        return f"{self.__class__.__name__}(id={self._item_id}, title='{self._title}', price=${self._price:.2f})"


class Table(StoreItem):
    """
    Represents a table in the store.
    """
    def get_description(self) -> str:
        return f"{self.title}: A sturdy table priced at ${self.price:.2f}. {self.description}"

class Bed(StoreItem):
    """
    Represents a bed in the store.

    Attributes:
        _pillow_count (int): Number of pillows included with the bed.
    """
    def __init__(self, *args: Any, pillow_count: int, **kwargs: Any):
        """
        Initializes a Bed instance.

        Args:
            *args: Positional arguments for StoreItem.
            pillow_count (int): Number of pillows included.
            **kwargs: Keyword arguments for StoreItem.
        """
        super().__init__(*args, **kwargs)
        self._pillow_count = pillow_count

    def get_description(self) -> str:
        return f"{self.title}: A comfortable bed with {self._pillow_count} pillows, priced at ${self.price:.2f}. {self.description}"

    def __repr__(self) -> str:
        """
        Returns a string representation of the bed.

        Returns:
            str: A formatted string with the bed's details.
        """
        return super().__repr__() + f", pillow_count={self._pillow_count}"


class Closet(StoreItem):
    """
    Represents a closet in the store.

    Attributes:
        _with_mirror (bool): Indicates whether the closet has a mirror.
    """
    def __init__(self, *args: Any, with_mirror: bool, **kwargs: Any):
        """
        Initializes a Closet instance.

        Args:
            *args: Positional arguments for StoreItem.
            with_mirror (bool): Indicates if the closet has a mirror.
            **kwargs: Keyword arguments for StoreItem.
        """
        super().__init__(*args, **kwargs)
        self._with_mirror = with_mirror

    def get_description(self) -> str:
        mirror_text = "with a mirror" if self._with_mirror else "without a mirror"
        return f"{self.title}: A spacious closet {mirror_text}, priced at ${self.price:.2f}. {self.description}"

    def __repr__(self) -> str:
        """
        Returns a string representation of the closet.

        Returns:
            str: A formatted string with the closet's details.
        """
        return super().__repr__() + f", with_mirror={self._with_mirror}"


class Chair(StoreItem):
    """
    Represents a chair in the store.

    Attributes:
        _material (str): The material of the chair.
    """
    def __init__(self, *args: Any, material: str, **kwargs: Any):
        """
        Initializes a Chair instance.

        Args:
            *args: Positional arguments for StoreItem.
            material (str): The material of the chair.
            **kwargs: Keyword arguments for StoreItem.
        """
        super().__init__(*args, **kwargs)
        self._material = material

    def get_description(self) -> str:
        return f"{self.title}: A {self._material} chair, priced at ${self.price:.2f}. {self.description}"
    
    def __repr__(self) -> str:
        """
        Returns a string representation of the chair.

        Returns:
            str: A formatted string with the chair's details.
        """
        return super().__repr__() + f", material='{self._material}'"


class Sofa(StoreItem):
    """
    Represents a sofa in the store.

    Attributes:
        _seating_capacity (int): Number of people the sofa can accommodate.
    """
    def __init__(self, *args: Any, seating_capacity: int, **kwargs: Any):
        """
        Initializes a Sofa instance.

        Args:
            *args: Positional arguments for StoreItem.
            seating_capacity (int): Number of people the sofa can seat.
            **kwargs: Keyword arguments for StoreItem.
        """
        super().__init__(*args, **kwargs)
        self._seating_capacity = seating_capacity

    def get_description(self) -> str:
        return f"{self.title}: A spacious sofa with seating for {self._seating_capacity} people, priced at ${self.price:.2f}. {self.description}"

    def __repr__(self) -> str:
        """
        Returns a string representation of the sofa.

        Returns:
            str: A formatted string with the sofa's details.
        """
        return super().__repr__() + f", seating_capacity={self._seating_capacity}"
    

class StoreItemFactory:
    """
    Factory class for creating different types of furniture items dynamically.
    """
    _item_classes = {
        "Table": Table,
        "Bed": Bed,
        "Closet": Closet,
        "Chair": Chair,
        "Sofa": Sofa
    }
    
    @staticmethod
    def create_item(item_type: str, *args, **kwargs) -> StoreItem:
        """
        Creates a StoreItem instance based on the provided item type.

        Args:
            item_type (str): The type of furniture (e.g., "Table", "Chair").
            *args: Positional arguments for the item's constructor.
            **kwargs: Keyword arguments for the item's constructor.

        Returns:
            StoreItem: An instance of the requested furniture type.

        Raises:
            ValueError: If the item_type is not recognized.
        """
        if item_type not in StoreItemFactory._item_classes:
            raise ValueError(f"Invalid item type: {item_type}")
        
        return StoreItemFactory._item_classes[item_type](*args, **kwargs)