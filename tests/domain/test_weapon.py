from unittest.mock import MagicMock

import pytest

from domain.element import Element
from domain.entity import Entity
from domain.weapon import Weapon


def test_weapon_creation_with_defaults():
    weapon = Weapon(name="Short Sword", base_damage=10)

    assert weapon.name == "Short Sword"
    assert weapon.base_damage == 10
    assert weapon.element == Element.NEUTRAL
    assert weapon.weight == 1.0


def test_weapon_creation_with_all_args():
    weapon = Weapon(
        name="Fire Axe",
        base_damage=15,
        description="Burning axe",
        weight=5.0,
        element=Element.FIRE,
    )

    assert weapon.name == "Fire Axe"
    assert weapon.base_damage == 15
    assert weapon.get_description() == "Burning axe"
    assert weapon.weight == 5.0
    assert weapon.element == Element.FIRE


def test_base_damage_must_be_integer():
    with pytest.raises(TypeError):
        Weapon(name="Sword", base_damage="10")


def test_base_damage_must_be_positive():
    with pytest.raises(ValueError):
        Weapon(name="Sword", base_damage=0)

    with pytest.raises(ValueError):
        Weapon(name="Sword", base_damage=-5)


def test_element_must_be_valid_element():
    with pytest.raises(TypeError):
        Weapon(name="Sword", base_damage=10, element="fire")


def test_base_damage_setter_updates_value():
    weapon = Weapon(name="Sword", base_damage=10)
    weapon.base_damage = 25

    assert weapon.base_damage == 25


def test_element_setter_updates_value():
    weapon = Weapon(name="Sword", base_damage=10)
    weapon.element = Element.ICE

    assert weapon.element == Element.ICE


def test_attack_applies_correct_damage():
    weapon = Weapon(name="Sword", base_damage=10, element=Element.FIRE)

    mock_user = MagicMock()
    mock_user.attack = 20

    mock_target = MagicMock(spec=Entity)

    weapon.attack(mock_user, mock_target)

    mock_target.damage_received.assert_called_once_with(30, Element.FIRE)


def test_attack_uses_updated_base_damage():
    weapon = Weapon(name="Sword", base_damage=5, element=Element.ICE)

    weapon.base_damage = 15

    mock_user = MagicMock()
    mock_user.attack = 10

    mock_target = MagicMock(spec=Entity)

    weapon.attack(mock_user, mock_target)

    mock_target.damage_received.assert_called_once_with(25, Element.ICE)


def test_get_attacks_returns_expected_structure():
    weapon = Weapon(name="Sword", base_damage=10)

    attacks = weapon.get_attacks()

    assert isinstance(attacks, dict)

    assert set(attacks.keys()) == {"1", "2"}

    assert attacks["1"]["description"] == "Ataque Normal"
    assert attacks["2"]["description"] == "Ataque Pesado"

    assert callable(attacks["1"]["method"])
    assert callable(attacks["2"]["method"])


def test_heavy_attack_applies_double_damage():
    weapon = Weapon(name="Sword", base_damage=10, element=Element.ICE)

    mock_user = MagicMock()
    mock_user.attack = 10

    mock_target = MagicMock(spec=Entity)

    weapon.heavy_attack(mock_user, mock_target)

    mock_target.damage_received.assert_called_once_with(40, Element.ICE)


def test_heavy_attack_uses_updated_base_damage():
    weapon = Weapon(name="Sword", base_damage=5, element=Element.NEUTRAL)

    weapon.base_damage = 15

    mock_user = MagicMock()
    mock_user.attack = 5

    mock_target = MagicMock(spec=Entity)

    weapon.heavy_attack(mock_user, mock_target)

    mock_target.damage_received.assert_called_once_with(40, Element.NEUTRAL)


def test_get_attacks_method_executes_correct_attack():
    weapon = Weapon(name="Sword", base_damage=10, element=Element.FIRE)

    mock_user = MagicMock()
    mock_user.attack = 10

    mock_target = MagicMock(spec=Entity)

    attacks = weapon.get_attacks()

    # Executa ataque normal via dicionário
    attacks["1"]["method"](mock_user, mock_target)

    mock_target.damage_received.assert_called_once_with(20, Element.FIRE)
