from dataclasses import dataclass
from datetime import datetime

from domain.hero import Hero


@dataclass
class GameState:
    """Represents the complete state of a saved game session.

    Coordinates all information needed to persist and restore
    a game session, including the current hero, level progress,
    and save metadata for versioning.

    Attributes:
        hero (Hero): The player's hero instance (Warrior/Mage/Archer).
        current_level (int): Current dungeon level (1 to MAX_LEVELS).
        save_date (str): ISO format timestamp of when the game was saved.
        game_version (str): Version string for save compatibility.
    """

    hero: Hero
    current_level: int
    save_date: str
    game_version: str = "0.1.0"

    MAX_LEVELS = 5

    @classmethod
    def create_new_game(cls, hero: Hero) -> "GameState":
        return cls(
            hero=hero,
            current_level=1,
            save_date=datetime.now().isoformat(),
            game_version="0.1.0",
        )

    @classmethod
    def from_dict(cls, data: dict, hero: Hero) -> "GameState":
        try:
            current_level = data["current_level"]
            save_date = data["save_date"]
        except KeyError as e:
            raise ValueError(f"Save corrompido: campo obrigatório ausente - {e}")

        if not isinstance(current_level, int):
            raise ValueError(
                f"Nível deve ser um inteiro, recebido: {type(current_level)}"
            )

        if current_level < 1 or current_level > cls.MAX_LEVELS + 1:
            raise ValueError(f"Save corrompido: nível {current_level} é inválido")

        return cls(
            hero=hero,
            current_level=current_level,
            save_date=save_date,
            game_version=data.get("game_version", "0.1.0"),
        )

    def to_dict(self) -> dict:
        return {
            "current_level": self.current_level,
            "save_date": self.save_date,
            "game_version": self.game_version,
        }

    def unlock_next_level(self) -> None:
        if not self.is_game_completed():
            self.current_level += 1
            self.update_save_timestamp()

    def update_save_timestamp(self) -> None:
        self.save_date = datetime.now().isoformat()

    def is_game_completed(self) -> bool:
        return self.current_level > self.MAX_LEVELS

    def get_progress_info(self) -> dict:
        if self.is_game_completed():
            return {
                "status": "Completo",
                "progresso": "Jogo Completo!",
                "porcentagem": 100.0,
            }

        porcentagem = ((self.current_level - 1) / self.MAX_LEVELS) * 100

        return {
            "status": "em_progresso",
            "progresso": f"Fase {self.current_level} de {self.MAX_LEVELS}",
            "porcentagem": round(porcentagem, 1),
        }
