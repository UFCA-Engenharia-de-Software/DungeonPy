from unittest.mock import MagicMock
import pytest
from domain.grimoire import Grimoire
from domain.item import Item
from domain.element import Element

# INITIALIZATION TESTS:


def test_grimoire_creation_valid():
    """Tests if the grimoire creation uses the right attributes."""

    book = Grimoire(
        name="Tome of Fire",
        element=Element.FIRE,
        magic_power=20,
        mana_cost=10,
        weight=3.0,
    )

    assert isinstance(book, Item)
    assert book.name == "Tome Of Fire"
    assert book.element == Element.FIRE
    assert book.magic_power == 20
    assert book.mana_cost == 10
    assert book.weight == 3.0
    assert "FIRE" in book.get_description()


def test_grimoire_attacks_structure():
    """Tests if the attacks dictionary is correctly created."""

    book = Grimoire("Book", Element.ICE, 10, 5)
    attacks = book.get_attacks()

    assert isinstance(attacks, dict)
    assert "1" in attacks
    assert "MP: 5" in attacks["1"]["description"]
    assert callable(attacks["1"]["method"])


# VALIDATION TESTS:


def test_magic_power_validation():
    """Tests if magic_power rejects invalid values."""

    with pytest.raises(TypeError):
        Grimoire("Book", Element.FIRE, magic_power="strong as hell", mana_cost=5)  # type: ignore

    with pytest.raises(ValueError):
        Grimoire("Book", Element.ICE, magic_power=-1, mana_cost=5)


def test_mana_cost_validation():
    """Tests if mana_cost rejects invalid values."""

    with pytest.raises(TypeError):
        Grimoire("Book", Element.LIGHTNING, magic_power=20, mana_cost="five")  # type: ignore

    with pytest.raises(ValueError):
        Grimoire("Book", Element.POISON, magic_power=20, mana_cost=-1)


def test_element_validation():
    """Tests if element can only be typed with the Elements enum."""

    with pytest.raises(TypeError):
        Grimoire("Book", element="FROST", magic_power=20, mana_cost=5)  # type: ignore


# COMBAT TESTS:


def test_cast_spell_success():
    """Creates a dream-scenario for the cast_spell() method: user has mana, uses it and deals damage.
    Using mocks to isolate Grimoire tests.
    """

    book = Grimoire("Book", Element.LIGHTNING, magic_power=15, mana_cost=10)

    # USER MOCKS:

    mock_user = MagicMock()
    mock_user.name = "Merlin"
    mock_user.current_mana = 50
    mock_user.attack = 5

    # TARGET MOCK:

    mock_target = MagicMock()
    mock_target.name = "Goblin"

    message = book.cast_spell(mock_user, mock_target)

    assert mock_user.current_mana == 40
    mock_target.damage_received.assert_called_once_with(20, Element.LIGHTNING)
    assert "Merlin" in message
    assert "LIGHTNING" in message


def test_cast_spell_insufficient_mana():
    """
    Tests if the attack doesn't work when there's no sufficient mana.
    """

    book = Grimoire("Ultima", Element.POISON, magic_power=100, mana_cost=50)

    # MOCKS:

    mock_user = MagicMock()
    mock_user.name = "Apprentice"
    mock_user.current_mana = 10

    mock_target = MagicMock()

    message = book.cast_spell(mock_user, mock_target)

    assert mock_user.current_mana == 10
    mock_target.damage_received.assert_not_called()
    assert "não possui mana" in message


# USE() METHOD TESTS:


def test_use_equip_on_mage_success():
    """Tests if the item can be equipped when the target has the equip_grimoire method."""

    book = Grimoire("Necronomicon", Element.POISON, 10, 10)

    mock_mage = MagicMock()
    mock_mage.name = "Gandalf"

    message = book.use(mock_mage)

    mock_mage.equip_grimoire.assert_called_once_with(book)
    assert "equipou o grimório" in message


def test_use_equip_on_non_mage_failure():
    """Tests if the equip fails when the target is not a mage."""

    book = Grimoire("Necronomicon", Element.POISON, 10, 10)

    class FakeWarrior:
        name = "Conan"

    warrior = FakeWarrior()
    message = book.use(warrior)

    assert "não entendeu nada" in message
