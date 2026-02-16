"""
Crie testes nesta ordem (mesma ordem das etapas):

9. test_execute_turn_basic - Turno executa sem erros, dano é aplicado?
10. test_combat_ends_on_monster_death - Combate termina quando monstro morre?
11. test_combat_ends_on_hero_death - Combate termina quando herói morre?
12. test_loot_on_victory - Loot é coletado após vitória?
13. test_no_loot_on_defeat - Sem loot se herói perdeu?
"""

import pytest
from services.battle import Battle
from domain.hero import Hero
from domain.warrior import Warrior
from domain.monster import Monster
from domain.element import Element
from domain.state import NeutralState, StunnedState


def test_combat_initialization():
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

    battle_orchestrator = Battle(sample_warrior, sample_monster)

    assert isinstance(battle_orchestrator.hero, Hero)
    assert isinstance(battle_orchestrator.monster, Monster)


def test_combat_invalid_hero():
    sample_monster: Monster = Monster(
        name="Fire Dragon",
        max_life=100,
        attack=25,
        speed=10,
        element=Element.FIRE,
        loot=["Dragon Scale"],
        description="A fierce dragon",
    )
    with pytest.raises(TypeError):
        Battle(sample_monster, sample_monster)


def test_combat_invalid_monster():
    sample_warrior: Warrior = Warrior(
        name="Errant Knight",
        max_life=200,
        current_life=100,
        attack=25,
        speed=25,
    )

    with pytest.raises(TypeError):
        Battle(sample_warrior, sample_warrior)


def test_turn_order_hero_faster():
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

    battle_orchestrator = Battle(sample_warrior, sample_monster)
    assert battle_orchestrator.turn_order == [sample_warrior, sample_monster]


def test_turn_order_hero_monster():
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
        speed=50,
        element=Element.FIRE,
        loot=["Dragon Scale"],
        description="A fierce dragon",
    )

    battle_orchestrator = Battle(sample_warrior, sample_monster)
    assert battle_orchestrator.turn_order == [sample_monster, sample_warrior]


def test_turn_order_speed_tie():
    sample_warrior: Warrior = Warrior(
        name="Errant Knight",
        max_life=200,
        current_life=100,
        attack=25,
        speed=10,
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

    battle_orchestrator = Battle(sample_warrior, sample_monster)
    assert battle_orchestrator.turn_order == [sample_warrior, sample_monster]


def test_apply_status_effects():
    sample_warrior: Warrior = Warrior(
        name="Errant Knight",
        max_life=200,
        current_life=100,
        attack=25,
        speed=10,
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

    battle_orchestrator = Battle(sample_warrior, sample_monster)

    battle_orchestrator._apply_status_effects(sample_warrior)
    assert isinstance(sample_warrior.current_status, NeutralState)

    battle_orchestrator._apply_status_effects(sample_monster)
    assert isinstance(sample_monster.current_status, NeutralState)


def test_status_expires():
    sample_warrior: Warrior = Warrior(
        name="Errant Knight",
        max_life=200,
        current_life=100,
        attack=25,
        speed=10,
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

    battle_orchestrator = Battle(sample_warrior, sample_monster)
    sample_warrior.current_status = StunnedState()

    assert sample_warrior.current_status.duration_turns == 1

    battle_orchestrator._apply_status_effects(sample_warrior)
    assert sample_warrior.current_status.duration_turns == 0

    battle_orchestrator._apply_status_effects(sample_warrior)
    assert isinstance(sample_warrior.current_status, NeutralState)


def test_can_act():
    sample_warrior: Warrior = Warrior(
        name="Errant Knight",
        max_life=200,
        current_life=100,
        attack=25,
        speed=10,
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

    battle_orchestrator = Battle(sample_warrior, sample_monster)
    assert battle_orchestrator._can_act(sample_warrior)

    sample_monster.set_status(StunnedState())
    assert not battle_orchestrator._can_act(sample_monster)


def test_is_combat_over():
    sample_warrior: Warrior = Warrior(
        name="Errant Knight",
        max_life=200,
        current_life=100,
        attack=25,
        speed=10,
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

    battle_orchestrator = Battle(sample_warrior, sample_monster)
    assert not battle_orchestrator._is_combat_over()

    sample_warrior.current_life = 0
    assert battle_orchestrator._is_combat_over()


def test_execute_turn_basic():
    hero = Warrior(
        name="Knight",
        max_life=100,
        current_life=100,
        attack=30,
        speed=20,
    )

    monster = Monster(
        name="Goblin",
        max_life=50,
        attack=10,
        speed=10,
        element=Element.FIRE,
        loot=["Gold"],
        description="Small goblin",
    )

    battle = Battle(hero, monster)

    result = battle.execute_turn(player_choice="attack")

    assert monster.current_life < monster.max_life
    assert result["result"] == "ongoing"


def test_combat_ends_on_monster_death():
    hero = Warrior(
        name="Knight",
        max_life=100,
        current_life=100,
        attack=999,  # dano alto para matar em 1 turno
        speed=20,
    )

    monster = Monster(
        name="Goblin",
        max_life=30,
        attack=5,
        speed=10,
        element=Element.FIRE,
        loot=["Gold"],
        description="Weak goblin",
    )

    battle = Battle(hero, monster)

    result = battle.execute_turn(player_choice="attack")

    assert result["result"] == "victory"
    assert monster.current_life <= 0


def test_combat_ends_on_hero_death():
    hero = Warrior(
        name="Knight",
        max_life=30,
        current_life=30,
        attack=5,
        speed=5,
    )

    monster = Monster(
        name="Ogre",
        max_life=200,
        attack=999,  # mata o herói
        speed=20,
        element=Element.FIRE,
        loot=["Club"],
        description="Strong ogre",
    )

    battle = Battle(hero, monster)

    result = battle.execute_turn(player_choice="attack")

    assert result["result"] == "defeat"
    assert hero.current_life <= 0


def test_loot_on_victory():
    hero = Warrior(
        name="Knight",
        max_life=100,
        current_life=100,
        attack=999,
        speed=20,
    )

    monster = Monster(
        name="Dragon Whelp",
        max_life=40,
        attack=5,
        speed=10,
        element=Element.FIRE,
        loot=["Scale", "Claw"],
        description="Young dragon",
    )

    battle = Battle(hero, monster)

    battle.execute_turn(player_choice="attack")
    result = battle.get_combat_result()

    assert result["result"] == "victory"
    assert result["loot"] == ["Scale", "Claw"]


def test_no_loot_on_defeat():
    hero = Warrior(
        name="Knight",
        max_life=20,
        current_life=20,
        attack=5,
        speed=5,
    )

    monster = Monster(
        name="Demon",
        max_life=200,
        attack=999,
        speed=20,
        element=Element.FIRE,
        loot=["Demon Horn"],
        description="Powerful demon",
    )

    battle = Battle(hero, monster)

    battle.execute_turn(player_choice="attack")
    result = battle.get_combat_result()

    assert result["result"] == "defeat"
    assert result["loot"] == []
