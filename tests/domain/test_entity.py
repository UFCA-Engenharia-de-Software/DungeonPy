import pytest
from src.domain.entity import Entity

"""
# 1. CRIAMOS UMA CLASSE FALSA (CONCRETA) SÓ PARA O TESTE
# Ela herda de Entity e implementa os métodos obrigatórios com "nada"
#Precisamos fazer isso, por causa dos métodos abstratos da entity, onde ela não pode ser executada sozinha, precisa ter uma filha que possui os próprios métodos dela "customizados"

"""


class EntidadeTeste(Entity):
    def strike(self, target):
        pass

    def damage_received(self, valor: int) -> None:
        pass


def test_constructor():
    entity_generic = EntidadeTeste("Monstrengo", 100, 90, 20, 10)

    assert entity_generic.name == "Monstrengo"
    assert entity_generic.max_life == 100
    assert entity_generic.current_life == 90
    assert entity_generic.attack == 20
    assert entity_generic.speed == 10


def test_is_it_alive():
    entity_generic = EntidadeTeste("Monstrengo", 100, 90, 20, 10)

    assert entity_generic.is_it_alive() == True

    entity_generic.current_life = 0

    assert entity_generic.is_it_alive() == False


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
        monstrao_do_grau = EntidadeTeste(123, 100, 50, 10, 5)

    # logic error
    with pytest.raises(ValueError):
        monstrao_do_grau = EntidadeTeste("", 100, 50, 10, 5)


def test_current_life_errors():
    with pytest.raises(TypeError):
        monstrao_do_grau = EntidadeTeste("Slime", 100, "50", 10, 5)

    monstrao_do_grau = EntidadeTeste("Slime", 100, 50, 10, 5)

    with pytest.raises(TypeError):
        monstrao_do_grau.current_life = "zoltrak"


def test_max_life():
    # Logic error
    with pytest.raises(ValueError):
        monstrao_do_grau = EntidadeTeste("Slime", 0, 50, 10, 5)

    # Error
    with pytest.raises(TypeError):
        monstrao_do_grau = EntidadeTeste("Slime", "0", 50, 10, 5)


def test_combats_attributes_errors():
    # Test Attack
    with pytest.raises(TypeError):
        mostrao_do_grau = EntidadeTeste("Slime", 100, 99, "1", 2)

    # Test Speed
    with pytest.raises(TypeError):
        mostrao_do_grau = EntidadeTeste("Slime", 100, 99, 1, "9")
