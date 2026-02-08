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
    def __init__(self, duration_turns, damage_per_turns):
        super().__init__("Poison", duration_turns)
        self.damage_per_turns = damage_per_turns

    def apply_effect(self, entity):
        entity.damage_received(
            value=self.damage_per_turns, strike_element=Element.POISON
        )

        self.duration_turns -= 1

    def prevents_action(self):
        return False
