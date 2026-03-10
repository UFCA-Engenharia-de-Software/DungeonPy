from services.monster_factory import MonsterFactory
from infra.cli import Color
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

        # ELEMENT ORDER:
        element_order = {
            1: Element.POISON,
            2: Element.LIGHTNING,
            3: Element.ICE,
            4: Element.FIRE,
            5: Element.NEUTRAL,
        }

        if environment:
            chosen_environment = environment
        else:
            if level in element_order:
                chosen_environment = element_order[level]
            else:
                valid_elements = [element for element in Element if element != Element.NEUTRAL]
                chosen_environment = random.choice(valid_elements)
        
        element_translation = {
            Element.FIRE: (f"{Color.ORANGE}FOGO{Color.RESET}"),
            Element.ICE: (f"{Color.CYAN}GELO{Color.RESET}"),
            Element.LIGHTNING: (f"{Color.YELLOW}RAIO{Color.RESET}"),
            Element.POISON: (f"{Color.PURPLE}VENENO{Color.RESET}"),
        }

        if (chosen_environment != Element.NEUTRAL):
            description = f"Você entra em uma sala dominada pelo {element_translation[chosen_environment]}."
        else:
            description = f"Você entra em uma sala estranha... não parece ter influência elemental aqui."

        monster_1 = MonsterFactory.create_monster(level, chosen_environment)
        monster_2 = MonsterFactory.create_boss(level, chosen_environment)

        return Room(
            description = description,
            environment = chosen_environment,
            monsters = [monster_1, monster_2],
            items = [],
        )

