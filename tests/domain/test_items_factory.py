import pytest

from services.items_factory import ItemsFactory
from domain.weapon import Weapon
from domain.ranged_weapon import RangedWeapon
from domain.grimoire import Grimoire
from domain.consumable_item import ConsumableItem
from domain.element import Element


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
