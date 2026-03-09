import pytest

from services.items_factory import ItemsFactory
from domain.weapon import Weapon
from domain.ranged_weapon import RangedWeapon
from domain.grimoire import Grimoire
from domain.consumable_item import ConsumableItem
from domain.element import Element
from unittest.mock import patch


def test_base_packs_return_dict():
    packs = ItemsFactory.get_base_packs()

    assert isinstance(packs, dict)
    assert "base_pack_warrior" in packs
    assert "base_pack_mage" in packs
    assert "base_pack_archer" in packs


def test_base_packs_return_new_instances():
    packs1 = ItemsFactory.get_base_packs()
    packs2 = ItemsFactory.get_base_packs()

    assert packs1["base_pack_warrior"][0] is not packs2["base_pack_warrior"][0]
    assert packs1["base_pack_mage"][0] is not packs2["base_pack_mage"][0]


def test_base_pack_contains_correct_types():
    packs = ItemsFactory.get_base_packs()

    warrior_items = packs["base_pack_warrior"]
    assert any(isinstance(item, Weapon) for item in warrior_items)

    mage_items = packs["base_pack_mage"]
    assert any(isinstance(item, Grimoire) for item in mage_items)

    archer_items = packs["base_pack_archer"]
    assert any(isinstance(item, RangedWeapon) for item in archer_items)


def test_base_pack_archer_has_ammo_required():
    packs = ItemsFactory.get_base_packs()
    archer_items = packs["base_pack_archer"]

    ranged = next(item for item in archer_items if isinstance(item, RangedWeapon))

    assert ranged.ammo_required > 0


def test_base_pack_mage_grimoire_has_element_and_mana():
    packs = ItemsFactory.get_base_packs()
    mage_items = packs["base_pack_mage"]

    grimoire = next(item for item in mage_items if isinstance(item, Grimoire))

    assert isinstance(grimoire.element, Element)
    assert grimoire.mana_cost > 0
    assert grimoire.magic_power > 0


def test_create_items_from_valid_config_weapon_and_consumable():
    config = {
        "weapon": [{"name": "Espada Teste", "base_damage": 10}],
        "consumable": [
            {
                "name": "Poção Teste",
                "description": "Recupera 10",
                "weight": 0.5,
                "recovered_value": 10,
            }
        ],
    }

    items = ItemsFactory.create_items_from_config(config)

    assert len(items) == 2
    assert any(isinstance(item, Weapon) for item in items)
    assert any(isinstance(item, ConsumableItem) for item in items)


def test_create_items_from_valid_grimoire_config():
    config = {
        "grimoire": [
            {
                "name": "Grimório Teste",
                "element": Element.FIRE,
                "magic_power": 20,
                "mana_cost": 5,
            }
        ]
    }

    items = ItemsFactory.create_items_from_config(config)

    assert len(items) == 1
    assert isinstance(items[0], Grimoire)
    assert items[0].element == Element.FIRE
    assert items[0].magic_power == 20
    assert items[0].mana_cost == 5


def test_create_items_from_valid_ranged_config():
    config = {
        "ranged_weapon": [{"name": "Arco Teste", "base_damage": 15, "ammo_required": 2}]
    }

    items = ItemsFactory.create_items_from_config(config)

    assert len(items) == 1
    assert isinstance(items[0], RangedWeapon)
    assert items[0].ammo_required == 2


def test_create_items_invalid_type_raises():
    config = {"invalid_type": [{"name": "Bug"}]}

    with pytest.raises(ValueError):
        ItemsFactory.create_items_from_config(config)


def test_every_monster_has_drop_table():
    expected_monsters = [
        "Salamandra",
        "Demônio Ígneo",
        "Espírito Vulcânico",
        "Golem de Gelo",
        "Lobo Glacial",
        "Espectro Congelado",
        "Serpente Elétrica",
        "Raijin",
        "Elemental de Raio",
        "Aranha Tóxica",
        "Hidra Venenosa",
        "Slime Corrosivo",
        "Goblin",
        "Orc",
        "Bandido Sombrio",
    ]

    for monster in expected_monsters:
        drop = ItemsFactory.get_predefined_drop_table(monster)
        assert drop != {}


def test_all_drop_tables_have_valid_structure():
    for monster_name, drop_config in ItemsFactory.DROP_TABLES.items():
        assert isinstance(drop_config, dict)

        items = ItemsFactory.create_items_from_config(drop_config)

        assert isinstance(items, list)
        assert len(items) > 0


def test_all_ranged_drops_have_ammo():
    for monster_name, drop_config in ItemsFactory.DROP_TABLES.items():
        items = ItemsFactory.create_items_from_config(drop_config)

        for item in items:
            if isinstance(item, RangedWeapon):
                assert item.ammo_required > 0


def test_grimoire_drops_have_element_and_mana():
    for monster_name, drop_config in ItemsFactory.DROP_TABLES.items():
        items = ItemsFactory.create_items_from_config(drop_config)

        for item in items:
            if isinstance(item, Grimoire):
                assert isinstance(item.element, Element)
                assert item.mana_cost > 0
                assert item.magic_power > 0


# Tests for balancing of itens and drops


@patch("services.items_factory.random.random", return_value=0.1)
def test_get_loot_for_monster_always_contains_fixed_drops(mock_random):
    """Every monster must drop a Health Potion and a Mana Potion."""
    loot = ItemsFactory.get_loot_for_monster("Goblin")

    names = [item.name for item in loot]
    assert "Poção De Cura" in names
    assert "Poção De Mana" in names


def test_get_loot_for_monster_known_includes_equipment():
    """Monsters with an entry in DROP_TABLES must drop equipment in addition to potions."""
    loot = ItemsFactory.get_loot_for_monster("Salamandra")

    equipment = [item for item in loot if not isinstance(item, ConsumableItem)]
    assert len(equipment) >= 1


@patch("services.items_factory.random.random", return_value=0.1)
def test_get_loot_for_monster_unknown_returns_only_fixed_drops(mock_random):
    """Unknown monsters (boss-generated, for example) only receive the fixed potions"""
    loot = ItemsFactory.get_loot_for_monster("Monstro Inexistente")

    assert len(loot) == len(ItemsFactory._fixed_drops())
    assert all(isinstance(item, ConsumableItem) for item in loot)


@patch("services.items_factory.random.random", return_value=0.1)
def test_get_loot_for_monster_returns_independent_lists(mock_random):
    """
    Two calls to the same monster must not share the same list nor the same objects
    this prevents cross-mutation between fights.
    """
    loot_a = ItemsFactory.get_loot_for_monster("Orc")
    loot_b = ItemsFactory.get_loot_for_monster("Orc")

    assert loot_a is not loot_b
    # The fixed potion objects must not be the same instance.
    assert loot_a[0] is not loot_b[0]


@patch("services.items_factory.random.random", return_value=0.1)
def test_get_loot_for_monster_all_known_monsters(mock_random):
    """All monsters in DROP_TABLES return loot with at least 3 items (2 potions + 1 equipment)."""
    for monster_name in ItemsFactory.DROP_TABLES:
        loot = ItemsFactory.get_loot_for_monster(monster_name)
        assert len(loot) >= 3, (
            f"{monster_name} deveria ter pelo menos 3 itens no loot, mas tem {len(loot)}"
        )


@patch("services.items_factory.random.random", return_value=0.1)
def test_drop_distribution_is_balanced(mock_random):
    """
    Each equipment type (weapon, ranged_weapon, grimoire) must have exactly 5 associated monsters."
    """
    counts = {"weapon": 0, "ranged_weapon": 0, "grimoire": 0}

    for drop_config in ItemsFactory.DROP_TABLES.values():
        for item_type in counts:
            if item_type in drop_config:
                counts[item_type] += 1

    assert counts["weapon"] == 5, f"weapons: esperado 5, encontrado {counts['weapon']}"
    assert counts["ranged_weapon"] == 5, (
        f"ranged_weapons: esperado 5, encontrado {counts['ranged_weapon']}"
    )
    assert counts["grimoire"] == 5, (
        f"grimoires: esperado 5, encontrado {counts['grimoire']}"
    )


@patch("services.items_factory.random.random", return_value=0.1)
def test_fixed_drops_mana_potion_has_correct_recovery_type(mock_random):
    """Mana potion in the fixed drops should have recovery_type='mana'."""
    drops = ItemsFactory._fixed_drops()
    mana_potions = [
        item
        for item in drops
        if isinstance(item, ConsumableItem) and "Mana" in item.name
    ]
    assert len(mana_potions) == 1
    assert mana_potions[0].recovery_type == "mana"


@patch("services.items_factory.random.random", return_value=0.1)
def test_fixed_drops_life_potion_has_correct_recovery_type(mock_random):
    """Healing potion in the fixed drops should have recovery_type='life'."""
    drops = ItemsFactory._fixed_drops()
    life_potions = [
        item
        for item in drops
        if isinstance(item, ConsumableItem) and "Cura" in item.name
    ]
    assert len(life_potions) == 1
    assert life_potions[0].recovery_type == "life"


def test_base_pack_mage_mana_potion_has_correct_recovery_type():
    """Mana potion in the Mage's starting pack should have recovery_type='mana'."""
    packs = ItemsFactory.get_base_packs()
    mage_items = packs["base_pack_mage"]
    mana_potions = [
        item
        for item in mage_items
        if isinstance(item, ConsumableItem) and item.recovery_type == "mana"
    ]
    assert len(mana_potions) >= 1


def test_warrior_base_pack_has_no_mana_potion():
    """Warrior's starting pack should not contain a mana potion."""
    packs = ItemsFactory.get_base_packs()
    warrior_items = packs["base_pack_warrior"]
    mana_potions = [
        item
        for item in warrior_items
        if isinstance(item, ConsumableItem) and item.recovery_type == "mana"
    ]
    assert len(mana_potions) == 0


def test_archer_base_pack_has_no_mana_potion():
    """Archer's starting pack should not contain a mana potion."""
    packs = ItemsFactory.get_base_packs()
    archer_items = packs["base_pack_archer"]
    mana_potions = [
        item
        for item in archer_items
        if isinstance(item, ConsumableItem) and item.recovery_type == "mana"
    ]
    assert len(mana_potions) == 0
