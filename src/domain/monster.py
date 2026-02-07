from domain.element import Element
from domain.entity import Entity
from domain.mixins import DescriptionMixin


class Monster(Entity, DescriptionMixin):
    """Class that represents a monster in the game.

    Monsters are entities that can attack heroes and drop items when defeated.
    They have an elemental affinity that affects damage calculation based on
    elemental advantages and disadvantages.

    Attributes:
        name (str): The monster's name.
        max_life (int): The maximum health points of the monster.
        current_life (int): The current health points of the monster.
        attack (int): The base attack power of the monster.
        speed (int): The speed stat that determines turn order in combat.
        current_status (State | None): The current status effect applied to the monster.
        element (Element): The elemental affinity of the monster.
        dropped_items (List[Item]): Items that can be dropped when defeated.
    """

    def __init__(
        self,
        name: str,
        max_life: int,
        attack: int,
        speed: int,
        element: Element,
        loot: list | None = None,
        description: str = "",
    ):
        super().__init__(
            name=name,
            max_life=max_life,
            current_life=max_life,
            attack=attack,
            speed=speed,
            current_status=None,
            element=element,
        )

        self.loot = loot or []
        self._description = description

    @property
    def loot(self) -> list:
        return self._loot

    @loot.setter
    def loot(self, value: list):
        if not isinstance(value, list):
            raise TypeError("Loot must be a list")
        self._loot = value

    def strike(self, target: Entity) -> None:
        target.damage_received(self.attack, self.element)

    def get_loot(self) -> list:
        return self.loot if not self.is_it_alive() else []

    def get_description(self) -> str:
        if self._description:
            return self._description
        return f"{self.name} is a {self.element.value} element monster."
