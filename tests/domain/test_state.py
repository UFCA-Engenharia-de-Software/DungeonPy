from domain.state import (
    NeutralState,
    PoisonedState,
    BurnState,
    FrozenState,
    StunnedState,
)
from domain.element import Element


class FakeEntity:
    """
    Fake class for State tests.
    Simulates temporary modifiers.
    """

    def __init__(self):
        self.received_damage = []
        self.base_attack = 10
        self.base_speed = 10
        self.attack_modifiers = []
        self.speed_modifiers = []

    @property
    def attack(self):
        return self.base_attack + sum(self.attack_modifiers)

    @property
    def speed(self):
        return self.base_speed + sum(self.speed_modifiers)

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


def test_burn_state_applies_attack_modifier():
    state = BurnState(duration_turns=2, attack_decrease=3)
    entity = FakeEntity()

    state.apply_effect(entity)

    assert entity.attack == 7
    assert -3 in entity.attack_modifiers


def test_burn_state_restores_attack_after_expiration():
    state = BurnState(duration_turns=1, attack_decrease=3)
    entity = FakeEntity()

    state.apply_effect(entity)

    assert entity.attack == 10
    assert entity.attack_modifiers == []


def test_burn_state_does_not_prevent_action():
    state = BurnState(duration_turns=1, attack_decrease=3)

    assert state.prevents_action() is False


def test_frozen_state_applies_speed_modifier():
    state = FrozenState(duration_turns=2, speed_decrease=4)
    entity = FakeEntity()

    state.apply_effect(entity)

    assert entity.speed == 6
    assert -4 in entity.speed_modifiers


def test_frozen_state_restores_speed_after_expiration():
    state = FrozenState(duration_turns=1, speed_decrease=4)
    entity = FakeEntity()

    state.apply_effect(entity)

    assert entity.speed == 10
    assert entity.speed_modifiers == []


def test_frozen_state_does_not_prevent_action():
    state = FrozenState(duration_turns=1, speed_decrease=4)

    assert state.prevents_action() is False


def test_stunned_state_prevents_action():
    state = StunnedState(duration_turns=1)

    assert state.prevents_action() is True


def test_stunned_state_reduces_duration():
    state = StunnedState(duration_turns=2)
    entity = FakeEntity()

    state.apply_effect(entity)

    assert state.duration_turns == 1
