from services.monster_factory import MonsterFactory
from domain.room import Room
from domain.element import Element
import random


class LevelFactory:
    """
    Factory responsible for creating balanced phases
    based on player progression.
    """

    @classmethod
    def create_room(cls, level: int, environment: Element | None = None) -> object:
        """
        Creates a room scaled according to the level.
        """

        if not isinstance(environment, Element) and environment is not None:
            raise TypeError("Enviroment must be a Element object or passes like None")

        if level <= 0:
            raise ValueError("Level must be greater than 0")

        valid_elements = [element for element in Element if element != Element.NEUTRAL]
        chosen_environment = environment or random.choice(valid_elements)

        description = f"Você entra em uma sala, dominada pelo {chosen_environment.name.capitalize()}"

        monstro_1 = MonsterFactory.create_monster(level, chosen_environment)

        if level == 4:
            monstro_2 = MonsterFactory.create_boss(level, chosen_environment)

        else:
            monstro_2 = MonsterFactory.create_monster(level, chosen_environment)

        return Room(
            description=description,
            environment=chosen_environment,
            monsters=[monstro_1, monstro_2],
            items=[],
        )
