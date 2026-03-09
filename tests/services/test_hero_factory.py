import pytest

from services.hero_factory import (
    ARCHER_STATS,
    MAGE_STATS,
    VALID_ARCHETYPES,
    WARRIOR_STATS,
    HeroFactory,
)
from domain.warrior import Warrior
from domain.mage import Mage
from domain.archer import Archer
from domain.hero import Hero
from domain.element import Element
from domain.inventory import Inventory


# ======================================================================
# get_class_differentials
# ======================================================================


class TestGetClassDifferentials:
    """Tests for the get_class_differentials method."""

    def test_returns_dict(self):
        result = HeroFactory.get_class_differentials()
        assert isinstance(result, dict)

    def test_contains_all_archetypes(self):
        result = HeroFactory.get_class_differentials()
        assert "warrior" in result
        assert "mage" in result
        assert "archer" in result

    def test_warrior_has_expected_keys(self):
        warrior = HeroFactory.get_class_differentials()["warrior"]
        expected_keys = {
            "description",
            "stats",
            "element",
            "special_abilities",
            "upgradeable_attributes",
        }
        assert set(warrior.keys()) == expected_keys

    def test_warrior_stats_match_constants(self):
        stats = HeroFactory.get_class_differentials()["warrior"]["stats"]
        assert stats["max_life"] == WARRIOR_STATS["max_life"]
        assert stats["attack"] == WARRIOR_STATS["attack"]
        assert stats["speed"] == WARRIOR_STATS["speed"]
        assert stats["shield"] == WARRIOR_STATS["shield"]
        assert stats["armor"] == WARRIOR_STATS["armor"]

    def test_warrior_special_abilities(self):
        warrior = HeroFactory.get_class_differentials()["warrior"]
        assert "to_rage" in warrior["special_abilities"]
        assert "defend" in warrior["special_abilities"]

    def test_warrior_upgradeable_attributes(self):
        warrior = HeroFactory.get_class_differentials()["warrior"]
        assert "shield" in warrior["upgradeable_attributes"]
        assert "armor" in warrior["upgradeable_attributes"]

    def test_warrior_element_is_neutral(self):
        warrior = HeroFactory.get_class_differentials()["warrior"]
        assert warrior["element"] == Element.NEUTRAL.value

    def test_mage_stats_match_constants(self):
        mage = HeroFactory.get_class_differentials()["mage"]
        assert mage["stats"]["max_life"] == MAGE_STATS["max_life"]
        assert mage["stats"]["attack"] == MAGE_STATS["attack"]
        assert mage["stats"]["speed"] == MAGE_STATS["speed"]
        assert mage["stats"]["max_mana"] == MAGE_STATS["max_mana"]

    def test_mage_special_abilities(self):
        mage = HeroFactory.get_class_differentials()["mage"]
        assert "meditate" in mage["special_abilities"]
        assert "ancient_magic" in mage["special_abilities"]
        assert "heavy_strike" in mage["special_abilities"]

    def test_mage_upgradeable_attributes(self):
        mage = HeroFactory.get_class_differentials()["mage"]
        assert "attack" in mage["upgradeable_attributes"]
        assert "max_mana" in mage["upgradeable_attributes"]

    def test_mage_element_is_neutral(self):
        mage = HeroFactory.get_class_differentials()["mage"]
        assert mage["element"] == Element.NEUTRAL.value

    def test_archer_stats_match_constants(self):
        archer = HeroFactory.get_class_differentials()["archer"]
        assert archer["stats"]["max_life"] == ARCHER_STATS["max_life"]
        assert archer["stats"]["attack"] == ARCHER_STATS["attack"]
        assert archer["stats"]["speed"] == ARCHER_STATS["speed"]
        assert archer["stats"]["max_ammo"] == ARCHER_STATS["max_ammo"]

    def test_archer_special_abilities(self):
        archer = HeroFactory.get_class_differentials()["archer"]
        assert "aim" in archer["special_abilities"]
        assert "reload" in archer["special_abilities"]
        assert "dodge" in archer["special_abilities"]

    def test_archer_upgradeable_attributes(self):
        archer = HeroFactory.get_class_differentials()["archer"]
        assert "speed" in archer["upgradeable_attributes"]
        assert "max_ammo" in archer["upgradeable_attributes"]
        assert "attack" in archer["upgradeable_attributes"]

    def test_archer_element_is_neutral(self):
        archer = HeroFactory.get_class_differentials()["archer"]
        assert archer["element"] == Element.NEUTRAL.value


# ======================================================================
# get_base_packs
# ======================================================================


class TestGetBasePacks:
    """Tests for the get_base_packs method."""

    def test_returns_dict(self):
        result = HeroFactory.get_base_packs()
        assert isinstance(result, dict)

    def test_contains_warrior_key(self):
        result = HeroFactory.get_base_packs()
        assert "base_pack_warrior" in result

    def test_contains_mage_key(self):
        result = HeroFactory.get_base_packs()
        assert "base_pack_mage" in result

    def test_contains_archer_key(self):
        result = HeroFactory.get_base_packs()
        assert "base_pack_archer" in result

    def test_warrior_pack_is_list(self):
        result = HeroFactory.get_base_packs()
        assert isinstance(result["base_pack_warrior"], list)

    def test_mage_pack_is_list(self):
        result = HeroFactory.get_base_packs()
        assert isinstance(result["base_pack_mage"], list)

    def test_archer_pack_is_list(self):
        result = HeroFactory.get_base_packs()
        assert isinstance(result["base_pack_archer"], list)


# ======================================================================
# create_hero — Warrior
# ======================================================================


class TestCreateWarrior:
    """Tests for creating a Warrior via create_hero."""

    def test_returns_warrior_instance(self):
        hero = HeroFactory.create_hero("warrior", "Arthur")
        assert isinstance(hero, Warrior)

    def test_is_hero_instance(self):
        hero = HeroFactory.create_hero("warrior", "Arthur")
        assert isinstance(hero, Hero)

    def test_has_correct_name(self):
        hero = HeroFactory.create_hero("warrior", "Arthur")
        assert hero.name == "Arthur"

    def test_has_balanced_max_life(self):
        hero = HeroFactory.create_hero("warrior", "Arthur")
        assert hero.max_life == WARRIOR_STATS["max_life"]

    def test_current_life_equals_max(self):
        hero = HeroFactory.create_hero("warrior", "Arthur")
        assert hero.current_life == hero.max_life

    def test_has_balanced_attack(self):
        hero = HeroFactory.create_hero("warrior", "Arthur")
        assert hero.attack == WARRIOR_STATS["attack"]

    def test_has_balanced_speed(self):
        hero = HeroFactory.create_hero("warrior", "Arthur")
        assert hero.speed == WARRIOR_STATS["speed"]

    def test_has_balanced_shield(self):
        hero = HeroFactory.create_hero("warrior", "Arthur")
        assert hero.shield == WARRIOR_STATS["shield"]

    def test_has_balanced_armor(self):
        hero = HeroFactory.create_hero("warrior", "Arthur")
        assert hero.armor == WARRIOR_STATS["armor"]

    def test_has_correct_element(self):
        hero = HeroFactory.create_hero("warrior", "Arthur")
        assert hero.element == WARRIOR_STATS["element"]

    def test_has_inventory(self):
        hero = HeroFactory.create_hero("warrior", "Arthur")
        assert isinstance(hero.inventory, Inventory)


# ======================================================================
# create_hero — Mage
# ======================================================================


class TestCreateMage:
    """Tests for creating a Mage via create_hero."""

    def test_returns_mage_instance(self):
        hero = HeroFactory.create_hero("mage", "Gandalf")
        assert isinstance(hero, Mage)

    def test_is_hero_instance(self):
        hero = HeroFactory.create_hero("mage", "Gandalf")
        assert isinstance(hero, Hero)

    def test_has_correct_name(self):
        hero = HeroFactory.create_hero("mage", "Gandalf")
        assert hero.name == "Gandalf"

    def test_has_balanced_max_life(self):
        hero = HeroFactory.create_hero("mage", "Gandalf")
        assert hero.max_life == MAGE_STATS["max_life"]

    def test_current_life_equals_max(self):
        hero = HeroFactory.create_hero("mage", "Gandalf")
        assert hero.current_life == hero.max_life

    def test_has_balanced_attack(self):
        hero = HeroFactory.create_hero("mage", "Gandalf")
        assert hero.attack == MAGE_STATS["attack"]

    def test_has_balanced_speed(self):
        hero = HeroFactory.create_hero("mage", "Gandalf")
        assert hero.speed == MAGE_STATS["speed"]

    def test_has_balanced_max_mana(self):
        hero = HeroFactory.create_hero("mage", "Gandalf")
        assert hero.max_mana == MAGE_STATS["max_mana"]

    def test_has_balanced_current_mana(self):
        hero = HeroFactory.create_hero("mage", "Gandalf")
        assert hero.current_mana == MAGE_STATS["current_mana"]

    def test_has_correct_element(self):
        hero = HeroFactory.create_hero("mage", "Gandalf")
        assert hero.element == MAGE_STATS["element"]

    def test_has_inventory(self):
        hero = HeroFactory.create_hero("mage", "Gandalf")
        assert isinstance(hero.inventory, Inventory)


# ======================================================================
# create_hero — Archer
# ======================================================================


class TestCreateArcher:
    """Tests for creating an Archer via create_hero."""

    def test_returns_archer_instance(self):
        hero = HeroFactory.create_hero("archer", "Legolas")
        assert isinstance(hero, Archer)

    def test_is_hero_instance(self):
        hero = HeroFactory.create_hero("archer", "Legolas")
        assert isinstance(hero, Hero)

    def test_has_correct_name(self):
        hero = HeroFactory.create_hero("archer", "Legolas")
        assert hero.name == "Legolas"

    def test_has_balanced_max_life(self):
        hero = HeroFactory.create_hero("archer", "Legolas")
        assert hero.max_life == ARCHER_STATS["max_life"]

    def test_current_life_equals_max(self):
        hero = HeroFactory.create_hero("archer", "Legolas")
        assert hero.current_life == hero.max_life

    def test_has_balanced_attack(self):
        hero = HeroFactory.create_hero("archer", "Legolas")
        assert hero.attack == ARCHER_STATS["attack"]

    def test_has_balanced_speed(self):
        hero = HeroFactory.create_hero("archer", "Legolas")
        assert hero.speed == ARCHER_STATS["speed"]

    def test_has_balanced_max_ammo(self):
        hero = HeroFactory.create_hero("archer", "Legolas")
        assert hero.max_ammo == ARCHER_STATS["max_ammo"]

    def test_has_balanced_current_ammo(self):
        hero = HeroFactory.create_hero("archer", "Legolas")
        assert hero.current_ammo == ARCHER_STATS["current_ammo"]

    def test_has_correct_element(self):
        hero = HeroFactory.create_hero("archer", "Legolas")
        assert hero.element == ARCHER_STATS["element"]

    def test_has_inventory(self):
        hero = HeroFactory.create_hero("archer", "Legolas")
        assert isinstance(hero.inventory, Inventory)


# ======================================================================
# create_hero — General behavior
# ======================================================================


class TestCreateHeroGeneral:
    """Tests for general create_hero behavior."""

    def test_case_insensitive(self):
        assert isinstance(HeroFactory.create_hero("WARRIOR", "X"), Warrior)
        assert isinstance(HeroFactory.create_hero("MAGE", "X"), Mage)
        assert isinstance(HeroFactory.create_hero("ARCHER", "X"), Archer)

    def test_mixed_case(self):
        assert isinstance(HeroFactory.create_hero("Warrior", "X"), Warrior)
        assert isinstance(HeroFactory.create_hero("Mage", "X"), Mage)
        assert isinstance(HeroFactory.create_hero("Archer", "X"), Archer)

    def test_strips_whitespace(self):
        assert isinstance(HeroFactory.create_hero("  warrior  ", "X"), Warrior)

    def test_invalid_archetype_raises_value_error(self):
        with pytest.raises(ValueError, match="Invalid archetype"):
            HeroFactory.create_hero("paladin", "Arthur")

    def test_empty_archetype_raises_value_error(self):
        with pytest.raises(ValueError):
            HeroFactory.create_hero("", "Arthur")

    def test_created_heroes_are_independent_instances(self):
        hero1 = HeroFactory.create_hero("warrior", "Arthur")
        hero2 = HeroFactory.create_hero("warrior", "Lancelot")
        assert hero1 is not hero2
        assert hero1.name != hero2.name

    def test_created_heroes_have_independent_inventories(self):
        hero1 = HeroFactory.create_hero("warrior", "Arthur")
        hero2 = HeroFactory.create_hero("warrior", "Lancelot")
        assert hero1.inventory is not hero2.inventory

    def test_different_archetypes_return_different_types(self):
        w = HeroFactory.create_hero("warrior", "W")
        m = HeroFactory.create_hero("mage", "M")
        a = HeroFactory.create_hero("archer", "A")
        assert type(w) is not type(m)
        assert type(m) is not type(a)
        assert type(w) is not type(a)


# ======================================================================
# Constants
# ======================================================================


class TestConstants:
    """Tests for the balancing constants."""

    def test_valid_archetypes_contains_all(self):
        assert "warrior" in VALID_ARCHETYPES
        assert "mage" in VALID_ARCHETYPES
        assert "archer" in VALID_ARCHETYPES

    def test_warrior_stats_has_required_keys(self):
        required = {"max_life", "attack", "speed", "shield", "armor", "element"}
        assert required.issubset(set(WARRIOR_STATS.keys()))

    def test_mage_stats_has_required_keys(self):
        required = {
            "max_life",
            "attack",
            "speed",
            "max_mana",
            "current_mana",
            "element",
        }
        assert required.issubset(set(MAGE_STATS.keys()))

    def test_archer_stats_has_required_keys(self):
        required = {
            "max_life",
            "attack",
            "speed",
            "max_ammo",
            "current_ammo",
            "element",
        }
        assert required.issubset(set(ARCHER_STATS.keys()))

    def test_warrior_stats_values_are_positive(self):
        assert WARRIOR_STATS["max_life"] > 0
        assert WARRIOR_STATS["attack"] > 0
        assert WARRIOR_STATS["speed"] > 0
        assert WARRIOR_STATS["shield"] >= 0
        assert WARRIOR_STATS["armor"] >= 0

    def test_mage_stats_values_are_positive(self):
        assert MAGE_STATS["max_life"] > 0
        assert MAGE_STATS["attack"] > 0
        assert MAGE_STATS["speed"] > 0
        assert MAGE_STATS["max_mana"] > 0

    def test_archer_stats_values_are_positive(self):
        assert ARCHER_STATS["max_life"] > 0
        assert ARCHER_STATS["attack"] > 0
        assert ARCHER_STATS["speed"] > 0
        assert ARCHER_STATS["max_ammo"] > 0

    def test_warrior_element_is_valid(self):
        assert isinstance(WARRIOR_STATS["element"], Element)

    def test_mage_element_is_valid(self):
        assert isinstance(MAGE_STATS["element"], Element)

    def test_archer_element_is_valid(self):
        assert isinstance(ARCHER_STATS["element"], Element)
