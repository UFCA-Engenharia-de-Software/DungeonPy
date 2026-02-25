from __future__ import annotations
from domain.weapon import Weapon
from domain.element import Element
from typing import TYPE_CHECKING, Dict, Any

if TYPE_CHECKING:
    from domain.entity import Entity
    from domain.hero import Hero


class Grimoire(Weapon):
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

        super().__init__(
            name=name,
            description=desc,
            weight=weight,
            base_damage=magic_power,
            element=element,
        )

        self.mana_cost = mana_cost

        self._attacks = {
            "1": {
                "description": f"Conjurar {element.name} (MP: {self.mana_cost})",
                "method": self.attack,
            },
            "2": {
                "description": f"Conjurar {element.name} Aprimorado (MP: {self.mana_cost * 2})",
                "method": self.heavy_attack,
            },
        }

    # GETTERS & SETTERS:

    @property
    def magic_power(self) -> int:
        return self.base_damage

    @magic_power.setter
    def magic_power(self, value: int) -> None:
        self.base_damage = value

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

    def attack(self, user: Hero, target: Entity) -> None:
        """
        Attacks. Just like that.
        Verifies mana, consumes it and deals damage to the target as in the Weapon class.
        """

        if getattr(user, "current_mana", 0) < self.mana_cost:
            raise ValueError(f"{user.name} não tem mana o suficiente para isso.")

        # CONSUMING MANA
        user.current_mana -= self.mana_cost
        super().attack(user, target)

    def heavy_attack(self, user: Hero, target: Entity) -> None:
        """
        Uses a stronger attack.
        Consumes more mana, deals more damage.
        """
        heavy_cost = 2 * self.mana_cost
        if getattr(user, "current_mana", 0) < heavy_cost:
            raise ValueError(f"{user.name} não tem mana o suficiente para isso.")

        user.current_mana -= heavy_cost
        super().heavy_attack(user, target)
