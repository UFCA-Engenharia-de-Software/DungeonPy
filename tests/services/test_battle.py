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
from domain.weapon import Weapon


def _create_warrior_with_weapon(**kwargs) -> Warrior:
    """Helper to create a warrior with an equipped weapon."""
    warrior = Warrior(**kwargs)
    weapon = Weapon(name="Test Sword", base_damage=1)
    warrior.inventory.add_item_to_inventory(weapon)
    warrior.equip_weapon(weapon)
    return warrior


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
    hero = _create_warrior_with_weapon(
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

    result = battle.execute_turn(player_choice="1")

    assert monster.current_life < monster.max_life
    assert result["result"] == "ongoing"


def test_combat_ends_on_monster_death():
    hero = _create_warrior_with_weapon(
        name="Knight",
        max_life=100,
        current_life=100,
        attack=999,  # high damage for kill monster
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

    result = battle.execute_turn(player_choice="1")

    assert result["result"] == "victory"
    assert monster.current_life <= 0


def test_combat_ends_on_hero_death():
    hero = _create_warrior_with_weapon(
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

    result = battle.execute_turn(player_choice="1")

    assert result["result"] == "defeat"
    assert hero.current_life <= 0


def test_loot_on_victory():
    hero = _create_warrior_with_weapon(
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

    result = battle.execute_turn(player_choice="1")

    assert result["result"] == "victory"
    assert result["loot"] == ["Scale", "Claw"]


def test_no_loot_on_defeat():
    hero = _create_warrior_with_weapon(
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

    result = battle.execute_turn(player_choice="1")

    assert result["result"] == "defeat"
    assert result["loot"] == []


def _make_monster(attack=10, speed=5, life=100):
    return Monster(
        name="Goblin",
        max_life=life,
        attack=attack,
        speed=speed,
        element=Element.NEUTRAL,
        loot=[],
        description="goblin de teste",
    )


def test_turn_log_has_required_keys():
    """execute_turn must return a dict with required keys."""
    hero = _create_warrior_with_weapon(
        name="Knight", max_life=100, current_life=100, attack=10, speed=20
    )
    battle = Battle(hero, _make_monster())
    result = battle.execute_turn(player_choice="1")

    # Top-level keys
    for key in ("result", "loot", "turn_log"):
        assert key in result, f"Chave ausente no resultado: {key}"

    # Keys inside turn_log
    turn_log = result["turn_log"]
    for key in ("actions", "combat_over", "hero_used_consumable", "status"):
        assert key in turn_log, f"Chave ausente no turn_log: {key}"


def test_action_failed_when_no_weapon_equipped():
    """Warrior sem arma: action_failed=True e monstro NÃO age (vida não muda)."""
    warrior = Warrior(
        name="Desarmado",
        max_life=100,
        current_life=100,
        attack=25,
        speed=30,  # most fast that monster
    )
    monster = _make_monster(attack=999, speed=5)
    battle = Battle(warrior, monster)

    life_before = warrior.current_life
    result = battle.execute_turn(player_choice="1")

    assert result["turn_log"].get("action_failed") is True
    assert warrior.current_life == life_before  # monster no attacked


def test_consumable_use_sets_hero_used_consumable():
    """Using a consumable marks hero_used_consumable=True in the turn_log."""
    from domain.consumable_item import ConsumableItem

    hero = _create_warrior_with_weapon(
        name="Knight", max_life=100, current_life=50, attack=10, speed=20
    )
    potion = ConsumableItem(
        name="Poção de Cura", description="Cura", weight=0.5, recovered_value=20
    )
    hero.inventory.add_item_to_inventory(potion)

    monster = _make_monster(attack=5, speed=5, life=200)
    battle = Battle(hero, monster)

    # Warrior.get_actions() does not expose inventory items — inject the potion
    # directly into the action dict, exactly as game_manager does at runtime.
    original_get_actions = hero.get_actions

    def patched_get_actions():
        actions = original_get_actions()
        actions["p"] = {"description": potion.name, "method": potion.use}
        return actions

    hero.get_actions = patched_get_actions
    result = battle.execute_turn(player_choice="p")
    assert result["turn_log"]["hero_used_consumable"] is True


def test_mana_potion_blocked_for_warrior_in_battle():
    """Mana potion used by Warrior should mark action_failed=True and monster should not act."""
    from domain.consumable_item import ConsumableItem

    hero = _create_warrior_with_weapon(
        name="Knight", max_life=100, current_life=100, attack=10, speed=20
    )
    mana_potion = ConsumableItem(
        name="Poção de Mana",
        description="Restaura mana",
        weight=0.5,
        recovered_value=30,
        recovery_type="mana",
    )
    hero.inventory.add_item_to_inventory(mana_potion)

    monster = _make_monster(attack=999, speed=5, life=200)
    battle = Battle(hero, monster)

    original_get_actions = hero.get_actions

    def patched_get_actions():
        actions = original_get_actions()
        actions["m"] = {"description": mana_potion.name, "method": mana_potion.use}
        return actions

    hero.get_actions = patched_get_actions
    life_before = hero.current_life
    result = battle.execute_turn(player_choice="m")

    assert result["turn_log"].get("action_failed") is True
    assert hero.current_life == life_before  # monster did not act


def test_turn_log_actions_list_not_empty_after_attack():
    """After a successful attack, the actions list should not be empty."""
    hero = _create_warrior_with_weapon(
        name="Knight", max_life=100, current_life=100, attack=10, speed=20
    )
    battle = Battle(hero, _make_monster())
    result = battle.execute_turn(player_choice="1")

    assert isinstance(result["turn_log"]["actions"], list)
    assert len(result["turn_log"]["actions"]) > 0


def test_warrior_rage_activates_on_action_2():
    """Activating rage (action 2) should double attack and zero shields."""
    warrior = Warrior(
        name="Bruto",
        max_life=200,
        current_life=200,
        attack=25,
        speed=30,
        shield=10,
        armor=10,
    )
    battle = Battle(warrior, _make_monster(speed=5))
    battle.execute_turn(player_choice="2")  # to_rage

    assert warrior.in_rage is True
    assert warrior.attack == 50  # doubled
    assert warrior.shield == 0
    assert warrior.armor == 0


def test_archer_aim_sets_special_state_in_log():
    """Aiming should register special_state='aiming' in the turn_log."""
    from domain.archer import Archer
    from domain.ranged_weapon import RangedWeapon

    archer = Archer(
        name="Legolas",
        max_life=100,
        current_life=100,
        attack=20,
        speed=30,
        max_ammo=10,
        current_ammo=10,
    )
    bow = RangedWeapon(name="Arco", base_damage=10, ammo_required=1)
    archer.inventory.add_item_to_inventory(bow)
    archer.equip_weapon(bow)

    battle = Battle(archer, _make_monster(speed=5))
    result = battle.execute_turn(player_choice="2")  # aim

    assert result["turn_log"].get("special_state") == "aiming"
