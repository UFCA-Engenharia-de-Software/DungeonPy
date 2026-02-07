from abc import ABC, abstractmethod

from domain.mixins import DescriptionMixin


class Item(ABC, DescriptionMixin):
    """Abstract base class that represents an item in the game.

    Items are objects that can be collected, stored in inventories, and used
    by heroes during their adventure. This class defines the common interface
    and attributes for all item types in the game.

    Subclasses must implement the use() method to define specific behavior
    when the item is used.

    Attributes:
        name (str): The item's name.
        description (str): A textual description of the item.
        weight (float): The item's weight, affecting inventory capacity.
    """

    def __init__(self, name: str, description: str = "", weight: float = 1.0):
        self.name = name
        self.weight = weight
        self._description: str = description

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Item name must be a string")

        if len(value.strip()) == 0:
            raise ValueError("Item name cannot be empty")

        self._name = value.strip().title()

    @property
    def weight(self) -> float:
        return self._weight

    @weight.setter
    def weight(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("Item weight must be a number")

        if value <= 0:
            raise ValueError("Item weight must be positive")

        self._weight = float(value)

    def get_description(self) -> str:
        """Return the item's description or a default one."""
        if self._description:
            return self._description
        return f"{self.name} is an item weighing {self.weight} units."

    @abstractmethod
    def use(self, target) -> None:
        """Use the item on a target. Must be implemented by subclasses."""
        pass
