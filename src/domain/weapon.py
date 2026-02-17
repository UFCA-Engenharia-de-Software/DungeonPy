from __future__ import annotations

from typing import TYPE_CHECKING

from domain.element import Element
from domain.entity import Entity
from domain.item import Item

if TYPE_CHECKING:
    from domain.hero import Hero


class Weapon(Item):
    """Represents an equippable weapon used by heroes and monsters.

    Weapons provide base damage and an elemental type that affect
    damage calculation through advantages and disadvantages.

    Attributes:
        base_damage (int): Fixed damage before user modifiers.
        element (Element): Element applied on strike.
    """

    def __init__(
        self,
        name: str,
        base_damage: int,
        description: str = "",
        weight: float = 1.0,
        element: Element = Element.NEUTRAL,
    ):
        super().__init__(name, description, weight)
        self.base_damage = base_damage
        self.element = element
        self._attacks = {
            "1": {"description": "Ataque Normal", "method": self.attack},
            "2": {"description": "Ataque Pesado", "method": self.heavy_attack},
        }

    @property
    def base_damage(self) -> int:
        return self._base_damage

    @base_damage.setter
    def base_damage(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("base_damage must be an integer")
        if value <= 0:
            raise ValueError("base_damage must be greater than 0")
        self._base_damage = value

    @property
    def element(self) -> Element:
        return self._element

    @element.setter
    def element(self, value: Element) -> None:
        if not isinstance(value, Element):
            raise TypeError("element must be a Element member. Example: Element.FIRE")
        self._element = value

    def get_attacks(self):
        return self._attacks

    def attack(self, user: Hero, target: Entity) -> None:
        damage = self.base_damage + user.attack
        target.damage_received(damage, self.element)

    def heavy_attack(self, user: Hero, target: Entity) -> None:
        damage = int((self.base_damage + user.attack) * 2.0)
        target.damage_received(damage, self.element)

    def use(self, target: Hero) -> None:
        target.equip_weapon(self)
