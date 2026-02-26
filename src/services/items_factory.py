# services/items_factory.py

from domain.consumable_item import ConsumableItem
from domain.weapon import Weapon
from domain.ranged_weapon import RangedWeapon
from domain.grimoire import Grimoire
from domain.element import Element


class ItemsFactory:
    """
    Responsible only for instantiating item objects.
    """

    ITEM_REGISTRY = {
        "consumable": ConsumableItem,
        "weapon": Weapon,
        "ranged_weapon": RangedWeapon,
        "grimoire": Grimoire,
    }

    """
    Base itens for starter in inventory
    """

    @staticmethod
    def get_base_packs() -> dict:
        return {
            "base_pack_warrior": [
                Weapon(name="Espada de Ferro", base_damage=10),
                Weapon(name="Adaga de Treino", base_damage=5),
                ConsumableItem(
                    name="Poção Pequena",
                    description="Recupera 20 de Vida",
                    weight=0.5,
                    recovered_value=20,
                ),
            ],
            "base_pack_mage": [
                Grimoire(
                    name="Grimório Iniciante",
                    element=Element.FIRE,
                    magic_power=12,
                    mana_cost=5,
                ),
                ConsumableItem(
                    name="Poção de Mana",
                    description="Recupera 30 de Mana",
                    weight=0.5,
                    recovered_value=30,
                ),
            ],
            "base_pack_archer": [
                RangedWeapon(
                    name="Arco de Madeira",
                    base_damage=8,
                    ammo_required=1,
                ),
                ConsumableItem(
                    name="Poção Pequena",
                    description="Recupera 20 de Vida",
                    weight=0.5,
                    recovered_value=20,
                ),
            ],
        }

    """
    Creates and returns a list of instantiated item objects based on a configuration dictionary.
    """

    @staticmethod
    def create_items_from_config(items_config: dict) -> list:
        created_items = []

        for item_type, configs in items_config.items():
            if item_type not in ItemsFactory.ITEM_REGISTRY:
                raise ValueError(f"Tipo de item desconhecido: {item_type}")

            item_class = ItemsFactory.ITEM_REGISTRY[item_type]

            for config in configs:
                created_items.append(item_class(**config))

        return created_items

    """
    Drop of Monsters
    """
    DROP_TABLES = {
        # FIRE
        "Salamandra": {
            "grimoire": [
                {
                    "name": "Grimório Flamejante",
                    "element": Element.FIRE,
                    "magic_power": 30,
                    "mana_cost": 8,
                }
            ]
        },
        "Demônio Ígneo": {
            "weapon": [{"name": "Espada Incandescente", "base_damage": 28}]
        },
        "Espírito Vulcânico": {
            "grimoire": [
                {
                    "name": "Tomo Vulcânico",
                    "element": Element.FIRE,
                    "magic_power": 35,
                    "mana_cost": 10,
                }
            ]
        },
        # ICE
        "Golem de Gelo": {"weapon": [{"name": "Martelo Congelado", "base_damage": 26}]},
        "Lobo Glacial": {
            "ranged_weapon": [
                {
                    "name": "Arco Congelante",
                    "base_damage": 22,
                    "ammo_required": 1,
                }
            ]
        },
        "Espectro Congelado": {
            "grimoire": [
                {
                    "name": "Grimório Glacial",
                    "element": Element.ICE,
                    "magic_power": 27,
                    "mana_cost": 7,
                }
            ]
        },
        # LIGHTNING
        "Serpente Elétrica": {
            "ranged_weapon": [
                {
                    "name": "Arco Tempestuoso",
                    "base_damage": 24,
                    "ammo_required": 1,
                }
            ]
        },
        "Raijin": {
            "grimoire": [
                {
                    "name": "Códice do Trovão",
                    "element": Element.LIGHTNING,
                    "magic_power": 40,
                    "mana_cost": 12,
                }
            ]
        },
        "Elemental de Raio": {
            "weapon": [{"name": "Lâmina Trovejante", "base_damage": 30}]
        },
        # POISON
        "Aranha Tóxica": {"weapon": [{"name": "Adaga Envenenada", "base_damage": 20}]},
        "Hidra Venenosa": {"weapon": [{"name": "Lança Venenosa", "base_damage": 32}]},
        "Slime Corrosivo": {
            "consumable": [
                {
                    "name": "Essência Corrosiva",
                    "description": "Recupera 25 de Vida",
                    "weight": 0.5,
                    "recovered_value": 25,
                }
            ]
        },
        # NEUTRAL
        "Goblin": {"weapon": [{"name": "Adaga Rústica", "base_damage": 12}]},
        "Orc": {"weapon": [{"name": "Machado de Guerra", "base_damage": 22}]},
        "Bandido Sombrio": {
            "ranged_weapon": [
                {
                    "name": "Besta Sombria",
                    "base_damage": 23,
                    "ammo_required": 1,
                }
            ]
        },
    }

    @staticmethod
    def get_predefined_drop_table(monster_name: str) -> dict:
        return ItemsFactory.DROP_TABLES.get(monster_name, {})
