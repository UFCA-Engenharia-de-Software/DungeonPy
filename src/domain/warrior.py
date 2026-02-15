from domain.hero import Hero
from domain.element import Element
from domain.inventory import Inventory
from domain.entity import Entity
import random


class Warrior(Hero):
    """Define some methods and specific attributes to Warrior archetype (expert in physical combat and survival).

    Args:
        Hero (abstraticlass): define some responsabilities to Warrior class.
    """

    def __init__(
        self,
        name: str,
        max_life: int,
        current_life: int,
        attack: int,
        speed: int,
        current_status=None,
        element: Element = Element.NEUTRAL,
        weapon_element: Element = Element.NEUTRAL,
        inventory: Inventory = None,
        #
        shield: int = 0,
        armor: int = 0,
        defend: bool = False,
        # weapon_upgrade: int = 0,
        in_rage: bool = False,
        in_test: bool = False,
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
        self.shield = shield
        self.armor = armor
        self.defend = defend
        # self.weapon_upgrade = weapon_upgrade
        self.in_rage = in_rage
        #
        self.normal_state: dict = {}
        self.attributes_to_upgrade = ["shield", "armor"]
        self.in_test = in_test

    def strike(self, target: Entity) -> None:
        """
        Atack enemies.
        """
        target.damage_received(self.attack, self.weapon_element)

    def damage_received(self, value: int, strike_element: Element) -> None:
        """Defends an strike or takes damage"""
        multiplier = strike_element.multiplier(self.element)
        final_damage = multiplier * value

        self._attempt_defend()

        if self.defend:
            self._reset_defend()
            return

        self.current_life -= max(0, int(final_damage - (self.shield + self.armor)))

    def upgrade(self, points: int, choice: int) -> None:
        """Upgrade specific attributes (shield, armor, weapon_upgrade)."""

        match choice:
            case 1:
                self.shield += points
            case 2:
                self.armor += points
            case _:
                raise ValueError(f"Escolha inválida {choice}. Deve ser 1 ou 2.")

    def _attempt_defend(self):
        """Check if defense succeeds based on shield strength"""

        # Validation to test `defend` without randomize
        if self.in_test:
            return

        buffer = random.randint((-self.shield), self.shield)
        self.defend = buffer > 0

    def _reset_defend(self):
        """Reset defense state after handling damage"""
        self.defend = False

    def to_rage(self) -> None:
        """
        Sacrifice defense in the current turn to douple damage in the next atack.
        """

        self.normal_state = {
            "in_rage": self.in_rage,
            "attack": self.attack,
            "shield": self.shield,
            "armor": self.armor,
        }

        self.in_rage = True
        self.attack = self.attack * 2
        self.shield = 0
        self.armor = 0

    def reset_rage(self) -> None:
        """Return attributes to normal values after a rage"""
        self.in_rage = self.normal_state["in_rage"]
        self.attack = self.normal_state["attack"]
        self.shield = self.normal_state["shield"]
        self.armor = self.normal_state["armor"]

        self.normal_state = {}

    def get_actions(self) -> dict:
        """
        Returns available combat actions for this archetype.
        """

        return {
            "1": {
                "description": "Atacar (ataque básico com arma)",
                "method": self.strike,
            },
            "2": {
                "description": "Fúria (dobra ataque, sacrifica defesa)",
                "method": self.to_rage,
            },
        }
