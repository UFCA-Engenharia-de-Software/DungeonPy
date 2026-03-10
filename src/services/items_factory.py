from domain.consumable_item import ConsumableItem
from domain.weapon import Weapon
from domain.ranged_weapon import RangedWeapon
from domain.grimoire import Grimoire
from domain.element import Element
import random


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

    # Fixes drops for more easy progression
    @staticmethod
    def _fixed_drops() -> list:
        """Returns fresh ConsumableItem instances based on a drop chance."""
        drops = []

        if random.random() <= 0.70:
            drops.append(
                ConsumableItem(
                    name="Poção de Cura",
                    description="Recupera 40 de Vida.",
                    weight=0.5,
                    recovered_value=40,
                )
            )

        if random.random() <= 0.50:
            drops.append(
                ConsumableItem(
                    name="Poção de Mana",
                    description="Recupera 30 de Mana.",
                    weight=0.5,
                    recovered_value=30,
                    recovery_type="mana",
                )
            )

        return drops

    # Table of drops the monster
    # Table of drops the monster
    DROP_TABLES = {
        # Drop fire items
        "Salamandra": {  # grimoire
            "grimoire": [
                {
                    "name": "Grimório Flamejante",
                    "element": Element.FIRE,
                    "magic_power": 30,
                    "mana_cost": 8,
                    "description": "Páginas quentes ao toque. Capaz de incinerar inimigos.",
                }
            ]
        },
        "Cavaleiro de Fogo": {  # weapon (ANTES ERA Demônio Ígneo)
            "weapon": [
                {
                    "name": "Espada Incandescente",
                    "base_damage": 25,
                    "description": "Forjada no núcleo de um vulcão. A lâmina nunca esfria.",
                }
            ]
        },
        "Lobo de Fogo": {  # ranged_weapon (ANTES ERA Espírito Vulcânico)
            "ranged_weapon": [
                {
                    "name": "Arco Vulcânico",
                    "base_damage": 24,
                    "ammo_required": 1,
                    "element": Element.FIRE,
                    "description": "Dispara flechas extremamente quentes, cuidado com os dedos.",
                }
            ]
        },
        # Drop ice items
        "Golem de Gelo": {  # weapon
            "weapon": [
                {
                    "name": "Martelo Congelado",
                    "base_damage": 25,
                    "description": "Pesado e brutal. Com ele, com certeza algo vai sobrar",
                }
            ]
        },
        "Yeti": {  # ranged_weapon (ANTES ERA Lobo Glacial)
            "ranged_weapon": [
                {
                    "name": "Arco Congelante",
                    "base_damage": 22,
                    "ammo_required": 1,
                    "element": Element.ICE,
                    "description": "A corda deste arco é feita de pura geada mágica.",
                }
            ]
        },
        "Espectro Congelado": {  # grimoire
            "grimoire": [
                {
                    "name": "Grimório Glacial",
                    "element": Element.ICE,
                    "magic_power": 27,
                    "mana_cost": 7,
                    "description": "Lê-se 'Fica frio aí' em runas antigas na parte de trás. Fascinante.",
                }
            ]
        },
        # Drop lightning items
        "Serpente Elétrica": {  # ranged_weapon
            "ranged_weapon": [
                {
                    "name": "Arco Tempestuoso",
                    "base_damage": 26,
                    "ammo_required": 1,
                    "element": Element.LIGHTNING,
                    "description": "Veloz como um relâmpago, mortal como a tempestade.",
                }
            ]
        },
        "Raijin": {  # grimoire
            "grimoire": [
                {
                    "name": "Códice do Trovão",
                    "element": Element.LIGHTNING,
                    "magic_power": 33,
                    "mana_cost": 12,
                    "description": "As runas deste livro estalam com pura eletricidade.",
                }
            ]
        },
        "Medusa Elétrica": {  # weapon (ANTES ERA Elemental de Raio)
            "weapon": [
                {
                    "name": "Lâmina Trovejante",
                    "base_damage": 28,
                    "element": Element.LIGHTNING,
                    "description": "Uma espada que emite o som de um trovão a cada golpe.",
                }
            ]
        },
        # Drop poison items
        "Aranha Tóxica": {  # weapon
            "weapon": [
                {
                    "name": "Adaga Envenenada",
                    "base_damage": 16,
                    "element": Element.POISON,
                    "description": "A lâmina pinga um líquido verde e corrosivo.",
                }
            ]
        },
        "Hidra Venenosa": {  # grimoire
            "grimoire": [
                {
                    "name": "Grimório Pestilento",
                    "element": Element.POISON,
                    "magic_power": 24,
                    "mana_cost": 9,
                    "description": "Cheira a morte e decadência. Suas magias adoecem o alvo.",
                }
            ]
        },
        "Sapo Venenoso": {  # ranged_weapon (ANTES ERA Slime Corrosivo)
            "ranged_weapon": [
                {
                    "name": "Lançador Corrosivo",
                    "base_damage": 18,
                    "ammo_required": 1,
                    "element": Element.POISON,
                    "description": "Arco rudimentar banhado em ácido de Slime.",
                }
            ]
        },
        # Drop Neutral items
        "Goblin": {  # weapon
            "weapon": [
                {
                    "name": "Adaga Rústica",
                    "base_damage": 12,
                    "element": Element.NEUTRAL,
                    "description": "Arma lascada e suja, mas perigosamente afiada.",
                }
            ]
        },
        "Orc": {  # grimoire
            "grimoire": [
                {
                    "name": "Tomo Profano",
                    "element": Element.NEUTRAL,
                    "magic_power": 22,
                    "mana_cost": 6,
                    "description": "Escrito em sangue, canaliza magia bruta e sem refinamento.",
                }
            ]
        },
        "Bandido Sombrio": {  # ranged_weapon
            "ranged_weapon": [
                {
                    "name": "Besta Sombria",
                    "base_damage": 23,
                    "ammo_required": 1,
                    "element": Element.NEUTRAL,
                    "description": "Uma besta pesada usada por assassinos nas sombras.",
                }
            ]
        },
    }

    # Returns the full list: fixed drops (potions) + equipment drop.
    @staticmethod
    def get_loot_for_monster(monster_name: str) -> list:
        """
        Returns the complete loot list for a defeated monster.

        Always includes the fixed drops (healing + mana potions).
        Appends the monster-specific equipment drop when defined.

        Args:
            monster_name: The exact name stored in monster.name.

        Returns:
            List of instantiated Item objects ready to be added to inventory.
        """
        loot = ItemsFactory._fixed_drops()

        equipment_config = ItemsFactory.DROP_TABLES.get(monster_name, {})
        if equipment_config:
            loot += ItemsFactory.create_items_from_config(equipment_config)

        return loot

    # Basic items for hero sobrevivation
    @staticmethod
    def get_base_packs() -> dict:
        """Base items for starter inventory."""
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
                    recovery_type="mana",
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

    @staticmethod
    def create_items_from_config(items_config: dict) -> list:
        """
        Creates and returns a list of instantiated item objects
        based on a configuration dictionary.
        """
        created_items = []

        for item_type, configs in items_config.items():
            if item_type not in ItemsFactory.ITEM_REGISTRY:
                raise ValueError(f"Tipo de item desconhecido: {item_type}")

            item_class = ItemsFactory.ITEM_REGISTRY[item_type]

            for config in configs:
                created_items.append(item_class(**config))

        return created_items

    @staticmethod
    def get_predefined_drop_table(monster_name: str) -> dict:
        """Returns the raw config dict for a monster (without fixed drops)."""
        return ItemsFactory.DROP_TABLES.get(monster_name, {})
