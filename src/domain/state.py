from abc import ABC, abstractmethod
from domain.element import Element


class State(ABC):
    """
    The State class is designed to assign status effects to other classes.
    By following the advantage order over Elements, it is possible to apply effects
    that may or may not prevent the hero/monster from taking action.

    """

    def __init__(self, name: str, duration_turns: int):
        self.name = name
        self.duration_turns = duration_turns

    @abstractmethod
    def apply_effect(self, entity):
        pass

    @abstractmethod
    def prevents_action(self) -> bool:
        pass


class NeutralState(State):
    """
    Expected effect of Neutral:
    - Applies no effects.
    - Does not prevent action.
    """

    def __init__(self):
        super().__init__("Neutral", 0)

    def apply_effect(self, entity):
        pass

    def prevents_action(self):
        return False


class PoisonedState(State):
    """
    Expected effect of Poisoned:
    - Applies poisoned status (x damage per turn).
    - Does not prevent action.
    """

    def __init__(self, duration_turns, damage_per_turns: int):
        super().__init__("Poison", duration_turns)
        self.damage_per_turns = damage_per_turns

    def apply_effect(self, entity):
        entity.damage_received(
            value=self.damage_per_turns, strike_element=Element.POISON
        )

        self.duration_turns -= 1

    def prevents_action(self):
        return False


class BurnState(State):
    """
    Expected effect of Burn:
    - Temporarily reduces attack.
    - Does not prevent action.
    """

    def __init__(self, duration_turns: int, attack_decrease: int):
        super().__init__("Burned", duration_turns)
        self.attack_decrease = attack_decrease
        self._applied = False

    def apply_effect(self, entity):
        if not self._applied:
            entity.attack_modifiers.append(-self.attack_decrease)
            self._applied = True

        self.duration_turns -= 1

        if self.duration_turns <= 0:
            entity.attack_modifiers.remove(-self.attack_decrease)

    def prevents_action(self) -> bool:
        return False


class StunnedState(State):
    """
    Expected effect of Stunned:
    - Prevents action for the duration.
    - Applies no damage.
    """

    def __init__(self, duration_turns: int = 1):
        super().__init__("Stunned", duration_turns)

    def apply_effect(self, entity):
        self.duration_turns -= 1

    def prevents_action(self):
        return True


class FrozenState(State):
    """
    Expected effect of Frozen:
    - Temporarily reduces speed.
    - Does not prevent action.
    """

    def __init__(self, duration_turns: int, speed_decrease: int):
        super().__init__("Frozen", duration_turns)
        self.speed_decrease = speed_decrease
        self._applied = False

    def apply_effect(self, entity):
        if not self._applied:
            entity.speed_modifiers.append(-self.speed_decrease)
            self._applied = True

        self.duration_turns -= 1

        if self.duration_turns <= 0:
            entity.speed_modifiers.remove(-self.speed_decrease)

    def prevents_action(self) -> bool:
        return False
