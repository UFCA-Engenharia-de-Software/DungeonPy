from abc import abstractmethod
from domain.entity import Entity
from domain.element import Element
from domain.inventory import Inventory


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
        weapon_element: Element = Element.NEUTRAL,
    ):
        super().__init__(
            name, max_life, current_life, attack, speed, current_status, element
        )
        self.inventory = inventory or Inventory()
        self.weapon_element = weapon_element

    @abstractmethod
    def strike(self, strike_elemente: Element) -> None:
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
