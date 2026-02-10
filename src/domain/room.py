from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING

from .mixins import DescriptionMixin
from .element import Element

if TYPE_CHECKING:
    from .monster import Monster
    from .entity import Entity
    from .item import Item


class Room(DescriptionMixin):
    """
    Represents a location in the dungeon, where the player can explore, encounter enemies or find items.

    Attributes:
        description (str): Narrative description of the room.
        environment (Element): The elemental nature of the room.
        monsters (List[Monster]): List of enemies present in the room.
        items (List[Item]): List of loot available in the room.
    """

    def __init__(
        self,
        description: str,
        environment: Element,
        monsters: Optional[List[Monster]] = None,
        items: Optional[List[Item]] = None,
    ) -> None:
        self.description = description
        self.environment = environment
        self._monsters: List[Monster] = []
        self._items: List[Item] = []

        if monsters:
            for m in monsters:
                self.add_monster(m)

        if items:
            for i in items:
                self.add_item(i)

    # PROPERTIES:

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Description must be a string!")
        if not value.strip():
            raise ValueError("Description cannot be empty!")
        self._description = value

    @property
    def environment(self) -> Element:
        return self._environment

    @environment.setter
    def environment(self, value: Element) -> None:
        if not isinstance(value, Element):
            raise TypeError("Environment must be of type Element!")
        self._environment = value

    # LIST MANAGEMENT:

    def add_monster(self, monster: Monster) -> None:
        """Adds a monster to the room."""
        self._monsters.append(monster)

    def remove_monster(self, monster: Monster) -> None:
        if monster in self._monsters:
            self._monsters.remove(monster)

    def add_item(self, item: Item) -> None:
        self._items.append(item)

    def remove_item(self, item: Item) -> None:
        if item in self._items:
            self._items.remove(item)

    def take_item(self, item_name: str) -> Optional[Item]:
        """
        Tries to find and remove an item from the room by name.
        Represents the hero looting the room.
        """

        for index, item in enumerate(self._items):
            if item.name.lower() == item_name.lower():
                return self._items.pop(index)
        return None

    @property
    def monsters(self) -> List[Monster]:
        """Returns a copy of the list, to prevent direct modifications."""
        return self._monsters[:]

    @property
    def items(self) -> List[Item]:
        """Returns a copy of the list."""
        return self._items[:]

    # DOMAIN LOGIC:

    def get_description(self) -> str:
        """
        Returns the full description of the room, including environment, monsters and items.
        """
        text = f"{self.description}\n"
        text += f"Ambiente: {self.environment.name}\n"

        if self.monsters:
            names = " ,".join([m.name for m in self.monsters])
            text += f"ATENÇÃO! INIMIGOS À VISTA: {names}\n"
        else:
            text += "A sala parece vazia...\n"

        if self.items:
            names = " ,".join([i.name for i in self.items])
            text += f"Na sala, você encontrou: {names}\n"
        else:
            text += "Não há nenhum item de valor por perto."

        return text

    def enter(self, hero: Entity) -> str:
        """
        Logic for when an entity (usually, the Hero) enters the room.
        """

        log = "-" * 30 + "\n"
        log += self.get_description() + "\n"
        log += "-" * 30 + "\n"

        if self._monsters:
            log += f"{hero.name} encontrou inimigos! Prepare-se para lutar!\n"
        else:
            log += "A sala parece tranquila.\n"

        return log
