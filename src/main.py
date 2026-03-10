from infra.cli import CLI
from infra.game_manager import GameManager


def main():
    interface = CLI()

    jogo = GameManager(interface)

    try:
        jogo.start_game()
    except Exception as e:
        print(f"\n[ERRO CRÍTICO NO JOGO]: {e}")


if __name__ == "__main__":
    main()
