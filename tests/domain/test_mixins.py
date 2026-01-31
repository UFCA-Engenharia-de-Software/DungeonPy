from domain.mixins import DescriptionMixin
import pytest


def test_mixin_implemented_correctly():
    class EntityWithDescription(DescriptionMixin):
        def get_description(self) -> str:
            return "Test description"

    entity = EntityWithDescription()
    assert entity.get_description() == "Test description"


def test_mixin_not_implemented():
    class EntityWithoutImplementation(DescriptionMixin):
        pass

    entity = EntityWithoutImplementation()
    with pytest.raises(NotImplementedError):
        entity.get_description()
