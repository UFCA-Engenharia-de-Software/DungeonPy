import pytest

from domain.entity import Entity
from domain.item import Item


class ConcreteItem(Item):
    """Concrete implementation of Item for testing purposes."""

    def use(self, target: Entity) -> None:
        """Simple implementation for testing."""
        pass


def test_item_creation() -> None:
    """Test basic item creation."""
    item: Item = ConcreteItem(
        name="Health Potion", description="Restores 50 HP", weight=0.5
    )

    assert item.name == "Health Potion"
    assert item.weight == 0.5
    assert item.get_description() == "Restores 50 HP"


def test_item_creation_with_defaults() -> None:
    """Test item creation with default description."""
    item: Item = ConcreteItem(name="Simple Stone", weight=2.0)

    assert item.name == "Simple Stone"
    assert item.weight == 2.0
    assert "Simple Stone" in item.get_description()


def test_item_name_validation_error() -> None:
    """Test that invalid names raise errors."""
    with pytest.raises(ValueError):
        ConcreteItem(name="", weight=1.0)

    with pytest.raises(TypeError):
        ConcreteItem(name=123, weight=1.0)


def test_item_weight_validation_error() -> None:
    """Test that invalid weights raise errors."""
    with pytest.raises(ValueError):
        ConcreteItem("Item", weight=-1.0)

    with pytest.raises(TypeError):
        ConcreteItem("Item", weight="heavy")


def test_get_description() -> None:
    """Test description with custom and default values."""
    # Custom description
    item1: Item = ConcreteItem("Wand", description="Magic wand", weight=0.3)
    assert item1.get_description() == "Magic wand"

    # Default description
    item2: Item = ConcreteItem("Rock", weight=1.5)
    assert "Rock" in item2.get_description()
