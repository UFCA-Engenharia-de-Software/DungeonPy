from unittest.mock import MagicMock
import pytest

from domain.mage import Mage
from domain.element import Element
from domain.grimoire import Grimoire
from domain.entity import Entity

# FIXTURES & MOCKS:


@pytest.fixture
def mage_default():
    """Creates a default mage to be used in the tests."""

    return Mage(
        name="Gandalf",
        max_life=100,
        current_life=100,
        max_mana=100,
        current_mana=100,
        attack=10,
        speed=10,
        element=Element.NEUTRAL,
    )


@pytest.fixture
def mock_target():
    """Creates a fake entity, just to get targeted while testing the attacks."""

    target = MagicMock(spec=Entity)
    target.name = "Orc Dummy"
    target.damage_received = MagicMock()
    return target


# INITIALIZATION TESTS:


def test_mage_initialization_success(mage_default):
    assert mage_default.name == "Gandalf"
    assert mage_default.max_mana == 100
    assert mage_default.current_mana == 100
    assert isinstance(mage_default, Entity)


# PROPERTIES VALIDATION TESTS:


def test_max_mana_validation(mage_default):
    with pytest.raises(TypeError):
        mage_default.max_mana = "one hundred"  # type: ignore

    with pytest.raises(ValueError):
        mage_default.max_mana = -1

    mage_default.max_mana = 200
    assert mage_default.max_mana == 200


def test_current_mana_logic(mage_default):
    mage_default.current_mana = -50
    assert mage_default.current_mana == 0

    mage_default.current_mana = 9999
    assert mage_default.current_mana == mage_default.max_mana

    with pytest.raises(TypeError):
        mage_default.current_mana = 50.5  # type: ignore


# COMBAT TESTS I - STRIKE METHOD:


def test_strike_without_grimoire(mage_default, mock_target):
    """Tests if the mage deals a weak physical attack when there's no grimoire equipped."""

    msg = mage_default.strike(mock_target)

    assert "soco fraco" in msg
    mock_target.damage_received.assert_called_once_with(1, Element.NEUTRAL)


def test_strike_with_grimoire_equipped(mage_default, mock_target):
    """
    When there's a grimoire equipped, it assigns the strike method responsability to the grimoire's cast_spell method.
    Using a Grimoire mock to isolate Mage tests.
    """

    mock_grimoire = MagicMock(spec=Grimoire)
    mock_grimoire.cast_spell.return_value = "Spell cast!"

    mage_default.equip_grimoire(mock_grimoire)
    msg = mage_default.strike(mock_target)

    assert msg == "Spell cast!"
    mock_grimoire.cast_spell.assert_called_once_with(mage_default, mock_target)


# COMBAT TESTS II - ANCIENT MAGIC METHOD:


def test_ancient_magic_success(mage_default, mock_target):
    """
    Tests if the Mage 'ultimate attack' (Ancicent Magic):
    - Spends 50 Mana Points;
    - Deals [(attack * 3) + 50] damage;
    """

    mage_default.current_mana = 50
    msg = mage_default.ancient_magic(mock_target)

    assert "MAGIA ANCESTRAL" in msg
    assert mage_default.current_mana == 0
    mock_target.damage_received.assert_called_once_with(80, Element.NEUTRAL)


def test_ancient_magic_insufficient_mana(mage_default, mock_target):
    """The attack shall not work if Mana < 50."""

    mage_default.current_mana = 49
    msg = mage_default.ancient_magic(mock_target)

    assert "não tem mana" in msg
    assert (
        mage_default.current_mana == 49
    )  # not supposed to spend mana if the attack fails.
    mock_target.damage_received.assert_not_called()  # no damage.


# UPGRADE TESTS:


def test_upgrade_attack(mage_default):
    """When choice == 1: attack raises."""

    initial_attack = mage_default.attack
    points = 5

    mage_default.upgrade(points, 1)
    assert mage_default.attack == initial_attack + points


def test_upgrade_mana(mage_default):
    """When choice == 2: max_mana raises and current_mana get restored."""

    mage_default.max_mana = 0
    mage_default.current_mana = 0
    initial_max = mage_default.max_mana
    points = 10

    mage_default.upgrade(points, 2)
    assert mage_default.max_mana == initial_max + points
    assert mage_default.current_mana == mage_default.max_mana


def test_upgrade_invalid_choice(mage_default):
    """Raise an error when there's no matching option for choice."""

    with pytest.raises(ValueError):
        mage_default.upgrade(points=5, choice=3)


# GET ACTION TESTS:


def test_get_actions_without_weapon(mage_default):
    actions = mage_default.get_actions()

    assert "1" in actions
    assert "2" in actions
    assert "MP: 0" in actions["1"]["description"]
    assert "Magia Ancestral" in actions["2"]["description"]


def test_get_actions_with_weapon(mage_default):
    # Using a mock grimoire, returning an attacks dictionary.

    mock_grimoire = MagicMock(spec=Grimoire)
    mock_grimoire.get_attacks.return_value = {
        "1": {"description": "Bola De Fogo", "method": lambda: None}
    }

    mage_default.equip_grimoire(mock_grimoire)
    actions = mage_default.get_actions()

    assert actions["1"]["description"] == "Bola De Fogo"
    assert "2" in actions
