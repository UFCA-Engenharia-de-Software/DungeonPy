from domain.item import Item
from domain.entity import Entity


class ConsumableItem(Item):
    """
    A Consumable Item is responsible for recovering the entity's life or mana in the game.

    Attributes:
        recovered_value (int): The amount to be restored.
        recovery_type (str): What is restored — "life" (default) or "mana".
    """

    VALID_RECOVERY_TYPES = ("life", "mana")

    def __init__(
        self,
        name: str,
        description: str,
        weight: float,
        recovered_value: int,
        recovery_type: str = "life",
    ):
        super().__init__(name, description, weight)
        self.recovered_value = recovered_value
        self.recovery_type = recovery_type

    @property
    def recovered_value(self):
        return self._recovered_value

    @recovered_value.setter
    def recovered_value(self, value):
        if not isinstance(value, int):
            raise TypeError("Recovered Value needs to be a whole number.")

        if value <= 0:
            raise ValueError("Recovered Value Must be greater than 0")

        self._recovered_value = value

    @property
    def recovery_type(self):
        return self._recovery_type

    @recovery_type.setter
    def recovery_type(self, value):
        if value not in self.VALID_RECOVERY_TYPES:
            raise ValueError(
                f"recovery_type must be one of {self.VALID_RECOVERY_TYPES}, got '{value}'."
            )
        self._recovery_type = value

    def use(self, target: Entity) -> None:
        if self.recovery_type == "mana":
            if not hasattr(target, "current_mana"):
                raise TypeError(f"{target.name} não possui mana para restaurar.")
            target.current_mana += self.recovered_value
        else:
            target.heal_life(self.recovered_value)
