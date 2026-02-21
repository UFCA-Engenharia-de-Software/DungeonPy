from domain.hero import Hero
from domain.element import Element
from domain.inventory import Inventory
from domain.grimoire import Grimoire
from domain.entity import Entity
from typing import Dict, Any


class Mage(Hero):
    """
    Represents the Mage archetype.
    It's a Hero class who's got Mana points to cast spells and deal damage.
    Able to use grimoires.
    """

    def __init__(
        self,
        name: str,
        max_life: int,
        current_life: int,
        max_mana: int,
        current_mana: int,
        attack: int,
        speed: int,
        current_status=None,
        element: Element = Element.NEUTRAL,
        weapon_element: Element = Element.NEUTRAL,
        inventory: Inventory = None,
    ):
        super().__init__(
            name,
            max_life,
            current_life,
            attack,
            speed,
            current_status,
            element,
            inventory,
            weapon_element,
        )

        self.max_mana = max_mana
        self.current_mana = current_mana

    # PROPERTIES:

    @property
    def max_mana(self) -> int:
        return self._max_mana

    @max_mana.setter
    def max_mana(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("max_mana must have a 'int' value!")
        if value < 0:
            raise ValueError("max_mana value can't be lower than 0.")

        self._max_mana = value

        if hasattr(self, "_current_mana") and self._current_mana > value:
            self._current_mana = value

    @property
    def current_mana(self) -> int:
        return self._current_mana

    @current_mana.setter
    def current_mana(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("current_mana must have a 'int' value!")

        if value < 0:
            self._current_mana = 0
        elif value > self._max_mana:
            self._current_mana = self._max_mana
        else:
            self._current_mana = value

    # COMBAT METHODS:

    def equip_grimoire(self, grimoire: Grimoire) -> None:
        """Allows Mage to equip grimoires."""
        self.equip_weapon(grimoire)

    def strike(self, target: Entity) -> str:
        """Default attack. Tries to cast the spell from the equipped grimoire."""

        if self.equipped_weapon and isinstance(self.equipped_weapon, Grimoire):
            return self.equipped_weapon.cast_spell(self, target)

        # Fallback (no grimoire equipped):
        damage = 1
        target.damage_received(damage, Element.NEUTRAL)
        return f"Na ausência de grimório, {self.name} deu um soco fraco em {target.name}! {damage} de dano."

    def damage_received(self, value: int, strike_element: Element) -> None:
        super().damage_received(value, strike_element)

    def ancient_magic(self, target: Entity) -> str:
        """Mage's special attack. Costs lots of mana, deals lots of damage."""

        mana_cost = 50

        if self.current_mana < mana_cost:
            return f"{self.name} tentou conjurar Magia Ancestral, mas não tem mana o suficiente para isso."

        self.current_mana -= mana_cost
        damage = (self.attack * 3) + 50
        target.damage_received(damage, Element.NEUTRAL)

        return f"{self.name} canaliza energia pura e lança MAGIA ANCESTRAL em {target.name}! {damage} de dano!"

    def upgrade(self, points: int, choice: int) -> None:
        """Allows to allocate stat points to upgrade the hero."""

        if choice == 1:
            self.attack += points
        elif choice == 2:
            self.max_mana += points
            self.current_mana += points
        else:
            raise ValueError(f"Escolha Inválida: {choice}! Deve ser 1 ou 2.")

    def get_actions(self) -> Dict[str, Any]:
        actions = {}

        if self.equipped_weapon:
            actions.update(self.equipped_weapon.get_attacks())

        else:
            actions["1"] = {
                "description": "Ataque Desarmado (MP: 0)",
                "method": self.strike,
            }

        actions["2"] = {
            "description": "Magia Ancestral (MP: 50)",
            "method": self.ancient_magic,
        }

        return actions
