from abc import abstractmethod
from typing import TYPE_CHECKING

from domain.element import Element
from domain.entity import Entity
from domain.inventory import Inventory

if TYPE_CHECKING:
    from domain.weapon import Weapon


class Hero(Entity):
    """
    Abstract base class for game heroes.

    Subclasses must implement 'strike' and 'upgrade' mechanics specific to their archetype
    (Warrior, Archer and Wizard).
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
    ):
        super().__init__(
            name, max_life, current_life, attack, speed, current_status, element
        )
        self.inventory = inventory if inventory is not None else Inventory()
        self._equipped_weapon = None

    @property
    def equipped_weapon(self):
        return self._equipped_weapon

    def equip_weapon(self, weapon: "Weapon") -> None:
        
        if hasattr(weapon, "allowed_class") and self.__class__.__name__ not in weapon.allowed_class:
            raise TypeError(f"A classe {self.__class__.__name__} não possui o conhecimento para empunhar {weapon.name}!")
        
        if self._equipped_weapon is not None:
            raise ValueError("Hero already has a weapon equipped.")

        self.inventory.remove_item_from_inventory(weapon)
        self._equipped_weapon = weapon

    def unequip_weapon(self) -> None:
        if self._equipped_weapon is None:
            raise ValueError("No weapon equipped.")

        if not self.inventory.add_item_to_inventory(self._equipped_weapon):
            raise ValueError("Inventory full.")

        self._equipped_weapon = None

    @abstractmethod
    def strike(self, target: Entity) -> None:
        """
        Atack enemies.

        Args:
            target (Entity): enemy to atack.
        """
        pass

    @abstractmethod
    def damage_received(self, value: int, strike_element: Element) -> None:
        """
        Each class has some spetial attributes for defense or evasion.
        """
        pass

    @abstractmethod
    def upgrade(self, points: int, choice: int) -> None:
        """
        Upgrade specific attributes.

        Args:
            poinst (int): amount of points that the player have.
            choice (int): selected attribute to upgrade.
        """
        pass

    @abstractmethod
    def get_actions(self) -> dict:
        """
        Mapping of action keys to action details.
        """
        pass

    def get_hero_status(self) -> dict:
        """
        Return a dict with all hero status.
        """
        weapon_name = self._equipped_weapon.name if self._equipped_weapon else "Nenhuma"

        return {
            "name": self.name,
            "current_life": self.current_life,
            "max_life": self.max_life,
            "attack": self.attack,
            "speed": self.speed,
            "element": self.element.value,
            "equipped_weapon": weapon_name,
        }
