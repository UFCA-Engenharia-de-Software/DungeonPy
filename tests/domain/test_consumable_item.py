import pytest
from domain.consumable_item import ConsumableItem
from domain.warrior import Warrior

def test_constructor():

    pocao = ConsumableItem(name ="bebidinha_da_massa", description = "gostin de guaraná", weight = 1, recovered_value = 10)
    
    assert pocao.name == "Bebidinha_Da_Massa"

    assert pocao._description == "gostin de guaraná"

    assert pocao.weight == 1

    assert pocao.recovered_value == 10


def test_validation_recovered_value():

    with pytest.raises(TypeError):
        ConsumableItem(name ="refri", description = "SABOR", weight = 1, recovered_value = "12")

    with pytest.raises(ValueError):
        ConsumableItem(name ="refri", description = "SABOR", weight = 1, recovered_value = 0)

    with pytest.raises(ValueError):
        ConsumableItem(name ="refri", description = "SABOR", weight = 1, recovered_value = -1)

def test_use_normal_heal():
    
    #Testing if pocao recoveres the warrior´s life correctly
    guerreirozin = Warrior(
        name="Errant Knight",
        max_life=200,
        current_life=100,
        attack=25,
        speed=25,
    )

    pocao = ConsumableItem(
        name ="bebidinha_da_massa", 
        description = "gostin de guaraná", 
        weight = 1, 
        recovered_value = 10
    )

    pocao.use(guerreirozin)

    assert guerreirozin.current_life == 110

def test_use_prevents_exceeding_max_life():

    #Testing if recovered_valus it´s greater than max_life will return current_life wiht max_life value
    guerreirozin = Warrior(
        name="Errant Knight",
        max_life=200,
        current_life=100,
        attack=25,
        speed=25,
    )

    pocao = ConsumableItem(
        name ="bebidinha_da_massa", 
        description = "gostin de guaraná", 
        weight = 1, 
        recovered_value = 220
    )

    pocao.use(guerreirozin)

    assert guerreirozin.current_life == 200

def test_use_massive_heal_caps_at_max_life():

    #Testing if recovered_value being greaten than the necessary life to recover
    guerreirozin = Warrior(
        name="Errant Knight",
        max_life=200,
        current_life=100,
        attack=25,
        speed=25,
    )

    pocao = ConsumableItem(
        name ="bebidinha_da_massa", 
        description = "gostin de guaraná", 
        weight = 1, 
        recovered_value = 190
    )

    pocao.use(guerreirozin)

    assert guerreirozin.current_life == 200