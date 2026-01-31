from domain.element import Element


def test_has_advantage_over_returns_true_when_there_is_advantage():
    fire_element = Element.FIRE
    ice_element = Element.ICE

    assert ice_element.has_advantage_over(fire_element) is True


def test_multiplier_returns_1_when_neutral_element():
    neutral_element = Element.NEUTRAL
    fire_element = Element.FIRE

    assert neutral_element.multiplier(fire_element) == 1.0


def test_multiplier_returns_05_when_there_is_disadvantage():
    fire_element = Element.FIRE
    ice_element = Element.ICE

    assert fire_element.multiplier(ice_element) == 0.5
