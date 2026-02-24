import pytest
from domain.element import Element
from domain.ranged_weapon import RangedWeapon
from unittest.mock import patch
from domain.archer import Archer
from domain.monster import Monster


def test_constructor():
    archer_generic = Archer(
        name="gavião_do_grau", max_life=200, current_life=100, attack=20, speed=30
    )

    assert archer_generic.name == "Gavião_Do_Grau"
    assert archer_generic.max_life == 200
    assert archer_generic.current_life == 100
    assert archer_generic.attack == 20
    assert archer_generic.speed == 30


def test_reset_dodge():
    archer_generic = Archer(
        name="gavião_do_grau",
        max_life=200,
        current_life=100,
        attack=20,
        speed=30,
        dodge=True,
    )

    archer_generic.reset_dodge()
    assert archer_generic.dodge is False


def test_reload():
    archer_generic = Archer(
        name="gavião_do_grau",
        max_life=200,
        current_life=100,
        attack=20,
        speed=30,
        current_ammo=0,
    )

    archer_generic.reload()
    assert archer_generic.current_ammo == archer_generic.max_ammo


def test_aim():
    archer_generic = Archer(
        name="gavião_do_grau",
        max_life=200,
        current_life=100,
        attack=20,
        speed=30,
        dodge=True,
        is_aiming=False,
    )

    archer_generic.aim()
    assert archer_generic.dodge is False
    assert archer_generic.is_aiming is True


def test_aim_cancel_dodge():
    archer_generic = Archer(
        name="gavião_do_grau",
        max_life=200,
        current_life=100,
        attack=20,
        speed=30,
        dodge=True,
    )
    archer_generic.aim()
    with patch("domain.archer.random.randint", return_value=1000):
        archer_generic.damage_received(10, Element.NEUTRAL)

    assert archer_generic.current_life == 90


def test_upgrade():
    archer_generic = Archer(
        name="gavião_do_grau",
        max_life=200,
        current_life=100,
        attack=20,
        speed=30,
        dodge=True,
        is_aiming=False,
    )

    archer_generic.upgrade(4, 2)

    assert archer_generic.speed == 32
    assert archer_generic.attack == 22
    assert archer_generic.max_ammo == 12


def test_get_actions():
    archer_generic = Archer(
        name="gavião_do_grau", max_life=200, current_life=100, attack=20, speed=30
    )
    assert archer_generic.get_actions() == {
        "1": {
            "description": "Atirar (Ataque básico com arma)",
            "method": archer_generic.strike,
        },
        "2": {
            "description": "Mirar (acerto garantido, sacrifica esquiva, aumenta de leve o dano)",
            "method": archer_generic.aim,
        },
        "3": {
            "description": "Recarregar (recarrega a munição)",
            "method": archer_generic.reload,
        },
    }


def test_attempted_dodge_success_in_damage_receive():
    archer_generic = Archer(
        name="gavião_do_grau", max_life=200, current_life=100, attack=20, speed=30
    )
    with patch("domain.archer.random.randint", return_value=50):
        #
        archer_generic.damage_received(10, Element.NEUTRAL)

    assert archer_generic.current_life == 100
    assert archer_generic.dodge is False


def test_attempted_dodge_fail_in_damage_receive():
    archer_generic = Archer(
        name="gavião_do_grau", max_life=200, current_life=100, attack=20, speed=30
    )

    with patch("domain.archer.random.randint", return_value=-1):
        archer_generic.damage_received(10, Element.NEUTRAL)

    assert archer_generic.current_life == 90


def test_attempted_dodge_with_aim():
    arqueirin = Archer(
        name="gavião_do_grau",
        max_life=200,
        current_life=100,
        attack=20,
        speed=30,
        dodge=True,
    )

    arqueirin.aim()
    with patch("domain.archer.random.randint", return_value=100):
        arqueirin.damage_received(10, Element.NEUTRAL)

    assert arqueirin.is_aiming is True
    assert arqueirin.dodge is False
    assert arqueirin.current_life == 90


def test_strike_is_aiming_buff():
    arqueirin = Archer(
        name="gavião_do_grau",
        max_life=200,
        current_life=100,
        attack=20,
        speed=30,
        current_ammo=10,
        max_ammo=12,
    )

    monstrin = Monster(
        name="Fire Dragon",
        max_life=100,
        attack=25,
        speed=10,
        element=Element.FIRE,
        loot=["Dragon Scale"],
        description="A fierce dragon",
    )
    arco = RangedWeapon(name="Arco Teste", base_damage=10, ammo_required=1)
    arqueirin.equipped_weapon = arco

    arqueirin.aim()
    arqueirin.strike(monstrin)

    # Attack it`s the same in the beggining
    assert arqueirin.attack == 20

    # Testing damage in
    # Ataque Base: 20
    # Buff de Mira (20 / 2.5): +8
    # Ataque Total do Herói: 28
    # Dano Base da Arma: 10
    # Dano Total = (28 + 10) * 1 (Multiplicador Elemental) = 38

    expected_life = 100 - 38
    assert monstrin.current_life == expected_life
    assert arqueirin.is_aiming is False


# Testing getters and setters


def test_max_ammo():
    with pytest.raises(TypeError):
        Archer(
            name="gavião_do_grau",
            max_life=200,
            current_life=100,
            attack=20,
            speed=30,
            max_ammo="é_bala_chefe",
        )

    with pytest.raises(ValueError):
        Archer(
            name="gavião_do_grau",
            max_life=200,
            current_life=100,
            attack=20,
            speed=30,
            max_ammo=-1,
        )


def test_current_ammo():
    # Error
    with pytest.raises(TypeError):
        Archer(
            name="gavião_do_grau",
            max_life=200,
            current_life=100,
            attack=20,
            speed=30,
            current_ammo="bala_de_mel",
        )

    # Logic Error
    with pytest.raises(ValueError):
        Archer(
            name="gavião_do_grau",
            max_life=200,
            current_life=100,
            attack=20,
            speed=30,
            current_ammo=-1,
        )

    # Logic error: current ammo cannot be greater than max ammo
    with pytest.raises(ValueError):
        Archer(
            name="gavião_do_grau",
            max_life=200,
            current_life=100,
            attack=20,
            speed=30,
            max_ammo=10,
            current_ammo=11,
        )


def test_dodge():
    with pytest.raises(TypeError):
        Archer(
            name="gavião_do_grau",
            max_life=200,
            current_life=100,
            attack=20,
            speed=30,
            dodge="Esquivo, Esquivo",
        )


def test_equipped_weapon():
    with pytest.raises(TypeError):
        arqueirozin = Archer(
            name="gavião_do_grau",
            max_life=200,
            current_life=100,
            attack=20,
            speed=30,
            equipped_weapon="3oitão",
        )

    # Testing if equipped weapon can be None
    arqueirozin = Archer(
        name="gavião_do_grau", max_life=200, current_life=100, attack=20, speed=30
    )
    assert arqueirozin.equipped_weapon is None


def test_is_aiming():
    with pytest.raises(TypeError):
        Archer(
            name="gavião_do_grau",
            max_life=200,
            current_life=100,
            attack=20,
            speed=30,
            is_aiming="ovo_atirar",
        )
