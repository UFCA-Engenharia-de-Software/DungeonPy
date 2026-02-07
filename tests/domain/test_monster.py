import pytest

from domain.element import Element
from domain.monster import Monster


def test_monster_creation() -> None:
    """Test basic monster creation"""
    monster: Monster = Monster(
        name="Fire Dragon",
        max_life=100,
        attack=25,
        speed=10,
        element=Element.FIRE,
        loot=["Dragon Scale"],
        description="A fierce dragon",
    )

    assert monster.name == "Fire Dragon"
    assert monster.max_life == 100
    assert monster.current_life == 100
    assert monster.attack == 25
    assert monster.speed == 10
    assert monster.element == Element.FIRE


def test_monster_strike() -> None:
    """Test that monster can attack other entities"""
    attacker: Monster = Monster("Orc", 100, 20, 10, Element.NEUTRAL)
    target: Monster = Monster("Goblin", 50, 5, 5, Element.NEUTRAL)

    attacker.strike(target)

    assert target.current_life == 30


def test_strike_with_elemental_advantage() -> None:
    """Test elemental advantage in combat"""
    fire_monster: Monster = Monster("Fire Dragon", 100, 20, 10, Element.FIRE)
    poison_monster: Monster = Monster("Poison Spider", 100, 10, 8, Element.POISON)

    fire_monster.strike(poison_monster)

    # 20 damage * 2 = 40 damage
    assert poison_monster.current_life == 60


def test_get_loot_when_alive() -> None:
    """Test that alive monsters don't drop loot"""
    monster: Monster = Monster(
        name="Dragon",
        max_life=100,
        attack=30,
        speed=10,
        element=Element.FIRE,
        loot=["Dragon Scale", "Gold"],
    )

    assert monster.is_it_alive()
    assert monster.get_loot() == []


def test_get_loot_when_dead() -> None:
    """Test that dead monsters drop loot"""
    monster: Monster = Monster(
        name="Zombie",
        max_life=50,
        attack=10,
        speed=5,
        element=Element.POISON,
        loot=["Rotten Flesh", "Bone"],
    )

    monster.current_life = 0

    assert not monster.is_it_alive()
    assert monster.get_loot() == ["Rotten Flesh", "Bone"]


def test_get_description() -> None:
    """Test description (DescriptionMixin implementation)"""
    monster1: Monster = Monster(
        "Ancient Dragon", 500, 80, 20, Element.FIRE, description="An ancient dragon"
    )
    assert monster1.get_description() == "An ancient dragon"

    monster2: Monster = Monster("Ice Wolf", 70, 18, 12, Element.ICE)
    assert "Ice Wolf" in monster2.get_description()
    assert "ice" in monster2.get_description()


def test_loot_setter_type_error() -> None:
    """Test that setting loot with invalid type raises TypeError"""
    monster: Monster = Monster("Orc", 100, 20, 10, Element.NEUTRAL)

    with pytest.raises(TypeError):
        monster.loot = "Invalid Loot String"

    with pytest.raises(TypeError):
        monster.loot = 123


def test_monster_name_validation_errors() -> None:
    """Test that invalid names raise appropriate errors"""
    with pytest.raises(TypeError):
        Monster(name=123, max_life=100, attack=20, speed=10, element=Element.FIRE)

    with pytest.raises(ValueError):
        Monster(name="", max_life=100, attack=20, speed=10, element=Element.FIRE)


def test_monster_invalid_element() -> None:
    """Test that invalid element type raises TypeError"""
    with pytest.raises(TypeError):
        Monster(
            name="Invalid Monster", max_life=100, attack=20, speed=10, element="fire"
        )


def test_monster_creation_with_defaults() -> None:
    """Test monster creation with default loot and description"""
    monster: Monster = Monster(
        name="Simple Slime", max_life=50, attack=5, speed=3, element=Element.NEUTRAL
    )

    assert monster.name == "Simple Slime"
    assert monster.loot == []
    assert "Simple Slime" in monster.get_description()


def test_strike_with_elemental_resistance() -> None:
    """Test elemental resistance in combat (0.5x damage)"""
    # POISON is resisted by FIRE (0.5x damage)
    poison_monster: Monster = Monster("Poison Spider", 100, 20, 10, Element.POISON)
    fire_monster: Monster = Monster("Fire Dragon", 100, 25, 10, Element.FIRE)

    poison_monster.strike(fire_monster)

    # 20 damage * 0.5 = 10 damage
    assert fire_monster.current_life == 90


def test_strike_can_kill_monster() -> None:
    """Test that strike can kill a monster"""
    strong_monster: Monster = Monster("Boss", 200, 100, 15, Element.FIRE)
    weak_monster: Monster = Monster("Slime", 10, 2, 1, Element.NEUTRAL)

    assert weak_monster.is_it_alive()

    strong_monster.strike(weak_monster)

    assert not weak_monster.is_it_alive()
    assert weak_monster.current_life == 0
    # Now can get loot
    assert weak_monster.get_loot() == []  # No loot was set
