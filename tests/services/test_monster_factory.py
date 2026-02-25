import pytest
from services.monster_factory import MonsterFactory
from domain.element import Element
from domain.monster import Monster


def test_create_monster_returns_instance():
    monster = MonsterFactory.create_monster(level=1)

    assert isinstance(monster, Monster)


def test_monster_scaling_attributes():
    level = 3
    monster = MonsterFactory.create_monster(level=level)

    assert monster.max_life == 50 + (level * 15)
    assert monster.attack == 10 + (level * 5)
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
