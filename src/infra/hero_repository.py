import json
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Optional

from domain.archer import Archer
from domain.consumable_item import ConsumableItem
from domain.element import Element
from domain.grimoire import Grimoire
from domain.hero import Hero
from domain.inventory import Inventory
from domain.item import Item
from domain.mage import Mage
from domain.ranged_weapon import RangedWeapon
from domain.warrior import Warrior
from domain.weapon import Weapon
from services.game_state import GameState

if TYPE_CHECKING:
    from domain.weapon import Weapon

_BASE_DIR = Path(__file__).resolve().parent.parent


class HeroRepository:
    """
    Responsible for GameState persistence in JSON format.

    Serializes and deserializes complete heroes (with inventory and equipped weapons)
    and game state to a single JSON file. The system maintains only one
    save file at a time (savegame.json).

    Attributes:
        SAVE_DIR (Path): Directory where the save file is stored.
        SAVE_FILE (Path): Complete path to the save file (savegame.json).
    """

    SAVE_DIR = _BASE_DIR / "saves"
    SAVE_FILE = SAVE_DIR / "savegame.json"

    """Serialização"""

    @staticmethod
    def _serialize_item(item: Item) -> Dict[str, Any]:
        base_data = {
            "name": item.name,
            "description": item.get_description(),
            "weight": item.weight,
        }

        if isinstance(item, ConsumableItem):
            return {
                "type": "consumable",
                **base_data,
                "recovered_value": item.recovered_value,
            }

        elif isinstance(item, RangedWeapon):
            return {
                "type": "ranged_weapon",
                **base_data,
                "base_damage": item.base_damage,
                "element": item.element.value,
                "ammo_required": item.ammo_required,
                "hit_probability": item.hit_probability,
            }

        elif isinstance(item, Grimoire):
            return {
                "type": "grimoire",
                **base_data,
                "magic_power": item.magic_power,
                "mana_cost": item.mana_cost,
                "element": item.element.value,
            }

        elif isinstance(item, Weapon):
            return {
                "type": "weapon",
                **base_data,
                "base_damage": item.base_damage,
                "element": item.element.value,
            }

        else:
            raise ValueError(f"Tipo de item desconhecido: {type(item)}")

    @staticmethod
    def _serialize_inventory(inventory: Inventory) -> Dict[str, Any]:
        return {
            "capacity": inventory.capacity,
            "items": [HeroRepository._serialize_item(item) for item in inventory.items],
        }

    @staticmethod
    def _serialize_hero(hero: Hero) -> Dict[str, Any]:
        base_data = {
            "name": hero.name,
            "max_life": hero.max_life,
            "current_life": hero.current_life,
            "attack": hero.attack,
            "speed": hero.speed,
            "element": hero.element.value,
            "inventory": HeroRepository._serialize_inventory(hero.inventory),
            "equipped_weapon": (
                HeroRepository._serialize_item(hero.equipped_weapon)
                if hero.equipped_weapon
                else None
            ),
        }

        if isinstance(hero, Warrior):
            return {
                "type": "warrior",
                **base_data,
                "shield": hero.shield,
                "armor": hero.armor,
            }

        elif isinstance(hero, Mage):
            return {
                "type": "mage",
                **base_data,
                "max_mana": hero.max_mana,
                "current_mana": hero.current_mana,
            }

        elif isinstance(hero, Archer):
            return {
                "type": "archer",
                **base_data,
                "max_ammo": hero.max_ammo,
                "current_ammo": hero.current_ammo,
            }

        else:
            raise ValueError(f"Tipo de herói desconhecido: {type(hero)}")

    @staticmethod
    def _serialize_game_state(game_state: GameState) -> Dict[str, Any]:
        return {
            "game_state": game_state.to_dict(),
            "hero": HeroRepository._serialize_hero(game_state.hero),
        }

    """Deserialização"""

    @staticmethod
    def _deserialize_item(data: Dict[str, Any]) -> Item:
        item_type = data["type"]

        if item_type == "consumable":
            return ConsumableItem(
                name=data["name"],
                description=data["description"],
                weight=data["weight"],
                recovered_value=data["recovered_value"],
            )

        elif item_type == "weapon":
            return Weapon(
                name=data["name"],
                base_damage=data["base_damage"],
                description=data["description"],
                weight=data["weight"],
                element=Element(data["element"]),
            )

        elif item_type == "ranged_weapon":
            return RangedWeapon(
                name=data["name"],
                base_damage=data["base_damage"],
                ammo_required=data["ammo_required"],
                hit_probability=data["hit_probability"],
                description=data["description"],
                weight=data["weight"],
                element=Element(data["element"]),
            )

        elif item_type == "grimoire":
            return Grimoire(
                name=data["name"],
                element=Element(data["element"]),
                magic_power=data["magic_power"],
                mana_cost=data["mana_cost"],
                weight=data["weight"],
            )

        else:
            raise ValueError(f"Tipo de item desconhecido: {item_type}")

    @staticmethod
    def _deserialize_inventory(data: Dict[str, Any]) -> Inventory:
        inventory = Inventory(capacity=data["capacity"])

        for item_data in data["items"]:
            try:
                item = HeroRepository._deserialize_item(item_data)
                inventory.add_item_to_inventory(item)
            except (ValueError, KeyError) as e:
                print(f"Aviso: Item corrompido ignorado - {e}")
                continue

        return inventory

    @staticmethod
    def _deserialize_hero(data: Dict[str, Any]) -> Hero:
        hero_type = data["type"]

        inventory = HeroRepository._deserialize_inventory(data["inventory"])

        base_args = {
            "name": data["name"],
            "max_life": data["max_life"],
            "current_life": data["current_life"],
            "attack": data["attack"],
            "speed": data["speed"],
            "element": Element(data["element"]),
            "inventory": inventory,
        }

        if hero_type == "warrior":
            hero = Warrior(**base_args, shield=data["shield"], armor=data["armor"])

        elif hero_type == "mage":
            hero = Mage(
                **base_args,
                max_mana=data["max_mana"],
                current_mana=data["current_mana"],
            )

        elif hero_type == "archer":
            hero = Archer(
                **base_args,
                max_ammo=data["max_ammo"],
                current_ammo=data["current_ammo"],
            )

        else:
            raise ValueError(f"Tipo de herói desconhecido: {hero_type}")

        if data["equipped_weapon"]:
            try:
                weapon = HeroRepository._deserialize_item(data["equipped_weapon"])
                hero.equip_weapon(weapon)  # type: ignore
            except (ValueError, KeyError, TypeError) as e:
                print(f"Aviso: Arma corrompida ignorada - {e}")

        return hero

    @staticmethod
    def _deserialize_game_state(data: Dict[str, Any]) -> GameState:
        hero = HeroRepository._deserialize_hero(data["hero"])
        return GameState.from_dict(data["game_state"], hero)

    """Persistência"""

    def save(self, game_state: GameState) -> None:
        try:
            self.SAVE_DIR.mkdir(exist_ok=True)

            data = self._serialize_game_state(game_state)

            with open(self.SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            raise OSError(f"Erro ao salvar jogo: {e}") from e

    def load(self) -> Optional[GameState]:
        if not self.has_save():
            return None

        try:
            with open(self.SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            return self._deserialize_game_state(data)

        except json.JSONDecodeError as e:
            raise ValueError(f"Save corrompido (JSON inválido): {e}") from e

        except (KeyError, TypeError) as e:
            raise ValueError(f"Save corrompido (dados inválidos): {e}") from e

    def has_save(self) -> bool:
        return self.SAVE_FILE.exists() and self.SAVE_FILE.is_file()

    def delete_save(self) -> None:
        if self.has_save():
            self.SAVE_FILE.unlink()

    def get_save_info(self) -> Optional[Dict[str, Any]]:
        if not self.has_save():
            return None

        try:
            with open(self.SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            game_data = data["game_state"]
            hero_data = data["hero"]

            return {
                "hero_name": hero_data["name"],
                "hero_type": hero_data["type"],
                "current_level": game_data["current_level"],
                "save_date": game_data["save_date"],
                "game_version": game_data["game_version"],
            }

        except (json.JSONDecodeError, KeyError):
            return {"corrupted": True}
