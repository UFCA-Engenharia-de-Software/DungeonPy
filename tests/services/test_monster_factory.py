import pytest
from services.monster_factory import MonsterFactory
from domain.element import Element
from domain.monster import Monster
from domain.weapon import Weapon
from domain.ranged_weapon import RangedWeapon
from domain.grimoire import Grimoire
from unittest.mock import patch


def test_create_monster_returns_instance():
    monster = MonsterFactory.create_monster(level=1)

    assert isinstance(monster, Monster)


def test_monster_scaling_attributes():
    level = 3
    monster = MonsterFactory.create_monster(level=level)

    assert monster.max_life == 55 + (level * 10)
    assert monster.attack == 8 + (level * 5)
    assert monster.speed == 5 + level


def test_create_monster_with_specific_element():
    monster = MonsterFactory.create_monster(level=2, element=Element.FIRE)

    assert monster.element == Element.FIRE


def test_invalid_level_raises_error():
    with pytest.raises(ValueError):
        MonsterFactory.create_monster(level=0)


def test_create_boss_is_stronger_than_normal():
    level = 5
    normal = MonsterFactory.create_monster(level=level, element=Element.ICE)
    boss = MonsterFactory.create_boss(level=level, element=Element.ICE)

    assert boss.max_life > normal.max_life
    assert boss.attack > normal.attack
    assert boss.speed >= normal.speed


# =============================================================================
# NOVOS TESTES — cobrem o vínculo Monster ↔ ItemsFactory
# =============================================================================


def test_monster_loot_is_populated_on_creation():
    """Monstro criado pela factory não deve ter loot vazio."""
    monster = MonsterFactory.create_monster(level=1, element=Element.FIRE)

    assert len(monster.loot) > 0


@patch("services.items_factory.random.random", return_value=0.1)
def test_monster_loot_contains_healing_potion(mock_random):
    """Todo monstro deve carregar Poção de Cura no loot."""
    monster = MonsterFactory.create_monster(level=1, element=Element.POISON)

    names = [item.name for item in monster.loot]
    assert "Poção De Cura" in names


@patch("services.items_factory.random.random", return_value=0.1)
def test_monster_loot_contains_mana_potion(mock_random):
    """Todo monstro deve carregar Poção de Mana no loot."""
    monster = MonsterFactory.create_monster(level=1, element=Element.LIGHTNING)

    names = [item.name for item in monster.loot]
    assert "Poção De Mana" in names


def test_monster_loot_contains_equipment():
    """
    Além das poções fixas, o monstro deve carregar ao menos
    um equipamento (weapon, ranged ou grimoire).
    """
    # Força um monstro cujo nome está garantido no DROP_TABLES
    monster = MonsterFactory.create_monster(level=2, element=Element.NEUTRAL)

    equipment = [
        item
        for item in monster.loot
        if isinstance(item, (Weapon, RangedWeapon, Grimoire))
    ]
    assert len(equipment) >= 1


def test_get_loot_only_after_death():
    """
    monster.get_loot() deve retornar itens apenas quando o monstro
    está morto, seguindo o contrato de Monster.get_loot().
    """
    monster = MonsterFactory.create_monster(level=1, element=Element.ICE)

    # Monstro vivo não entrega loot
    assert monster.get_loot() == []

    # Mata o monstro manualmente
    monster.current_life = 0

    assert len(monster.get_loot()) > 0


@patch("services.items_factory.random.random", return_value=0.1)
def test_boss_loot_contains_fixed_drops(mock_random):
    """Boss deve receber ao menos as poções fixas no loot."""
    boss = MonsterFactory.create_boss(level=3, element=Element.FIRE)

    names = [item.name for item in boss.loot]
    assert "Poção De Cura" in names
    assert "Poção De Mana" in names


def test_two_monsters_have_independent_loot_lists():
    """
    Dois monstros do mesmo tipo não devem compartilhar a lista de loot
    nem os mesmos objetos — mutação em um não afeta o outro.
    """
    m1 = MonsterFactory.create_monster(level=1, element=Element.NEUTRAL)
    m2 = MonsterFactory.create_monster(level=1, element=Element.NEUTRAL)

    assert m1.loot is not m2.loot
    assert m1.loot[0] is not m2.loot[0]


def test_all_elements_produce_monsters_with_loot():
    """Criar um monstro de cada elemento deve sempre gerar loot populado."""
    for element in Element:
        monster = MonsterFactory.create_monster(level=1, element=element)
        assert len(monster.loot) > 0, (
            f"Monstro do elemento {element.name} foi criado sem loot."
        )
