from __future__ import annotations

from typing import TYPE_CHECKING

from domain.element import Element
from domain.weapon import Weapon

if TYPE_CHECKING:
    from domain.entity import Entity
    from domain.hero import Hero


class RangedWeapon(Weapon):
    """Represents a ranged weapon used by heroes.

    Ranged weapons require ammunition to perform attacks.
    They extend the base Weapon behavior by validating
    and consuming ammunition before dealing damage.

    Attributes:
        ammo_required (int): Amount of ammunition consumed per attack.
    """

    def __init__(
        self,
        name: str,
        base_damage: int,
        ammo_required: int,
        description: str = "",
        weight: float = 1.0,
        element: Element = Element.NEUTRAL,
    ):
        super().__init__(name, base_damage, description, weight, element)
        self.ammo_required = ammo_required

    @property
    def ammo_required(self) -> int:
        return self._ammo_required

    @ammo_required.setter
    def ammo_required(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("ammo_required must be an integer.")
        if value <= 0:
            raise ValueError("ammo_required must be greater than 0.")
        self._ammo_required = value

    def attack(self, user: Hero, target: Entity) -> None:
        if user.current_ammo < self._ammo_required:
            raise ValueError("Not enough ammunition.")

        user.current_ammo -= self._ammo_required
        super().attack(user, target)
