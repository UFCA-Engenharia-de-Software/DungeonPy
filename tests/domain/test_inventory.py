import pytest

from domain.inventory import Inventory
from domain.item import Item


class MockItem(Item):
    def use(self, target) -> None:
        pass


# Initialization / Capacity


def test_create_inventory_with_default_capacity() -> None:
    inventory = Inventory()
    assert inventory.capacity == 100.0
    assert len(inventory) == 0


def test_capacity_must_be_positive_number() -> None:
    with pytest.raises(TypeError):
        Inventory(capacity="invalid")

    with pytest.raises(ValueError):
        Inventory(capacity=0)


# Add / Can add item


def test_can_add_item_based_on_weight() -> None:
    inventory = Inventory(capacity=10)
    potion = MockItem(name="Potion", weight=5.0)

    assert inventory.can_add_item(potion) is True


def test_cannot_add_item_when_exceeds_capacity() -> None:
    inventory = Inventory(capacity=5)
    sword = MockItem(name="Sword", weight=10.0)

    assert inventory.can_add_item(sword) is False
    assert inventory.add_item_to_inventory(sword) is False
    assert len(inventory) == 0


def test_add_item_successfully() -> None:
    inventory = Inventory()
    potion = MockItem(name="Potion", weight=5.0)

    result = inventory.add_item_to_inventory(potion)

    assert result is True
    assert len(inventory) == 1


def test_add_item_raises_error_when_not_item() -> None:
    inventory = Inventory()

    with pytest.raises(TypeError):
        inventory.add_item_to_inventory("not an item")


# Remove / Find / Has item


def test_remove_item_by_object() -> None:
    inventory = Inventory()
    potion = MockItem(name="Potion", weight=5.0)

    inventory.add_item_to_inventory(potion)

    assert inventory.remove_item_from_inventory(potion) is True
    assert len(inventory) == 0


def test_find_and_remove_item_by_name_case_insensitive() -> None:
    inventory = Inventory()
    potion = MockItem(name="Health Potion", weight=5.0)

    inventory.add_item_to_inventory(potion)

    assert inventory.has_item("health potion") is True
    assert inventory.remove_item_by_name("HEALTH POTION") is True
    assert inventory.has_item("health potion") is False


def test_remove_nonexistent_item_returns_false() -> None:
    inventory = Inventory()

    assert inventory.remove_item_by_name("Nonexistent") is False


# Summary / List


def test_get_items_summary() -> None:
    inventory = Inventory(capacity=20)
    inventory.add_item_to_inventory(MockItem(name="Potion", weight=5.0))

    summary = inventory.get_items_summary()

    assert summary["capacity"] == 20.0
    assert summary["current_weight"] == 5.0
    assert summary["available_capacity"] == 15.0
    assert summary["item_count"] == 1
    assert summary["items"][0]["name"] == "Potion"


def test_list_all_items_empty() -> None:
    inventory = Inventory()

    assert inventory.list_all_items() == ["Empty inventory"]


def test_list_all_items_with_content() -> None:
    inventory = Inventory(capacity=50)
    inventory.add_item_to_inventory(MockItem(name="Potion", weight=5.0))

    result = inventory.list_all_items()

    assert "Capacity: 5.0/50.0" in result[0]
    assert "Potion" in result[2]


# Clear / State / Special


def test_clear_inventory() -> None:
    inventory = Inventory()
    inventory.add_item_to_inventory(MockItem(name="Item", weight=5.0))

    inventory.clear_all_items_from_inventory()

    assert inventory.is_empty() is True


def test_len_and_str_special_methods() -> None:
    inventory = Inventory()
    potion = MockItem(name="Potion", weight=5.0)

    inventory.add_item_to_inventory(potion)

    assert len(inventory) == 1
    assert "Potion" in str(inventory)


def test_items_property_returns_copy() -> None:
    inventory = Inventory()
    potion = MockItem(name="Potion", weight=5.0)

    inventory.add_item_to_inventory(potion)

    items_copy = inventory.items
    items_copy.clear()

    assert len(inventory) == 1
