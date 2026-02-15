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
