from enum import Enum


class Elemento(Enum):
    """Enum que representa os elementos do jogo.

    Elementos seguem um ciclo de vantagens:
    VENENO -> RAIO -> GELO -> FOGO -> VENENO

    NEUTRO não tem vantagem nem desvantagem sobre nenhum elemento.

    Attributes:
        FOGO: Elemento de fogo.
        GELO: Elemento de gelo.
        RAIO: Elemento de raio.
        VENENO: Elemento de veneno.
        NEUTRO: Elemento neutro.
    """

    FOGO = "fogo"
    GELO = "gelo"
    RAIO = "raio"
    VENENO = "veneno"
    NEUTRO = "neutro"

    def tem_vantagem_sobre(self, outro: "Elemento") -> bool:
        if self == Elemento.NEUTRO or outro == Elemento.NEUTRO:
            return False

        vantagens = {
            Elemento.VENENO: Elemento.RAIO,
            Elemento.RAIO: Elemento.GELO,
            Elemento.GELO: Elemento.FOGO,
            Elemento.FOGO: Elemento.VENENO,
        }

        return vantagens.get(self) == outro

    def multiplicador(self, outro: "Elemento") -> float:
        if self == Elemento.NEUTRO or outro == Elemento.NEUTRO:
            return 1.0

        vantagens = {
            Elemento.VENENO: Elemento.RAIO,
            Elemento.RAIO: Elemento.GELO,
            Elemento.GELO: Elemento.FOGO,
            Elemento.FOGO: Elemento.VENENO,
        }

        if vantagens.get(self) == outro:
            return 2.0

        if vantagens.get(outro) == self:
            return 0.5

        return 1.0
