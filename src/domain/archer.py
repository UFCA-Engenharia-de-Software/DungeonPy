from domain.hero import Hero
from domain.element import Element
from domain.entity import Entity
from domain import state
from domain.ranged_weapon import RangedWeapon
from domain.inventory import Inventory
import random


class Archer(Hero):
    """
    A Ranged Hero archetype that relies on speed, precision, and ammunition.

    The Archer balances risk and reward using the 'Aim' mechanic: sacrificing
    mobility (dodge) for guaranteed hits and increased damage.
    Unlike other classes, the Archer manages a resource (Ammo) and avoids damage
    through a speed-based Dodge mechanic rather than heavy armor.

    Attributes:
        max_ammo (int): Maximum capacity of the quiver.
        current_ammo (int): Current arrows available.
        dodge (bool): State indicating if the next attack will be evaded.
        equipped_weapon (RangedWeapon): The bow or ranged weapon currently in use.
        is_aiming (bool): State indicating if the Archer is focused (cant dodge, buffs damage).
    """

    def __init__(
        self,
        name: str,
        max_life: int,
        current_life: int,
        attack: int,
        speed: int,
        current_status: state = None,
        element: Element = Element.NEUTRAL,
        inventory: Inventory = None,
        max_ammo: int = 10,
        current_ammo: int = 0,
        dodge: bool = False,
        equipped_weapon: RangedWeapon = None,
        is_aiming: bool = False,
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

        self.max_ammo = max_ammo
        self.current_ammo = current_ammo
        self.dodge = dodge
        if equipped_weapon is not None:
            self.equip_weapon(equipped_weapon)
        self.is_aiming = is_aiming

    @property
    def max_ammo(self):
        return self._max_ammo

    @max_ammo.setter
    def max_ammo(self, value):
        if not isinstance(value, int):
            raise TypeError("Max ammo must be a int")

        if value <= 0:
            raise ValueError("Max ammo cannot be negative or 0")

        self._max_ammo = value

    @property
    def current_ammo(self):
        return self._current_ammo

    @current_ammo.setter
    def current_ammo(self, value):
        if not isinstance(value, int):
            raise TypeError("Current ammo must be a int")

        if value < 0:
            raise ValueError("Current ammo cannot be a negative number")

        if value > self.max_ammo:
            raise ValueError("Current ammo must not be greater than max_ammo")

        self._current_ammo = value

    @property
    def dodge(self):
        return self._dodge

    @dodge.setter
    def dodge(self, value):
        if not isinstance(value, bool):
            raise TypeError("Deviation probability needs to be true or false")

        self._dodge = value

    @property
    def is_aiming(self):
        return self._is_aiming

    @is_aiming.setter
    def is_aiming(self, value):
        if not isinstance(value, bool):
            raise TypeError("Is aiming needs to be True or False")

        self._is_aiming = value

    def equip_weapon(self, weapon: RangedWeapon):
        if not isinstance(weapon, RangedWeapon):
            raise TypeError("Archer Weapon must be a RangedWeapon")

        super().equip_weapon(weapon)

    def strike(self, target: Entity) -> None:
        """
        Attack enemies - lembrar de modificar esse método em guerreiro
        """

        normal_attack = self.attack
        if self.equipped_weapon is None:
            raise ValueError("No weapon equiped")

        if self.is_aiming:
            self.attack = int(self.attack + (self.attack / 2.5))
        try:
            self.equipped_weapon.attack(self, target)
        finally:
            # Still happens yet the weapon method fail
            self.is_aiming = False
            self.attack = normal_attack

    def damage_received(self, value: int, strike_element: Element) -> None:
        """Calculates dodge chance first, then applies damage if not dodged."""
        # Roll dodge BEFORE taking damage so battle.py can compare life before/after
        self.attempted_dodge()

        if self.dodge:
            # Dodge successful: reset flag and skip damage entirely
            self.last_dodged = True
            self.reset_dodge()
            return

        multiplier = strike_element.multiplier(self.element)
        final_damage = multiplier * value
        self.current_life -= int(final_damage)

    def attempted_dodge(self) -> None:
        """Calculate dodge based on speed and randomness"""

        if self.is_aiming:
            self.reset_dodge()
            return

        chance = random.randint(1, 100)
        self.dodge = chance <= self.speed

    def ultimate(self, target: Entity):
        """Archer's special attack. Costs lots of arrows and a bit of life, deals lots of damage."""

        ammo_cost = 3

        if self.current_ammo < ammo_cost:
            return f"{self.name} não tem munição suficiente para isso."

        life_recoil = 15
        if self.current_life <= life_recoil:
            return f"{self.name} está muito fraco e não aguentaria o recuo do ataque."

        damage = int(self.attack * 3.2)
        target.damage_received(damage, Element.NEUTRAL)

        self.current_ammo -= ammo_cost
        self.current_life -= life_recoil

        return f"{self.name} sacrifica sua própria vitalidade para disparar um TIRO TRIPLO letal em {target.name}! Causou {damage} de dano."

    def reset_dodge(self) -> None:
        """Reset dodge after deviating"""
        self.dodge = False

    def reload(self) -> None:
        """reset the class attribute current_ammo to max"""
        self.current_ammo = self.max_ammo

    def aim(self) -> None:
        """Archer Habilite that he cannot miss the strike, receive a little damage boost and cannot dodge"""
        self.is_aiming = True
        self.dodge = False

    def end_of_turn_routine(self):
        """Resets aiming for GameManager using."""
        pass

    def upgrade(self, points: int) -> None:
        """Upgrade specific attributes (attack, speed)
        It`s ignoring the parent class logic for game design choice and otimization of time
        """

        speed_increase = points // 2
        ammo_increase = points - speed_increase
        attack_increase = ammo_increase

        self.speed += speed_increase
        self.max_ammo += ammo_increase
        self.attack += attack_increase

        self.max_life += 10
        self.current_life += 10

    def get_actions(self) -> dict:
        """
        Returns available combat actions for this archetype.
        """

        return {
            "1": {
                "description": "Atirar (Ataque básico com arma, gasta 1 flecha)",
                "method": self.strike,
            },
            "2": {
                "description": "Mirar (acerto garantido, sacrifica esquiva, aumenta de leve o dano)",
                "method": self.aim,
            },
            "3": {
                "description": "Recarregar (recarrega a munição)",
                "method": self.reload,
            },
            "4": {
                "description": "Tiro Triplo (Gasta 3 flechas, se dá 10 de dano, mas inflige muito dano)",
                "method": self.ultimate,
            },
        }
