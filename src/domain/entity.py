from abc import ABC, abstractmethod
from domain.element import Element
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.state import State


class Entity(ABC):
    def __init__(
        self,
        name: str,
        max_life: int,
        current_life: int,
        attack: int,
        speed: int,
        current_status: "State" = None,
        element: Element = Element.NEUTRAL,
    ):
        """

        Initializes the Entity with combat stats and elemental affinity.

        Args:
            element (Element): The natural element of the entity. Used to calculate
                               weakness and resistance when receiving damage.
                               Defaults to Element.NEUTRAL.

        """
        self.name = name
        self.max_life = max_life
        self.current_life = current_life
        self.attack = attack
        self.speed = speed
        self.current_status = current_status
        self.element = element

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, valor):
        if not isinstance(valor, str):
            raise TypeError("the attribute Name must be a string")

        if len((valor.strip())) == 0:
            raise ValueError("Name cannot be empty")

        self.__name = valor.strip().title()

    @property
    def max_life(self):
        return self.__max_life

    @max_life.setter
    def max_life(self, valor):
        if not isinstance(valor, int):
            raise TypeError("Max life must be a whole number")

        if valor <= 0:
            raise ValueError("Max life must be greater than 0")

        self.__max_life = valor

    @property
    def current_life(self):
        return self.__current_life

    @current_life.setter
    def current_life(self, valor):
        if not isinstance(valor, int):
            raise TypeError("Current life needs to be a whole number")

        if valor < 0:
            self.__current_life = 0

        elif valor > self.max_life:
            self.__current_life = self.max_life

        else:
            self.__current_life = valor

    @property
    def attack(self):
        return self.__attack

    @attack.setter
    def attack(self, valor):
        if not isinstance(valor, int):
            raise TypeError("The attack value needs to be a whole number")

        if valor < 0:
            self.__attack = 0

        else:
            self.__attack = valor

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, valor):
        if not isinstance(valor, int):
            raise TypeError("The speed value needs to be a whole number")

        if valor < 0:
            self.__speed = 0

        else:
            self.__speed = valor

    @property
    def current_status(self):
        return self.__current_status

    @current_status.setter
    def current_status(self, valor):
        from domain.state import State, NeutralState

        if valor is None:
            self.__current_status = NeutralState()
            return

        if not isinstance(valor, State):
            raise TypeError("current_status must be a object from state")

        self.__current_status = valor

    @property
    def element(self):
        return self.__element

    @element.setter
    def element(self, value):
        if not isinstance(value, Element):
            raise TypeError(
                "element must be a Element attribute. Example: 'Element.ICE'"
            )

        self.__element = value

    def damage_received(self, value: int, strike_element: Element) -> None:
        multiplier = strike_element.multiplier(self.element)

        final_damage = int(value * multiplier)

        self.current_life -= final_damage

    @abstractmethod
    def strike(self, target) -> None:
        pass

    def set_status(self, new_status) -> None:
        self.current_status = new_status

    def is_it_alive(self) -> bool:
        return self.current_life > 0
