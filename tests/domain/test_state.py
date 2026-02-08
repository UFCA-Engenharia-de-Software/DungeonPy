from domain.state import NeutralState, PoisonedState
from domain.element import Element


class FakeEntity:
    """
    This is a 'Fake Class' for tests in state.
    """
    def __init__(self):
        self.received_damage = []

    def damage_received(self, value, strike_element):
        self.received_damage.append((value, strike_element))


def test_neutral_state_does_not_prevent_action():
    state = NeutralState()
    assert state.prevents_action() is False


def test_neutral_state_does_not_apply_effect():
    state = NeutralState()
    entity = FakeEntity()

    state.apply_effect(entity)

    assert entity.received_damage == []


def test_poisoned_state_applies_damage():
    state = PoisonedState(duration_turns=3, damage_per_turns=5)
    entity = FakeEntity()

    state.apply_effect(entity)

    assert entity.received_damage == [(5, Element.POISON)]


def test_poisoned_state_reduces_duration():
    state = PoisonedState(duration_turns=3, damage_per_turns=5)
    entity = FakeEntity()

    state.apply_effect(entity)

    assert state.duration_turns == 2


def test_poisoned_state_does_not_prevent_action():
    state = PoisonedState(duration_turns=1, damage_per_turns=5)

    assert state.prevents_action() is False
