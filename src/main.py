# main.py

# Ajuste os imports dependendo de onde as classes estão (ex: src.cli import CLI)
from infra.cli import CLI
from infra.game_manager import GameManager

def main():
    # 1. Instanciamos a interface visual
    interface = CLI()
    
    # 2. Injetamos a interface no Orquestrador
    jogo = GameManager(interface)
    
    # 3. Damos o Play!
    try:
        jogo.start_game()
    except Exception as e:
        print(f"\n[ERRO CRÍTICO NO JOGO]: {e}")
        # Se der erro, ele vai te mostrar exatamente o que quebrou!

if __name__ == "__main__":
    main()
