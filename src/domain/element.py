from enum import Enum


class Element(Enum):
    """Enum that represents the game elements.

    Elements follow an advantage cycle:
    POISON -> LIGHTNING -> ICE -> FIRE -> POISON

    NEUTRAL has no advantage or disadvantage over any element.

    Attributes:
        FIRE: Fire element.
        ICE: Ice element.
        LIGHTNING: Lightning element.
        POISON: Poison element.
        NEUTRAL: Neutral element.
    """

    FIRE = "fire"
    ICE = "ice"
    LIGHTNING = "lightning"
    POISON = "poison"
    NEUTRAL = "neutral"

    @property
    def _advantages(self) -> dict["Element", "Element"]:
        return {
            Element.POISON: Element.LIGHTNING,
            Element.LIGHTNING: Element.ICE,
            Element.ICE: Element.FIRE,
            Element.FIRE: Element.POISON,
        }

    def has_advantage_over(self, other: "Element") -> bool:
        if self == Element.NEUTRAL or other == Element.NEUTRAL:
            return False

        return self._advantages.get(self) == other

    def multiplier(self, other: "Element") -> float:
        if self == Element.NEUTRAL or other == Element.NEUTRAL:
            return 1.0

        if self._advantages.get(self) == other:
            return 2.0

        if self._advantages.get(other) == self:
            return 0.5

        return 1.0
