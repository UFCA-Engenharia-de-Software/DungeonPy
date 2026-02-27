from services.arts import MONSTER_ARTS
import random
from domain.monster import Monster
from domain.element import Element


class MonsterFactory:
    """
    Factory responsible for creating balanced monsters
    based on room level or player progression.
    """

    BASE_NAMES = {
        Element.FIRE: ["Salamandra", "Lobo de Fogo", "Cavaleiro de Fogo"],
        Element.ICE: ["Golem de Gelo", "Yeti", "Espectro Congelado"],
        Element.LIGHTNING: ["Medusa Elétrica", "Raijin", "Elemental de Raio"],
        Element.POISON: ["Aranha Tóxica", "Sapo Venenoso", "Slime Corrosivo"],
        Element.NEUTRAL: ["Goblin", "Orc", "Bandido Sombrio"],
    }

    @classmethod
    def create_monster(cls, level: int, element: Element | None = None) -> Monster:
        """
        Creates a monster scaled according to the level.
        """

        if level <= 0:
            raise ValueError("Level must be greater than 0")

        element = element or random.choice(list(Element))

        name = random.choice(cls.BASE_NAMES[element])

        # Progressive scaling
        max_life = 50 + (level * 15)
        attack = 10 + (level * 5)
        speed = 5 + level
        art = MONSTER_ARTS.get(name, MONSTER_ARTS["DEFAULT"])

        description = (
            f"{name} de nível {level}. "
            f"Uma criatura imbuída com o poder de {element.name.lower()}."
        )

        return Monster(
            name=name,
            max_life=max_life,
            attack=attack,
            speed=speed,
            element=element,
            loot=[],  # Can be integrated with ItemFactory later
            description=description,
            art=art,
        )

    @classmethod
    def create_boss(cls, level: int, element: Element) -> Monster:
        """
        Creates a stronger monster for special rooms.
        """

        name = f"Guardião Supremo de {element.name.title()}"

        max_life = 120 + (level * 25)
        attack = 25 + (level * 8)
        speed = 10 + level

        description = f"{name}, um chefe elemental extremamente poderoso."

        return Monster(
            name=name,
            max_life=max_life,
            attack=attack,
            speed=speed,
            element=element,
            loot=[],
            description=description,
        )
