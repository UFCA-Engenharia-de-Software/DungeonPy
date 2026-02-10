import pytest

from domain.room import Room
from domain.warrior import Warrior
from domain.element import Element
from domain.monster import Monster
from domain.item import Item
from domain.inventory import Inventory

# HELPER CLASS:


class SimpleItem(Item):
    def use(self, target):
        pass


# FIXTURES:


@pytest.fixture
def hero():
    return Warrior(
        name="Conan",
        max_life=100,
        current_life=100,
        attack=10,
        speed=5,
        element=Element.NEUTRAL,
        inventory=Inventory(capacity=50.0),
    )


@pytest.fixture
def item():
    return SimpleItem(name="Poção De Cura", description="Cura 10 HP", weight=1.0)


@pytest.fixture
def heavy_item():
    return SimpleItem(
        name="Pedra Grande", description="Pesado. Não tente carregar.", weight=100.0
    )


@pytest.fixture
def monster():
    return Monster("ORC", 50, 5, 5, Element.FIRE)


# ROOM TESTS:


def test_room_valid_initialization():
    room = Room("Sala segura.", Element.NEUTRAL)
    assert room.description == "Sala segura."
    assert len(room.monsters) == 0
    assert len(room.items) == 0


def test_invalid_room_description():
    """Tests if the room rejects empty descriptions."""
    with pytest.raises(ValueError):
        Room("", Element.NEUTRAL)


def test_invalid_room_environment_type():
    """Tests if the room rejects incorrect types of environment."""
    with pytest.raises(TypeError):
        Room("Sala segura.", "DefinitivamenteNãoÉUmElemento")  # type: ignore


def test_monster_encapsulation(monster):
    """Tests if the Monsters list is truly protected."""
    room = Room("Arena Infernal", Element.FIRE)
    room.add_monster(monster)

    # TRYING TO GET THE LIST AND CLEAN IT:
    outside_list = room.monsters
    outside_list.clear()

    # HOPEFULLY, THE LIST REMAINS UNTOUCHED:
    assert len(room.monsters) == 1
    assert room.monsters[0].name == "Orc"


def test_item_encapsulation(item):
    """Tests if the Items list is truly protected."""
    room = Room("Tesouraria", Element.NEUTRAL)
    room.add_item(item)

    outside_list = room.items
    outside_list.clear()

    assert len(room.items) == 1
    assert room.items[0].name == "Poção De Cura"


def test_enter_output(hero, monster, item):
    """Tests if the so called 'enter' method returns a string without printing."""
    room = Room("Sala escura", Element.NEUTRAL, monsters=[monster], items=[item])
    log = room.enter(hero)

    assert "Sala escura" in log
    assert "Orc" in log
    assert "Poção De Cura" in log
    assert "Prepare-se para lutar" in log


# TAKE ITEM TESTS:


def test_take_item_success(item):
    """Tests if the room gives the item and removes it from the inner list."""
    room = Room("Sala do Baú", Element.NEUTRAL)
    room.add_item(item)

    taken_item = room.take_item("Poção De Cura")

    assert taken_item is not None
    assert taken_item.name == "Poção De Cura"
    assert len(room.items) == 0


def test_take_item_not_found(item):
    """Tests taking an item who's not in the room."""
    room = Room("Sala vazia", Element.NEUTRAL)
    room.add_item(item)

    taken_item = room.take_item("Espada Lendária")

    assert taken_item is None
    assert len(room.items) == 1


# INTEGRATION TESTS:


def test_integration_hero_loots_room(hero, item):
    """
    Tests the following walkthrough:
    1. ROOM have ITEM.
    2. HERO tries to take it.
    3. ROOM gives it.
    4. HERO stores it in INVENTORY.
    """

    room = Room("Sala do Tesouro", Element.NEUTRAL)
    room.add_item(item)

    found_item = room.take_item("Poção De Cura")

    if found_item:
        success = hero.inventory.add_item_to_inventory(found_item)

    assert success is True
    assert len(room.items) == 0
    assert len(hero.inventory.items) == 1
    assert hero.inventory.items[0].name == "Poção De Cura"


def test_integration_hero_cannot_loot_heavy_items(hero, heavy_item):
    """FAIL SCNEARIO: HERO picks up an item, but it's too heavy and he drops it."""

    room = Room("Caverna", Element.NEUTRAL)
    room.add_item(heavy_item)

    found_item = room.take_item("Pedra Grande")

    success = False
    if found_item:
        success = hero.inventory.add_item_to_inventory(found_item)

    assert success is False
    assert len(hero.inventory.items) == 0
    assert len(room.items) == 0
