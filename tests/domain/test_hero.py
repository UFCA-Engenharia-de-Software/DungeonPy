import pytest
from domain.hero import Hero
from domain.entity import Entity
from domain.element import Element
from domain.inventory import Inventory


class ConcreteHero(Hero):
    def strike(self, target: Entity, strike_element: Element) -> None:
        target.damage_received(self.attack, strike_element)

    def damage_received(self, value: int, strike_element: Element) -> None:
        multiplier = strike_element.multiplier(self.element)
        self.current_life -= int(value * multiplier)

    def upgrade(self, points: int, choice: int) -> None:
        pass

    def get_actions(self):
        pass


def test_hero_cannot_be_instantiated_directly():
    with pytest.raises(TypeError):
        Hero("Test", 100, 100, 10, 5)


def test_default_inventory_is_created_when_none():
    hero = ConcreteHero("Lina", 100, 100, 10, 5)
    assert isinstance(hero.inventory, Inventory)


def test_custom_inventory_is_used():
    inv = Inventory(capacity=50.0)
    hero = ConcreteHero("Lina", 100, 100, 10, 5, inventory=inv)
    assert hero.inventory is inv


def test_concrete_hero_is_instance_of_hero_and_entity():
    hero = ConcreteHero("Link", 100, 100, 10, 5)
    assert isinstance(hero, Hero)
    assert isinstance(hero, Entity)


def test_missing_strike_raises():
    class Incomplete(Hero):
        def damage_received(self, value, strike_element):
            pass

        def upgrade(self, points, choice):
            pass

        def get_actions(self):
            pass

    with pytest.raises(TypeError):
        Incomplete("X", 100, 100, 10, 5)


def test_missing_damage_received_raises():
    class Incomplete(Hero):
        def strike(self, target, strike_element):
            pass

        def upgrade(self, points, choice):
            pass

        def get_actions(self):
            pass

    with pytest.raises(TypeError):
        Incomplete("X", 100, 100, 10, 5)


def test_missing_upgrade_raises():
    class Incomplete(Hero):
        def strike(self, target, strike_element):
            pass

        def damage_received(self, value, strike_element):
            pass

        def get_actions(self):
            pass

    with pytest.raises(TypeError):
        Incomplete("X", 100, 100, 10, 5)


def test_missing_actions_raises():
    class Incomplete(Hero):
        def strike(self, target, strike_element):
            pass

        def damage_received(self, value, strike_element):
            pass

        def upgrade(self, points, choice):
            pass

    with pytest.raises(TypeError):
        Incomplete("X", 100, 100, 10, 5)


def test_get_hero_status_returns_correct_dict():
    """Testa se get_hero_status retorna um dicionário com todos os atributos corretos."""
    hero = ConcreteHero(
        name="TestHero",
        max_life=100,
        current_life=80,
        attack=15,
        speed=5,
        element=Element.FIRE,
    )

    status = hero.get_hero_status()

    # Note: Entity.name apply .title() in name
    assert status["name"] == "Testhero"
    assert status["current_life"] == 80
    assert status["max_life"] == 100
    assert status["attack"] == 15
    assert status["speed"] == 5
    assert status["element"] == Element.FIRE.value
    assert status["equipped_weapon"] == "Nenhuma"


def test_get_hero_status_with_equipped_weapon():
    """Testa se get_hero_status mostra corretamente a arma equipada."""
    from unittest.mock import Mock

    hero = ConcreteHero("TestHero", 100, 100, 15, 5)

    # equipped weapon
    fake_weapon = Mock()
    fake_weapon.name = "Espada Mágica"
    hero._equipped_weapon = fake_weapon

    status = hero.get_hero_status()

    assert status["equipped_weapon"] == "Espada Mágica"


def test_equip_weapon_with_allowed_class_succeeds():
    """Herói da classe permitida consegue equipar a arma."""
    from domain.weapon import Weapon
    from domain.warrior import Warrior

    warrior = Warrior("Arthur", 100, 100, 20, 10)
    sword = Weapon(name="Espada", base_damage=15)
    warrior.equip_weapon(sword)
    assert warrior.equipped_weapon is sword


def test_equip_weapon_wrong_class_raises_type_error():
    """Herói de classe errada recebe TypeError ao tentar equipar."""
    from domain.weapon import Weapon

    hero = ConcreteHero("Mago Sem Arma", 100, 100, 10, 5)
    sword = Weapon(name="Espada", base_damage=15)  # allowed_class = ["Warrior"]

    with pytest.raises(TypeError):
        hero.equip_weapon(sword)


def test_equip_weapon_error_message_contains_allowed_class():
    """Error mensagem, talk which class can equip weapon"""
    from domain.weapon import Weapon

    hero = ConcreteHero("Intruso", 100, 100, 10, 5)
    sword = Weapon(name="Espada Longa", base_damage=20)

    with pytest.raises(TypeError, match="Warrior"):
        hero.equip_weapon(sword)


def test_equip_ranged_weapon_wrong_class_raises():
    """Warrior not equip ranged_weapon."""
    from domain.ranged_weapon import RangedWeapon
    from domain.warrior import Warrior

    warrior = Warrior("Guerreiro", 150, 150, 30, 10)
    bow = RangedWeapon(name="Arco", base_damage=15, ammo_required=1)

    with pytest.raises(TypeError):
        warrior.equip_weapon(bow)


def test_equip_grimoire_wrong_class_raises():
    """Warrior não pode equipar grimório."""
    from domain.grimoire import Grimoire
    from domain.element import Element
    from domain.warrior import Warrior

    warrior = Warrior("Guerreiro", 150, 150, 30, 10)
    grimoire = Grimoire(name="Tomo", element=Element.FIRE, magic_power=20, mana_cost=5)

    with pytest.raises(TypeError):
        warrior.equip_weapon(grimoire)
