from services.arts import MONSTER_ARTS
from services.items_factory import ItemsFactory
import random
from domain.monster import Monster
from domain.element import Element


class MonsterFactory:
    """
    Factory responsible for creating balanced monsters
    based on room level or player progression.

    Integration with ItemsFactory:
        Every monster created here already carries its loot list populated
        via ItemsFactory.get_loot_for_monster(name). The GameManager only
        needs to call monster.get_loot() after confirming the monster is
        defeated — no extra factory call required at that point.
    """

    BASE_NAMES = {
        Element.FIRE: ["Salamandra", "Demônio Ígneo", "Espírito Vulcânico"],
        Element.ICE: ["Golem de Gelo", "Lobo Glacial", "Espectro Congelado"],
        Element.LIGHTNING: ["Serpente Elétrica", "Raijin", "Elemental de Raio"],
        Element.POISON: ["Aranha Tóxica", "Hidra Venenosa", "Slime Corrosivo"],
        Element.NEUTRAL: ["Goblin", "Orc", "Bandido Sombrio"],
    }

    @classmethod
    def create_monster(cls, level: int, element: Element | None = None) -> Monster:
        """
        Creates a monster scaled according to the level.
        Loot is automatically populated via ItemsFactory.
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

        # call directly after victory
        loot = ItemsFactory.get_loot_for_monster(name)

        return Monster(
            name=name,
            max_life=max_life,
            attack=attack,
            speed=speed,
            element=element,
            loot=loot,
            description=description,
            art=art,
        )

    @classmethod
    def create_boss(cls, level: int, element: Element) -> Monster:
        """
        Creates a stronger monster for special rooms.
        Bosses drop the standard fixed items (potions) only,
        since their name won't match any DROP_TABLE entry.
        To give bosses unique drops, add their name to DROP_TABLES.
        """
        name = f"Guardião Supremo de {element.name.title()}"

        max_life = 120 + (level * 25)
        attack = 25 + (level * 8)
        speed = 10 + level

        description = f"{name}, um chefe elemental extremamente poderoso."

        # Bosses always drop the fixed potions; unique gear can be added
        # to DROP_TABLES using their generated name as key if needed.
        loot = ItemsFactory.get_loot_for_monster(name)

        return Monster(
            name=name,
            max_life=max_life,
            attack=attack,
            speed=speed,
            element=element,
            loot=loot,
            description=description,
        )
