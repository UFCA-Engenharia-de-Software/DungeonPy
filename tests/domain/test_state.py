from domain.state import (
    NeutralState,
    PoisonedState,
    BurnState,
    FrozenState,
    StunnedState,
)
from domain.element import Element


class FakeEntity:
    """Entidade falsa blindada com getters e setters para os testes."""

    def __init__(self):
        self._attack = 10
        self._speed = 10
        self.current_status = None
        self.received_damage = []

    # Liberando o acesso total ao Ataque para o teste funcionar
    @property
    def attack(self):
        return self._attack

    @attack.setter
    def attack(self, value):
        self._attack = value

    # Liberando o acesso total à Velocidade para o teste funcionar
    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value

    def damage_received(self, value, strike_element):
        self.received_damage.append((value, strike_element))
        pass

    def set_status(self, status):
        self.current_status = status


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
    entity.attack = 10  # Vida/Ataque inicial

    state.apply_effect(entity)

    assert entity.attack == 7


def test_burn_state_restores_attack_after_expiration():
    state = BurnState(duration_turns=1, attack_decrease=3)
    entity = FakeEntity()
    entity.attack = 10

    state.apply_effect(entity)

    assert entity.attack == 10


def test_burn_state_does_not_prevent_action():
    state = BurnState(duration_turns=1, attack_decrease=3)

    assert state.prevents_action() is False


def test_frozen_state_applies_speed_modifier():
    state = FrozenState(duration_turns=2, speed_decrease=4)
    entity = FakeEntity()
    entity.speed = 10

    state.apply_effect(entity)

    # Verifica se a velocidade caiu de 10 para 6
    assert entity.speed == 6


def test_frozen_state_restores_speed_after_expiration():
    state = FrozenState(duration_turns=1, speed_decrease=4)
    entity = FakeEntity()
    entity.speed = 10

    state.apply_effect(entity)

    # Como durava só 1 turno, a velocidade já deve ter sido devolvida!
    assert entity.speed == 10


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
