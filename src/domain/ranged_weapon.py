from __future__ import annotations

import random
from typing import TYPE_CHECKING, cast

from domain.element import Element
from domain.weapon import Weapon

if TYPE_CHECKING:
    from domain.archer import Archer
    from domain.entity import Entity
    from domain.hero import Hero


class RangedWeapon(Weapon):
    """Represents a ranged weapon used by heroes.

    Ranged weapons require ammunition to perform attacks.
    They extend the base Weapon behavior by validating
    and consuming ammunition before dealing damage.

    Attributes:
        ammo_required (int): Amount of ammunition consumed per attack.
        hit_probability (int): Base chance to hit when not aiming (0 to 100).
    """

    def __init__(
        self,
        name: str,
        base_damage: int,
        ammo_required: int,
        hit_probability: int = 70,
        description: str = "",
        weight: float = 1.0,
        element: Element = Element.NEUTRAL,
    ):
        super().__init__(name, base_damage, description, weight, element)
        self.ammo_required = ammo_required
        self.hit_probability = hit_probability

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

    @property
    def hit_probability(self) -> int:
        return self._hit_probability

    @hit_probability.setter
    def hit_probability(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("hit_probability must be an integer.")
        if value < 0 or value > 100:
            raise ValueError("hit_probability must be between 0 and 100.")
        self._hit_probability = value

    def attack(self, user: Hero, target: Entity) -> None:
        archer_user = cast("Archer", user)

        if archer_user.current_ammo < self._ammo_required:
            raise ValueError("Not enough ammunition.")

        archer_user.current_ammo -= self._ammo_required

        if archer_user.is_aiming:
            super().attack(archer_user, target)
            return

        if random.randint(1, 100) <= self._hit_probability:
            super().attack(archer_user, target)
