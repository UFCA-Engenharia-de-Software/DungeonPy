from abc import ABC, abstractmethod


class Entity(ABC):
    def __init__(
        self,
        name: str,
        max_life: int,
        current_life: int,
        attack: int,
        speed: int,
        current_status=None,
    ):
        """
        Anotação de correção de diagrama: max_life precisa vir primeiro que current life.

        Anotações ao decorrer do código:
        current_life pode ser 0 por definir se a entidade está viva ou morta.
        Ainda em current_life, ela precisa voltar a ser 0, caso se torne negativa.
        Se uma entidade sofre um dano que deixa a vida maior que 0 ou recupera uma vida maior que a sua máxima, o sistema não pode crachar, mas redefinir seus valores para uma quantidade coerente.

        Dagame_receive é um método abstrato, pois, dependendo da classe filha de entity os modificadores do cálculo mudam, exemplo: "Mostros possuem fraquezas e resistências elementais." | "Guerreiro possui defesa". (Polimorfismo)
        O método abstrato serve para dizer que toda classe filha precisa fazer seu próprio método damage_received

        Justificativa do nome do método "atacar". No ingês, o atacar e ataque são attack, então, para o método atacar, escolhi a palavra "strike".

        Strike também é um método abstrato pelo mesmo raciocínio de damage_receive

        justificativa de nome "estar_vivo" método para is it alive ? assim, o nome fica mais coerente com a função do método: "Verificar estado do da entidade"

        Sobre "is it alive": Dentro do método ocorre a importação da classe State, assim, é possível fazer a validação do atributo passado sem acontecer um erro de Circular Import. None vai ser trocado para State. Por que passar State, leva a aceitar as classes filhas ? Pela Herança, garantindo que o Veneno seja um Estado, e pelo Polimorfismo permitindo que a gente passe o Veneno onde se espera um Estado. Herança e Polimorfismo andam sempre juntos.)

        """
        self.name = name
        self.max_life = max_life
        self.current_life = current_life
        self.attack = attack
        self.speed = speed
        self.current_status = current_status

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
        if valor is None:
            self.__current_status = None
            return

        # from src.domain.estados import state -> para evitar quebrar o código com importações em ciclo

        # else not isinstance(valor, "state"): (Precisa mudar para quando classe Estado estiver pronta)
        # raise TypeError("current_status must be a object from state")
        self.__current_status = valor

    @abstractmethod
    def damage_received(self, valor: int) -> None:
        pass

    @abstractmethod
    def strike(self, target) -> None:
        pass

    def set_status(self, new_status) -> None:
        # from .src.domain import state -> para evitar quebrar o código com importações em ciclo

        # if not isinstance(new_status,None):
        # raise TypeError("New status must be a STATE object")

        self.current_status = new_status

    def is_it_alive(self) -> bool:
        return self.current_life > 0
