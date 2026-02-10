from domain.state import (
    NeutralState,
    PoisonedState,
    BurnState,
    StunnedState,
    FrozenState,
)
from domain.element import Element


class FakeEntity:
    """
    Fake class for State tests.
    """

    def __init__(self):
        self.received_damage = []
        self.attack = 10
        self.speed = 10

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


def test_burn_state_reduces_attack():
    state = BurnState(duration_turns=2, attack_decrease=3)
    entity = FakeEntity()

    state.apply_effect(entity)

    assert entity.attack == 7


def test_burn_state_reduces_duration():
    state = BurnState(duration_turns=2, attack_decrease=3)
    entity = FakeEntity()

    state.apply_effect(entity)

    assert state.duration_turns == 1


def test_burn_state_does_not_prevent_action():
    state = BurnState(duration_turns=1, attack_decrease=3)

    assert state.prevents_action() is False


def test_stunned_state_prevents_action():
    state = StunnedState(duration_turns=1)

    assert state.prevents_action() is True


def test_stunned_state_reduces_duration():
    state = StunnedState(duration_turns=2)
    entity = FakeEntity()

    state.apply_effect(entity)

    assert state.duration_turns == 1


def test_frozen_state_reduces_speed():
    state = FrozenState(duration_turns=2, speed_decrease=4)
    entity = FakeEntity()

    state.apply_effect(entity)

    assert entity.speed == 6


def test_frozen_state_reduces_duration():
    state = FrozenState(duration_turns=2, speed_decrease=4)
    entity = FakeEntity()

    state.apply_effect(entity)

    assert state.duration_turns == 1


def test_frozen_state_does_not_prevent_action():
    state = FrozenState(duration_turns=1, speed_decrease=4)

    assert state.prevents_action() is False
