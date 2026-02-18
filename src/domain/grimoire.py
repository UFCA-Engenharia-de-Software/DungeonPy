from __future__ import annotations
from domain.item import Item
from domain.element import Element
from typing import TYPE_CHECKING, Dict, Any

if TYPE_CHECKING:
    from domain.entity import Entity
    from domain.hero import Hero


class Grimoire(Item):
    """
    Represents a magic spells book.
    Unlike melee and ranged weapons, it consumes Mana and defines the mage's attack element.
    Can only be used by Mages.
    """

    def __init__(
        self,
        name: str,
        element: Element,
        magic_power: int,
        mana_cost: int,
        weight: float = 2.0,
    ):
        if not isinstance(element, Element):
            raise TypeError(
                "The element must belong to the Element type. EX: Element.FIRE"
            )

        desc = f"Um grimório antigo, cujas runas emanam {element.name}."

        super().__init__(name, description=desc, weight=weight)

        self.element = element
        self.magic_power = magic_power
        self.mana_cost = mana_cost
        self._attacks = {
            "1": {
                "description": f"Conjurar {element.name} (MP: {mana_cost})",
                "method": self.cast_spell,
            },
        }

    # GETTERS & SETTERS:

    @property
    def element(self) -> Element:
        return self._element

    @element.setter
    def element(self, value: Element) -> None:
        if not isinstance(value, Element):
            raise TypeError(
                "The element must belong to the Element type. EX: Element.FIRE"
            )
        self._element = value

    @property
    def magic_power(self) -> int:
        return self._magic_power

    @magic_power.setter
    def magic_power(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Magic Power must have a 'int' value.")
        if value < 0:
            raise ValueError("Magic Power can't go below 0.")
        self._magic_power = value

    @property
    def mana_cost(self) -> int:
        return self._mana_cost

    @mana_cost.setter
    def mana_cost(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Mana Cost must have a 'int' value.")
        if value < 0:
            raise ValueError("Mana Cost can't go below 0.")
        self._mana_cost = value

    # METHODS:

    def use(self, target: Entity) -> str:
        """
        Tries to equip the grimoire to the target.
        The method accepts any Entity, but the grimoire can only be equipped if the entity can use grimoires (Mage).
        """

        if hasattr(target, "equip_grimoire"):
            target.equip_grimoire(self)
            return f"{target.name} equipou o grimório '{self.name}'. Suas magias são do elemento {self.element.name} agora!"

        return f"{target.name} tentou ler o grimório e não entendeu nada. Apenas Magos podem usar isso."

    def get_attacks(self) -> Dict[str, Any]:
        return self._attacks

    def cast_spell(self, user: Hero, target: Entity) -> str:
        if getattr(user, "current_mana", 0) < self.mana_cost:
            return f"{user.name} não possui mana o suficiente para usar esse feitiço."

        user.current_mana -= self.mana_cost
        damage = self.magic_power + user.attack
        target.damage_received(damage, self.element)

        return f"{user.name} dispara uma rajada de {self.element.name}! {damage} de dano causado."
