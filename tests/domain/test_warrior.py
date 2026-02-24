from domain.warrior import Warrior
from domain.element import Element
from domain.monster import Monster
from domain.weapon import Weapon


def test_warrior_creation() -> None:
    sample_warrior: Warrior = Warrior(
        name="Errant Knight",
        max_life=200,
        current_life=100,
        attack=20,
        speed=25,
    )

    assert sample_warrior.name == "Errant Knight"
    assert sample_warrior.max_life == 200
    assert sample_warrior.attack == 20
    assert sample_warrior.speed == 25
    assert sample_warrior.element == Element.NEUTRAL


def test_strike() -> None:
    sample_warrior: Warrior = Warrior(
        name="Errant Knight",
        max_life=200,
        current_life=100,
        attack=25,
        speed=25,
    )

    sample_monster: Monster = Monster(
        name="Fire Dragon",
        max_life=100,
        attack=25,
        speed=10,
        element=Element.FIRE,
        loot=["Dragon Scale"],
        description="A fierce dragon",
    )

    weapon = Weapon(name="Sword", base_damage=1)
    sample_warrior.inventory.add_item_to_inventory(weapon)
    sample_warrior.equip_weapon(weapon)

    sample_warrior.strike(sample_monster)

    assert sample_monster.current_life == 74


def test_damage_received():
    sample_warrior: Warrior = Warrior(
        name="Errant Knight",
        max_life=200,
        current_life=100,
        attack=25,
        speed=25,
        shield=10,
        armor=10,
    )

    sample_monster: Monster = Monster(
        name="Fire Dragon",
        max_life=100,
        attack=100,
        speed=10,
        element=Element.FIRE,
        loot=["Dragon Scale"],
        description="A fierce dragon",
    )

    sample_warrior.in_test = True
    sample_monster.strike(sample_warrior)
    assert sample_warrior.current_life == 20
    assert not sample_warrior.defend


def test_negative_damege_untreated():
    """If `shield + armor > final damage`, this would heal the Warrior"""

    sample_warrior: Warrior = Warrior(
        name="Errant Knight",
        max_life=200,
        current_life=100,
        attack=25,
        speed=25,
        shield=10,
        armor=10,
    )

    sample_monster: Monster = Monster(
        name="Fire Dragon",
        max_life=100,
        attack=0,
        speed=10,
        element=Element.FIRE,
        loot=["Dragon Scale"],
        description="A fierce dragon",
    )

    sample_warrior.in_test = True
    sample_monster.strike(sample_warrior)
    assert sample_warrior.current_life == 100
    assert not sample_warrior.defend


def test_defend():
    sample_warrior: Warrior = Warrior(
        name="Errant Knight",
        max_life=200,
        current_life=100,
        attack=25,
        speed=25,
    )

    sample_monster: Monster = Monster(
        name="Fire Dragon",
        max_life=100,
        attack=25,
        speed=10,
        element=Element.FIRE,
        loot=["Dragon Scale"],
        description="A fierce dragon",
    )

    sample_warrior.in_test = True
    sample_warrior.defend = True
    sample_monster.strike(sample_warrior)
    assert sample_warrior.current_life == 100
    assert not sample_warrior.defend


def test_update():
    sample_warrior: Warrior = Warrior(
        name="Errant Knight",
        max_life=200,
        current_life=100,
        attack=25,
        speed=25,
        shield=10,
        armor=10,
    )

    sample_warrior.upgrade(2)
    assert sample_warrior.shield == 11
    assert sample_warrior.armor == 11


def test_rage():
    sample_warrior: Warrior = Warrior(
        name="Errant Knight",
        max_life=200,
        current_life=100,
        attack=25,
        speed=25,
        shield=10,
        armor=10,
    )

    sample_warrior.to_rage()
    assert sample_warrior.in_rage
    assert sample_warrior.attack == 50
    assert sample_warrior.shield == 0
    assert sample_warrior.armor == 0

    sample_warrior.reset_rage()
    assert not sample_warrior.in_rage
    assert sample_warrior.attack == 25
    assert sample_warrior.shield == 10
    assert sample_warrior.armor == 10


def test_get_actions():
    sample_warrior: Warrior = Warrior(
        name="Errant Knight",
        max_life=200,
        current_life=100,
        attack=25,
        speed=25,
        shield=10,
        armor=10,
    )

    assert sample_warrior.get_actions() == {
        "1": {
            "description": "Atacar (ataque básico com arma)",
            "method": sample_warrior.strike,
        },
        "2": {
            "description": "Fúria (dobra ataque, sacrifica defesa)",
            "method": sample_warrior.to_rage,
        },
    }
