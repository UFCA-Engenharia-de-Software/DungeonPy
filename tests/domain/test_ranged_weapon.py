from unittest.mock import MagicMock, patch

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
    assert weapon.hit_probability == 70
    assert weapon.element == Element.NEUTRAL


def test_hit_probability_can_be_defined_on_creation():
    weapon = RangedWeapon("Bow", 15, ammo_required=2, hit_probability=85)

    assert weapon.hit_probability == 85


def test_ammo_required_must_be_int():
    with pytest.raises(TypeError):
        RangedWeapon("Bow", 10, ammo_required="two")


def test_ammo_required_must_be_positive():
    with pytest.raises(ValueError):
        RangedWeapon("Bow", 10, ammo_required=0)


def test_hit_probability_must_be_int():
    with pytest.raises(TypeError):
        RangedWeapon("Bow", 10, ammo_required=1, hit_probability=75.5)


def test_hit_probability_must_be_between_0_and_100():
    with pytest.raises(ValueError):
        RangedWeapon("Bow", 10, ammo_required=1, hit_probability=101)


def test_attack_consumes_ammo():
    weapon = RangedWeapon("Bow", 10, ammo_required=3, hit_probability=100)

    user = MagicMock()
    user.attack = 5
    user.current_ammo = 10

    target = MagicMock()

    weapon.attack(user, target)

    assert user.current_ammo == 7

    target.damage_received.assert_called_once_with(15, weapon.element)


def test_attack_hits_when_user_is_aiming():
    weapon = RangedWeapon("Bow", 10, ammo_required=3, hit_probability=0)

    user = MagicMock()
    user.attack = 5
    user.current_ammo = 10
    user.is_aiming = True

    target = MagicMock()

    weapon.attack(user, target)

    assert user.current_ammo == 7
    target.damage_received.assert_called_once_with(15, weapon.element)


def test_attack_hits_based_on_probability():
    weapon = RangedWeapon("Bow", 10, ammo_required=2, hit_probability=40)

    user = MagicMock()
    user.attack = 5
    user.current_ammo = 10
    user.is_aiming = False

    target = MagicMock()

    with patch("domain.ranged_weapon.random.randint", return_value=35):
        weapon.attack(user, target)

    assert user.current_ammo == 8
    target.damage_received.assert_called_once_with(15, weapon.element)


def test_attack_misses_based_on_probability():
    weapon = RangedWeapon("Bow", 10, ammo_required=2, hit_probability=40)

    user = MagicMock()
    user.attack = 5
    user.current_ammo = 10
    user.is_aiming = False

    target = MagicMock()

    with patch("domain.ranged_weapon.random.randint", return_value=80):
        weapon.attack(user, target)

    assert user.current_ammo == 8
    target.damage_received.assert_not_called()


def test_attack_raises_when_not_enough_ammo():
    weapon = RangedWeapon("Bow", 10, ammo_required=5)

    user = MagicMock()
    user.attack = 5
    user.current_ammo = 3  # insufficient

    target = MagicMock()

    with pytest.raises(ValueError):
        weapon.attack(user, target)

    assert user.current_ammo == 3


def test_heavy_attack_deals_double_damage_and_consumes_ammo():
    weapon = RangedWeapon("Bow", 10, ammo_required=2, hit_probability=100)

    user = MagicMock()
    user.attack = 5
    user.current_ammo = 10
    user.is_aiming = False

    target = MagicMock()

    weapon.heavy_attack(user, target)

    assert user.current_ammo == 8
    target.damage_received.assert_called_once_with(30, weapon.element)


def test_heavy_attack_raises_when_not_enough_ammo():
    weapon = RangedWeapon("Bow", 10, ammo_required=5)

    user = MagicMock()
    user.attack = 5
    user.current_ammo = 3
    user.is_aiming = False

    target = MagicMock()

    with pytest.raises(ValueError):
        weapon.heavy_attack(user, target)

    assert user.current_ammo == 3
