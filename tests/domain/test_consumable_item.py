import pytest
from domain.consumable_item import ConsumableItem
from domain.warrior import Warrior


def test_constructor():
    pocao = ConsumableItem(
        name="bebidinha_da_massa",
        description="gostin de guaraná",
        weight=1,
        recovered_value=10,
    )

    assert pocao.name == "Bebidinha_Da_Massa"

    assert pocao._description == "gostin de guaraná"

    assert pocao.weight == 1

    assert pocao.recovered_value == 10


def test_validation_recovered_value():
    with pytest.raises(TypeError):
        ConsumableItem(
            name="refri", description="SABOR", weight=1, recovered_value="12"
        )

    with pytest.raises(ValueError):
        ConsumableItem(name="refri", description="SABOR", weight=1, recovered_value=0)

    with pytest.raises(ValueError):
        ConsumableItem(name="refri", description="SABOR", weight=1, recovered_value=-1)


def test_constructor_default_recovery_type():
    pocao = ConsumableItem(
        name="Poção de Cura",
        description="Recupera vida",
        weight=0.5,
        recovered_value=25,
    )
    assert pocao.recovery_type == "life"


def test_constructor_mana_recovery_type():
    pocao = ConsumableItem(
        name="Poção de Mana",
        description="Recupera mana",
        weight=0.5,
        recovered_value=20,
        recovery_type="mana",
    )
    assert pocao.recovery_type == "mana"


def test_invalid_recovery_type_raises():
    import pytest

    with pytest.raises(ValueError):
        ConsumableItem(
            name="Poção Estranha",
            description="Tipo inválido",
            weight=0.5,
            recovered_value=10,
            recovery_type="stamina",
        )


def test_use_mana_heals_mage():
    from domain.mage import Mage
    from domain.element import Element

    mago = Mage(
        name="Gandalf",
        max_life=80,
        current_life=80,
        max_mana=100,
        current_mana=40,
        attack=50,
        speed=15,
        element=Element.FIRE,
    )

    pocao_mana = ConsumableItem(
        name="Poção de Mana",
        description="Recupera mana",
        weight=0.5,
        recovered_value=30,
        recovery_type="mana",
    )

    pocao_mana.use(mago)
    assert mago.current_mana == 70
    assert mago.current_life == 80  # life not change


def test_use_mana_on_non_mage_raises():
    import pytest

    pocao_mana = ConsumableItem(
        name="Poção de Mana",
        description="Recupera mana",
        weight=0.5,
        recovered_value=20,
        recovery_type="mana",
    )

    guerreiro = Warrior(
        name="Errant Knight",
        max_life=200,
        current_life=100,
        attack=25,
        speed=25,
    )

    with pytest.raises(TypeError):
        pocao_mana.use(guerreiro)


def test_use_life_potion_does_not_restore_mana():
    from domain.mage import Mage
    from domain.element import Element

    mago = Mage(
        name="Merlim",
        max_life=80,
        current_life=50,
        max_mana=100,
        current_mana=40,
        attack=50,
        speed=15,
        element=Element.FIRE,
    )

    pocao_vida = ConsumableItem(
        name="Poção de Cura",
        description="Recupera vida",
        weight=0.5,
        recovered_value=20,
    )

    pocao_vida.use(mago)
    assert mago.current_life == 70
    assert mago.current_mana == 40  # mana not change


def test_use_normal_heal():
    # Testing if pocao recoveres the warrior´s life correctly
    guerreirozin = Warrior(
        name="Errant Knight",
        max_life=200,
        current_life=100,
        attack=25,
        speed=25,
    )

    pocao = ConsumableItem(
        name="bebidinha_da_massa",
        description="gostin de guaraná",
        weight=1,
        recovered_value=10,
    )

    pocao.use(guerreirozin)

    assert guerreirozin.current_life == 110
