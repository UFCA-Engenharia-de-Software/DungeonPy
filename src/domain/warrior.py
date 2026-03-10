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
        inventory: Inventory = None,
        #
        shield: int = 0,
        armor: int = 0,
        defend: bool = False,
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
        )
        self.shield = shield
        self.armor = armor
        self.defend = defend
        self.in_rage = in_rage
        #
        self.normal_state: dict = {}
        self.attributes_to_upgrade = ["shield", "armor"]
        self.in_test = in_test

    def strike(self, target: Entity) -> None:
        """
        Atack enemies with default choice.
        """
        if self.equipped_weapon is None:
            raise ValueError(
                "Nenhuma arma equipada! Equipe uma arma no inventário antes de atacar."
            )
        self.equipped_weapon.attack(self, target)

    def heavy_strike(self, target: Entity) -> None:
        """
        Atack enemies with heavy choice.
        """
        if self.equipped_weapon is None:
            raise ValueError(
                "Nenhuma arma equipada! Equipe uma arma no inventário antes de atacar."
            )
        self.equipped_weapon.heavy_attack(self, target)

    def damage_received(self, value: int, strike_element: Element) -> None:
        """Defends an strike or takes damage"""
        multiplier = strike_element.multiplier(self.element)
        final_damage = multiplier * value

        self._attempt_defend()

        if self.defend:
            self.last_blocked = True
            self._reset_defend()
            return

        self.current_life -= max(0, int(final_damage - self.armor))

    def upgrade(self, points: int) -> None:
        """Upgrade specific attributes (shield, armor)."""
        shield_increase = points // 2
        armor_increase = points - shield_increase
        self.shield += shield_increase
        self.armor += armor_increase
        self.attack += 2

        self.max_life += 10
        self.current_life += 10

    def _attempt_defend(self):
        """Check if defense succeeds based on shield strength"""

        # Validation to test `defend` without randomize
        if self.in_test:
            return

        chance = random.randint(1, 100)
        self.defend = chance <= self.shield

    def _reset_defend(self):
        """Reset defense state after handling damage"""
        self.defend = False

    def to_rage(self) -> None:
        """
        Sacrifice defense in the current turn to douple damage in the next atack.
        """
        if self.in_rage:
            raise ValueError(f"{self.name} já está em Fúria! ATAQUE!!")

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

        # Some kind of clock to end rage when needed
        self.rage_duration = 2

    def reset_rage(self) -> None:
        """Return attributes to normal values after a rage"""
        self.in_rage = self.normal_state["in_rage"]
        self.attack = self.normal_state["attack"]
        self.shield = self.normal_state["shield"]
        self.armor = self.normal_state["armor"]

        self.normal_state = {}

    def end_of_turn_routine(self):
        """Calls reset_rage for GameManager using."""
        if self.in_rage:
            self.rage_duration -= 1

            if self.rage_duration <= 0:
                self.reset_rage()

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
