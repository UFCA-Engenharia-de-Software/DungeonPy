import pytest
from services.level_factory import LevelFactory
from domain.element import Element
from domain.room import Room


def test_create_level_return_room():
    salinha = LevelFactory.create_room(level=1, environment=Element.FIRE)

    assert isinstance(salinha, Room)


def test_level_validation():
    with pytest.raises(ValueError):
        LevelFactory.create_room(level=0, environment=Element.FIRE)


def test_environment_validation():
    with pytest.raises(TypeError):
        LevelFactory.create_room(level=2, environment=int)


def testing_boss_creation():
    salinha = LevelFactory.create_room(level=4, environment=Element.FIRE)

    assert salinha.monsters[1].attack > salinha.monsters[0].attack


def test_no_arguments_for_enviroment():
    salinha = LevelFactory.create_room(level=1)

    assert isinstance(salinha.environment, Element)
