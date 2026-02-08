from typing import List, Optional

from domain.item import Item


class Inventory:
    """Represents an inventory that can store items with a capacity limit.

    The inventory manages a collection of items and enforces a maximum
    capacity based on the total weight of stored items.

    Attributes:
        items (List[Item]): List of items currently in the inventory.
        capacity (float): Maximum weight capacity of the inventory.
    """

    def __init__(self, capacity: float = 100.0):
        self.capacity = capacity
        self._items: List[Item] = []

    @property
    def items(self) -> List[Item]:
        return self._items.copy()

    @property
    def capacity(self) -> float:
        return self._capacity

    @capacity.setter
    def capacity(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("Capacity must be a number")
        if value <= 0:
            raise ValueError("Capacity must be positive")

        self._capacity = float(value)

    def calculate_current_weight(self) -> float:
        return sum(item.weight for item in self._items)

    def get_available_weight_capacity(self) -> float:
        return self.capacity - self.calculate_current_weight()

    def can_add_item(self, item: Item) -> bool:
        """Assumes item is a valid Item instance."""
        return item.weight <= self.get_available_weight_capacity()

    def add_item_to_inventory(self, item: Item) -> bool:
        if not isinstance(item, Item):
            raise TypeError("Only Item instances can be added to inventory")

        if not self.can_add_item(item):
            return False

        self._items.append(item)
        return True

    def remove_item_from_inventory(self, item: Item) -> bool:
        if item in self._items:
            self._items.remove(item)
            return True
        return False

    def find_item_by_name(self, item_name: str) -> Optional[Item]:
        for item in self._items:
            if item.name.lower() == item_name.lower():
                return item
        return None

    def remove_item_by_name(self, item_name: str) -> bool:
        item = self.find_item_by_name(item_name)
        if item:
            return self.remove_item_from_inventory(item)
        return False

    def get_items_summary(self) -> dict:
        return {
            "capacity": self.capacity,
            "current_weight": self.calculate_current_weight(),
            "available_capacity": self.get_available_weight_capacity(),
            "item_count": len(self._items),
            "items": [
                {"name": item.name, "weight": item.weight} for item in self._items
            ],
        }

    def list_all_items(self) -> List[str]:
        if self.is_empty():
            return ["Empty inventory"]

        summary = self.get_items_summary()
        result = []
        result.append(
            f"Capacity: {summary['current_weight']:.1f}/{summary['capacity']}"
        )
        result.append("Items:")

        for index, item_data in enumerate(summary["items"], 1):
            result.append(
                f"  {index}. {item_data['name']} (weight: {item_data['weight']})"
            )

        return result

    def clear_all_items_from_inventory(self) -> None:
        self._items.clear()

    def has_item(self, item_name: str) -> bool:
        return self.find_item_by_name(item_name) is not None

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        """Return the number of items in the inventory."""
        return len(self._items)

    def __str__(self) -> str:
        """Return a string representation of the inventory."""
        return "\n".join(self.list_all_items())
