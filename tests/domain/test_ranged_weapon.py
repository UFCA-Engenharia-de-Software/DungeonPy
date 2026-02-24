from unittest.mock import MagicMock

import pytest

from domain.element import Element
from domain.ranged_weapon import RangedWeapon


def test_ranged_weapon_creation():
    weapon = RangedWeapon(
        name="Bow",
        base_damage=15,
        ammo_required=2,
        element=Element.NEUTRAL,
    )

    assert weapon.name == "Bow"
    assert weapon.base_damage == 15
    assert weapon.ammo_required == 2
    assert weapon.element == Element.NEUTRAL


def test_ammo_required_must_be_int():
    with pytest.raises(TypeError):
        RangedWeapon("Bow", 10, ammo_required="two")  # type: ignore


def test_ammo_required_must_be_positive():
    with pytest.raises(ValueError):
        RangedWeapon("Bow", 10, ammo_required=0)


def test_attack_consumes_ammo():
    weapon = RangedWeapon("Bow", 10, ammo_required=3)

    user = MagicMock()
    user.attack = 5
    user.current_ammo = 10

    target = MagicMock()

    weapon.attack(user, target)

    assert user.current_ammo == 7

    target.damage_received.assert_called_once_with(15, weapon.element)


def test_attack_raises_when_not_enough_ammo():
    weapon = RangedWeapon("Bow", 10, ammo_required=5)

    user = MagicMock()
    user.attack = 5
    user.current_ammo = 3  # insufficient

    target = MagicMock()

    with pytest.raises(ValueError):
        weapon.attack(user, target)

    assert user.current_ammo == 3
