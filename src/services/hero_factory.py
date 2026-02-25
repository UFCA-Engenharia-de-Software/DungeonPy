from domain.archer import Archer
from domain.element import Element
from domain.hero import Hero
from domain.inventory import Inventory
from domain.mage import Mage
from domain.warrior import Warrior


# Balancing constants per archetype
WARRIOR_STATS = {
    "max_life": 150,
    "attack": 30,
    "speed": 10,
    "shield": 20,
    "armor": 15,
    "element": Element.NEUTRAL,
}

MAGE_STATS = {
    "max_life": 80,
    "attack": 50,
    "speed": 15,
    "max_mana": 100,
    "current_mana": 100,
    "element": Element.FIRE,
}

ARCHER_STATS = {
    "max_life": 100,
    "attack": 35,
    "speed": 25,
    "max_ammo": 15,
    "current_ammo": 15,
    "element": Element.NEUTRAL,
}

VALID_ARCHETYPES = ("warrior", "mage", "archer")


class HeroFactory:
    """Factory for creating heroes with balanced attributes.

    Responsibilities:
        - Instantiate heroes of each archetype with balanced stats.
        - Provide the differentials of each class for the interface.
        - Supply base packs of starter items for each archetype.
    """

    @staticmethod
    def get_class_differentials() -> dict:
        """Return a dictionary with the differentials of each archetype."""
        return {
            "warrior": {
                "description": "Expert in physical combat and survival.",
                "stats": {
                    "max_life": WARRIOR_STATS["max_life"],
                    "attack": WARRIOR_STATS["attack"],
                    "speed": WARRIOR_STATS["speed"],
                    "shield": WARRIOR_STATS["shield"],
                    "armor": WARRIOR_STATS["armor"],
                },
                "element": WARRIOR_STATS["element"].value,
                "special_abilities": ["to_rage", "defend"],
                "upgradeable_attributes": ["shield", "armor"],
            },
            "mage": {
                "description": "Master of arcane arts.",
                "stats": {
                    "max_life": MAGE_STATS["max_life"],
                    "attack": MAGE_STATS["attack"],
                    "speed": MAGE_STATS["speed"],
                    "max_mana": MAGE_STATS["max_mana"],
                },
                "element": MAGE_STATS["element"].value,
                "special_abilities": ["meditate", "ancient_magic", "heavy_strike"],
                "upgradeable_attributes": ["attack", "max_mana"],
            },
            "archer": {
                "description": "Swift and precise ranged combatant.",
                "stats": {
                    "max_life": ARCHER_STATS["max_life"],
                    "attack": ARCHER_STATS["attack"],
                    "speed": ARCHER_STATS["speed"],
                    "max_ammo": ARCHER_STATS["max_ammo"],
                },
                "element": ARCHER_STATS["element"].value,
                "special_abilities": ["aim", "reload", "dodge"],
                "upgradeable_attributes": ["speed", "max_ammo", "attack"],
            },
        }

    @staticmethod
    def get_base_packs() -> dict:
        """Return the starter item packs for each archetype.
        - Delegates item creation to the static method `ItemsFactory.get_base_packs()`.
        """
        from services.items_factory import ItemsFactory

        return ItemsFactory.get_base_packs()

    @staticmethod
    def create_hero(choice: str, name: str) -> Hero:
        """Instantiate and return a hero of the chosen archetype."""
        choice_lower = choice.strip().lower()

        if choice_lower not in VALID_ARCHETYPES:
            raise ValueError(
                f"Invalid archetype: '{choice}'. "
                f"Valid options: {', '.join(VALID_ARCHETYPES)}"
            )

        if choice_lower == "warrior":
            return HeroFactory._create_warrior(name)
        if choice_lower == "mage":
            return HeroFactory._create_mage(name)
        if choice_lower == "archer":
            return HeroFactory._create_archer(name)

    # Creation methods per archetype
    @staticmethod
    def _create_warrior(name: str) -> Warrior:
        """Create a Warrior instance with balanced attributes."""
        inventory = Inventory()

        base_pack = HeroFactory.get_base_packs().get("base_pack_warrior", [])
        for item in base_pack:
            inventory.add_item_to_inventory(item)

        return Warrior(
            name=name,
            max_life=WARRIOR_STATS["max_life"],
            current_life=WARRIOR_STATS["max_life"],
            attack=WARRIOR_STATS["attack"],
            speed=WARRIOR_STATS["speed"],
            element=WARRIOR_STATS["element"],
            inventory=inventory,
            shield=WARRIOR_STATS["shield"],
            armor=WARRIOR_STATS["armor"],
        )

    @staticmethod
    def _create_mage(name: str) -> Mage:
        """Create a Mage instance with balanced attributes."""
        inventory = Inventory()

        base_pack = HeroFactory.get_base_packs().get("base_pack_mage", [])
        for item in base_pack:
            inventory.add_item_to_inventory(item)

        return Mage(
            name=name,
            max_life=MAGE_STATS["max_life"],
            current_life=MAGE_STATS["max_life"],
            max_mana=MAGE_STATS["max_mana"],
            current_mana=MAGE_STATS["current_mana"],
            attack=MAGE_STATS["attack"],
            speed=MAGE_STATS["speed"],
            element=MAGE_STATS["element"],
            inventory=inventory,
        )

    @staticmethod
    def _create_archer(name: str) -> Archer:
        """Create an Archer instance with balanced attributes."""
        inventory = Inventory()

        base_pack = HeroFactory.get_base_packs().get("base_pack_archer", [])
        for item in base_pack:
            inventory.add_item_to_inventory(item)

        archer = Archer(
            name=name,
            max_life=ARCHER_STATS["max_life"],
            current_life=ARCHER_STATS["max_life"],
            attack=ARCHER_STATS["attack"],
            speed=ARCHER_STATS["speed"],
            element=ARCHER_STATS["element"],
            max_ammo=ARCHER_STATS["max_ammo"],
            current_ammo=ARCHER_STATS["current_ammo"],
        )
        archer.inventory = inventory
        return archer
