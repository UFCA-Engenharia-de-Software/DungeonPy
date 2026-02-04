import pytest
from domain.entity import Entity
from domain.element import Element

"""
# 1. WE CREATE A FAKE (CONCRETE) CLASS JUST FOR TESTING
# It inherits from Entity and implements the required methods with "do nothing" bodies
# We need to do this because of the abstract methods in Entity; it cannot be instantiated directly, it needs a child class with its own "customized" methods

"""


class EntidadeTeste(Entity):
    def strike(self, target):
        pass


def test_constructor():
    entity_generic = EntidadeTeste("Monstrengo", 100, 90, 20, 10)

    assert entity_generic.name == "Monstrengo"
    assert entity_generic.max_life == 100
    assert entity_generic.current_life == 90
    assert entity_generic.attack == 20
    assert entity_generic.speed == 10
    assert entity_generic.element == Element.NEUTRAL

    # Testing attribute passing
    entity_generic = EntidadeTeste("Monstrengo", 100, 90, 20, 10, element=Element.FIRE)
    assert entity_generic.element == Element.FIRE


def test_is_it_alive():
    entity_generic = EntidadeTeste("Monstrengo", 100, 90, 20, 10)

    assert entity_generic.is_it_alive()

    entity_generic.current_life = 0

    assert not entity_generic.is_it_alive()


def test_current_life_logics():
    monstrao_do_grau = EntidadeTeste("Slime", 100, 50, 10, 5)

    # A negative life must turn into 0
    monstrao_do_grau.current_life = -9999
    assert monstrao_do_grau.current_life == 0

    # Current life cannot surpass the Max Life
    monstrao_do_grau.current_life = 1000
    assert monstrao_do_grau.current_life == monstrao_do_grau.max_life

    # Testing the constructor
    monstrao_do_grau = EntidadeTeste("Slime", 100, 500, 10, 5)
    assert monstrao_do_grau.current_life == 100


def test_combats_attributes_logics():
    monstrao_do_grau = EntidadeTeste("Slime", 100, 50, 10, 5)

    monstrao_do_grau.attack = -1
    assert monstrao_do_grau.attack == 0

    monstrao_do_grau.speed = -1
    assert monstrao_do_grau.speed == 0


def test_name_errors():
    # Error
    with pytest.raises(TypeError):
        EntidadeTeste(123, 100, 50, 10, 5)

    # logic error
    with pytest.raises(ValueError):
        EntidadeTeste("", 100, 50, 10, 5)


def test_current_life_errors():
    with pytest.raises(TypeError):
        EntidadeTeste("Slime", 100, "50", 10, 5)

    monstrao_do_grau = EntidadeTeste("Slime", 100, 50, 10, 5)

    with pytest.raises(TypeError):
        monstrao_do_grau.current_life = "zoltrak"


def test_max_life():
    # Logic error
    with pytest.raises(ValueError):
        EntidadeTeste("Slime", 0, 50, 10, 5)

    # Error
    with pytest.raises(TypeError):
        EntidadeTeste("Slime", "0", 50, 10, 5)


def test_combats_attributes_errors():
    # Test Attack
    with pytest.raises(TypeError):
        EntidadeTeste("Slime", 100, 99, "1", 2)

    # Test Speed
    with pytest.raises(TypeError):
        EntidadeTeste("Slime", 100, 99, 1, "9")


def test_damage_elemental_interaction():
    monstro_fogo = EntidadeTeste("Chama", 100, 100, 10, 5, element=Element.FIRE)

    # Neutral damage
    # 10 of damage -> needs to decrease life to 90 (current_life it´s 100)
    monstro_fogo.damage_received(10, Element.NEUTRAL)
    assert monstro_fogo.current_life == 90

    # damage by weakness
    # 10 of damage -> needs to descrease life to 70 (Multiplier it´s 2)
    monstro_fogo.damage_received(10, Element.ICE)
    assert monstro_fogo.current_life == 70

    # damage by resistence
    # 20 of damage -> needs to decrease life to 60 (Multiplier it´s 0.5)
    monstro_fogo.damage_received(20, Element.POISON)
    assert monstro_fogo.current_life == 60


def test_element_errors():
    with pytest.raises(TypeError):
        EntidadeTeste("Chama", 100, 100, 10, 5, element="fogo_falso")

    entity = EntidadeTeste("Chama", 100, 100, 10, 5, element=Element.FIRE)
    with pytest.raises(TypeError):
        entity.element = "gelo_fake"
