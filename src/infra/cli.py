import os
import sys
import time


class Color:
    # --- Cores Universais (Forçando tons específicos da paleta de 256 cores) ---
    RED = "\033[38;5;196m"  # Vermelho vivo e vibrante
    GREEN = "\033[38;5;46m"  # Verde neon/claro
    YELLOW = "\033[38;5;226m"  # Amarelo canário puro (nunca vai virar marrom!)
    BLUE = "\033[38;5;39m"  # Azul claro vibrante
    MAGENTA = "\033[38;5;201m"  # Magenta/Rosa choque
    CYAN = "\033[38;5;51m"  # Ciano brilhante
    RESET = "\033[0m"  # Reseta para a cor padrão do terminal do usuário

    # --- Cores Escuras / Clássicas ---
    DARK_RED = "\033[38;5;124m"  # Vermelho sangue escuro
    DARK_GREEN = "\033[38;5;28m"  # Verde musgo
    DARK_BLUE = "\033[38;5;21m"  # Azul marinho profundo

    # --- Cores Neutras ---
    WHITE = "\033[38;5;231m"  # Branco puro absoluto
    GRAY = "\033[38;5;244m"  # Cinza médio perfeito para bordas
    BLACK = "\033[38;5;16m"  # Preto puro

    # --- Cores Especiais ---
    BROWN = "\033[38;5;130m"  # Marrom couro
    ORANGE = "\033[38;5;208m"  # Laranja fogo
    PURPLE = "\033[38;5;93m"  # Roxo sombrio


class CLI:
    """
    Classe responsável pela interface visual e interação com o jogador.
    Usa menus interativos com setas do teclado para maior imersão.
    """

    @staticmethod
    def _ler_tecla() -> str:
        """
        Lê a tecla pressionada de forma invisível.
        Funciona tanto no Windows (msvcrt) quanto no Mac/Linux (tty/termios).
        Retorna: 'UP', 'DOWN', 'ENTER' ou 'OTHER'
        """
        if os.name == "nt":  # Se for Windows
            import msvcrt

            tecla = msvcrt.getch()
            if tecla in [b"\xe0", b"\x00"]:  # Setas do teclado no Windows
                direcao = msvcrt.getch()
                if direcao == b"H":
                    return "UP"
                if direcao == b"P":
                    return "DOWN"
            elif tecla == b"\r":  # Enter no Windows
                return "ENTER"
            return "OTHER"

        else:  # Se for Mac ou Linux (Unix)
            import sys
            import tty
            import termios

            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)

                if ch == "\x1b":  # Código de escape para setas no Mac/Linux
                    sys.stdin.read(1)  # Pula o '['
                    direcao = sys.stdin.read(1)
                    if direcao == "A":
                        return "UP"
                    if direcao == "B":
                        return "DOWN"
                elif ch in ["\r", "\n"]:  # Enter no Mac/Linux
                    return "ENTER"
                return "OTHER"
            finally:
                # Restaura o terminal ao normal, para não bugar o console do professor!
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    @staticmethod
    def _limpar_tela() -> None:
        """Limpa o terminal para dar a sensação de transição de tela."""
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def _clear_keyboard_buffer():
        """Clear all keys pressed by the user"""

        import os

        if os.name == "nt":
            import msvcrt

            while msvcrt.kbhit():
                msvcrt.getch()
        else:
            import sys
            import termios

            termios.tcflush(sys.stdin, termios.TCIOFLUSH)

    @staticmethod
    def _mostrar_menu_interativo(
        titulo: str, opcoes: list[str], arte_ascii: str = ""
    ) -> int:
        """
        Desenha um menu interativo e retorna o ÍNDICE da opção escolhida.
        """
        indice_atual = 0

        while True:
            CLI._limpar_tela()

            if arte_ascii:
                print(arte_ascii)

            print(f"{Color.GRAY}=" * 60 + Color.RESET)
            print(f"{titulo:^60}")
            print(f"{Color.GRAY}=" * 60 + f"{Color.RESET}\n")

            for i, opcao in enumerate(opcoes):
                if i == indice_atual:
                    print(
                        f"  {Color.GREEN}►{Color.RESET} {opcao} {Color.GREEN}◄{Color.RESET}"
                    )
                else:
                    print(f"    {opcao}  ")

            print("\n" + f"{Color.GRAY}-" * 60 + Color.RESET)
            footer = "[Use as setas ↑ ↓ para mover e ENTER para confirmar]"
            print(f"{Color.GRAY}{footer.center(60)}{Color.RESET}")

            acao = CLI._ler_tecla()

            if acao == "UP":
                indice_atual = (indice_atual - 1) % len(opcoes)
            elif acao == "DOWN":
                indice_atual = (indice_atual + 1) % len(opcoes)
            elif acao == "ENTER":
                return indice_atual

    @staticmethod
    def show_main_menu(has_save: bool = False) -> str:
        """Exibe o menu principal com a arte do jogo e subtítulo."""

        art_colored = f"""

{Color.BLUE}▄▄▄▄▄▄                                       {Color.YELLOW}▄▄▄▄▄▄▄         {Color.RESET}
{Color.BLUE}███▀▀██▄                                     {Color.YELLOW}███▀▀███▄       {Color.RESET}
{Color.BLUE}███  ███ ██ ██ ████▄ ▄████ ▄█▀█▄ ▄███▄ ████▄ {Color.YELLOW}███▄▄███▀ ██ ██ {Color.RESET}
{Color.BLUE}███  ███ ██ ██ ██ ██ ██ ██ ██▄█▀ ██ ██ ██ ██ {Color.YELLOW}███▀▀▀▀   ██▄██ {Color.RESET}
{Color.BLUE}██████▀  ▀██▀█ ██ ██ ▀████ ▀█▄▄▄ ▀███▀ ██ ██ {Color.YELLOW}███        ▀██▀ {Color.RESET}
{Color.BLUE}                        ██                   {Color.YELLOW}            ██  {Color.RESET}
{Color.BLUE}                      ▀▀▀                    {Color.YELLOW}          ▀▀▀   {Color.RESET}
        """

        subtitle = "  Uma jornada de sombras, escolhas e perdas ".center(60)
        subtitle_colored = f"{Color.CYAN}{subtitle}{Color.RESET}"
        version = "v1.0.0".rjust(58)
        version_colored = f"{Color.YELLOW}{version}{Color.RESET}"

        arte_completa = f"{art_colored}\n{subtitle_colored}\n\n{version_colored}\n"

        if has_save:
            opcoes = [
                f"{Color.GREEN}Continuar Jornada{Color.RESET}",
                f"{Color.YELLOW}Iniciar Nova Jornada{Color.RESET}",
                f"{Color.RED}Sair do Jogo{Color.RESET}",
            ]
        else:
            opcoes = [
                f"{Color.YELLOW}Iniciar Nova Jornada{Color.RESET}",
                f"{Color.RED}Sair do Jogo{Color.RESET}",
            ]

        escolha_idx = CLI._mostrar_menu_interativo(
            f"{Color.BROWN}M E N U   P R I N C I P A L{Color.RESET}",
            opcoes,
            arte_ascii=arte_completa,
        )

        if has_save:
            if escolha_idx == 0:
                return "2"
            if escolha_idx == 1:
                return "1"
            if escolha_idx == 2:
                return "3"
        else:
            if escolha_idx == 0:
                return "1"
            if escolha_idx == 1:
                return "3"

    @staticmethod
    def show_save_notification(save_info: dict) -> None:
        """Exibe notificação de save com informações do progresso."""

        CLI._limpar_tela()
        print(f"\n{Color.GREEN}{'=' * 60}{Color.RESET}")
        print(f"{Color.GREEN}{'JOGO SALVO COM SUCESSO':^60}{Color.RESET}")
        print(f"{Color.GREEN}{'=' * 60}{Color.RESET}")

        print(
            f"\n{Color.WHITE}Progresso: {Color.CYAN}{save_info['progresso']}{Color.RESET}"
        )
        print(
            f"{Color.WHITE}Salvo em: {Color.GRAY}{save_info['save_date'][:19].replace('T', ' ')}{Color.RESET}"
        )

        print(
            f"\n{Color.YELLOW}[Pressione ENTER para continuar]{Color.RESET}".center(60)
        )
        CLI._clear_keyboard_buffer()
        CLI._ler_tecla()

    @staticmethod
    def confirm_overwrite_save() -> bool:
        """
        Alerta o jogador que já existe um save e pergunta se ele deseja sobrescrever.
        Retorna True se ele aceitar apagar o save, False se ele desistir.
        """
        opcoes = [
            f"{Color.DARK_RED}Sim, apagar meu progresso e recomeçar{Color.RESET}",
            f"{Color.GREEN}Não, manter meu jogo salvo{Color.RESET}",
        ]

        idx = CLI._mostrar_menu_interativo(
            titulo=f"{Color.RED}AVISO CRÍTICO{Color.RESET}: Você já possui um {Color.GREEN}jogo salvo!{Color.RESET}\nIniciar uma nova jornada {Color.RED}apagará{Color.RESET} seu progresso atual para sempre.{Color.RESET}",
            opcoes=opcoes,
        )

        return idx == 0

    @staticmethod
    def ask_hero_info() -> tuple[str, str]:
        """Guia o jogador na criação do personagem com imersão e arte."""
        import time

        CLI._limpar_tela()
        print(f"{Color.CYAN}=" * 60)
        print(f"{' O DESPERTAR ':^60}")
        print("=" * 60 + f"{Color.RESET}\n")

        print(
            f"{Color.MAGENTA}Uma voz antiga e cansada ecoa na escuridão da sua mente...\n{Color.RESET}"
        )
        time.sleep(1)

        name = ""
        while not name:
            name = (
                input(
                    f"{Color.MAGENTA}— Diga-me, alma errante... qual é o seu nome? \n> {Color.RESET}"
                )
                .strip()
                .title()
            )
            if not name:
                print(
                    f"{Color.YELLOW}— Não tenha medo. Fale seu nome...\n{Color.RESET}"
                )

        arte_classes = f"""
      {Color.RED}[ GUERREIRO ]{Color.RESET}          {Color.GREEN}[ ARQUEIRO ]{Color.RESET}            {Color.BLUE}[ MAGO ]{Color.RESET}

        {Color.YELLOW}o{Color.BROWN}=={Color.YELLOW}}}{Color.WHITE}=====>{Color.RESET}             {Color.BROWN}>>{Color.WHITE}---{Color.BROWN}>{Color.RESET}                   S2

       {Color.RED}Vida:{Color.RESET}  150            Vida:  100             Vida:   80
       Ataque: 30            Ataque: 35             {Color.BLUE}Ataque:{Color.RESET} 50
       Veloc:  10            {Color.GREEN}Veloc:{Color.RESET}  25             Veloc:  15
        """

        opcoes_classe = [
            "Guerreiro (Especialista em combate corpo a corpo e escudos)",
            "Arqueiro  (Rápido, letal e ataca à distância)",
            "Mago      (Especialista em magias e poder explosivo)",
        ]

        escolha_idx = CLI._mostrar_menu_interativo(
            f"{Color.CYAN}Saudações, {Color.YELLOW}{name}{Color.CYAN}... Qual caminho você trilhou?{Color.RESET}",
            opcoes_classe,
            arte_ascii=arte_classes,
        )

        class_choice = str(escolha_idx + 1)

        return name, class_choice

    @staticmethod
    def show_game_over() -> str:
        """Exibe a tela de derrota de forma interativa."""

        arte_game_over = f"""{Color.DARK_RED}
    ██████   ███████ ███    ███ ███████     ███████ ██    ██ ███████ ██████
    ██       ██   ██ ████  ████ ██          ██   ██  ██  ██  ██      ██   ██
    ██   ███ ███████ ██ ████ ██ █████       ██   ██   █  █   █████   ██████
    ██    ██ ██   ██ ██  ██  ██ ██          ██   ██    ██    ██      ██   ██
    ██████   ██   ██ ██      ██ ███████     ███████    ██    ███████ ██   ██
        {Color.RESET}"""

        narrativa = (
            f"\n{Color.GRAY}Seu corpo cai ao chão frio da masmorra...\n"
            f"As sombras se aproximam enquanto sua visão escurece.\n"
            f"\nA princesa continua aguardando por um herói...{Color.RESET}\n"
        )

        opcoes = [
            "Tentar Novamente",
            "Voltar ao Menu Principal",
        ]

        escolha_idx = CLI._mostrar_menu_interativo(
            f"{Color.RED}VOCÊ FOI DERROTADO...{Color.RESET}",
            opcoes,
            arte_ascii=arte_game_over + narrativa,
        )

        return "1" if escolha_idx == 0 else "2"

    @staticmethod
    def _imprimir_lento(text: str, delay: float = 0.05) -> None:
        """Gera o efeito de máquina de escrever (RPG clássico)."""
        import time
        import os

        jump = False

        if os.name == "nt":
            import msvcrt

            for char in text:
                sys.stdout.write(char)
                sys.stdout.flush()

                if not jump:
                    if msvcrt.kbhit():
                        key = msvcrt.getch()
                        if key in [b"\r", b"\n"]:
                            jump = True
                    else:
                        time.sleep(delay)
        else:
            import select
            import termios

            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                new_settings = termios.tcgetattr(fd)
                new_settings[3] = new_settings[3] & ~termios.ECHO & ~termios.ICANON
                termios.tcsetattr(fd, termios.TCSADRAIN, new_settings)

                for char in text:
                    sys.stdout.write(char)
                    sys.stdout.flush()

                    if not jump:
                        i, _, _ = select.select([sys.stdin], [], [], delay)
                        if i:
                            ch = sys.stdin.read(1)
                            if ch in ["\n", "\r"]:
                                jump = True
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        print()

    @staticmethod
    def show_victory(hero_name: str) -> None:
        """Exibe o final narrativo e melancólico do jogo, seguido pelos créditos."""
        import time

        arte_vela = r"""
               (
              ) )
             ( (
              |
           .--|--.
          /       \
         |_________|
        """

        def _tocar_cena(linhas: list[tuple[str, float]]) -> None:
            CLI._limpar_tela()
            print("=" * 60)
            print(f"{Color.CYAN}{' A ÚLTIMA SALA ':^60}{Color.RESET}")
            print("=" * 60)

            print(f"{Color.YELLOW}{arte_vela}{Color.RESET}")

            print(
                f"{Color.MAGENTA}[Aperte ENTER durante o texto para avançar rápido]{Color.RESET}\n"
            )

            for texto, atraso in linhas:
                CLI._imprimir_lento(texto, atraso)

            CLI._clear_keyboard_buffer()

            print(
                "\n"
                + f"{Color.CYAN}[Pressione ENTER para continuar]{Color.RESET}".center(
                    60 + len(Color.CYAN) + len(Color.RESET)
                )
            )
            CLI._ler_tecla()

        _tocar_cena(
            [
                (
                    "Narrador: O Herói entra na sala arrastando a perna esquerda. O cheiro de poeira antiga empesteia o ar.",
                    0.04,
                ),
                (
                    "Narrador: A princesa está encostada na parede, imóvel. A cabeça caída para o lado.",
                    0.05,
                ),
                (
                    f"{hero_name}: (Ofegante) Eu... eu finalmente cheguei. A porta de ferro... quase acabou comigo.",
                    0.05,
                ),
            ]
        )

        _tocar_cena(
            [
                (
                    "Narrador: Ele se deixa cair de joelhos, exausto. A arma retumbou ao bater no chão de pedra.",
                    0.04,
                ),
                (
                    f"{hero_name}: Eu perdi minha bota na armadilha do segundo andar. Imagina... o grande herói chegando descalço.",
                    0.06,
                ),
                (
                    f"{hero_name}: Mas eu precisava chegar. Eu precisava ver se você...",
                    0.05,
                ),
                (
                    "Narrador: Ele estende a mão trêmula, com medo de tocá-la. O coração bate na garganta.",
                    0.05,
                ),
            ]
        )

        _tocar_cena(
            [
                (
                    "Princesa: (Com a voz fraca, mas em tom de repreensão) Você perdeu a bota de couro que eu te dei?",
                    0.05,
                ),
                (
                    "Narrador: O herói congela. Ela abre lentamente um dos olhos, respirando fundo.",
                    0.04,
                ),
                (
                    f"{hero_name}: Você... você tá viva! Eu achei que...",
                    0.04,
                ),
                (
                    "Princesa: Acha que eu ia deixar um lorde das trevas me matar antes de eu te cobrar o dinheiro daquela bota?",
                    0.06,
                ),
            ]
        )

        _tocar_cena(
            [
                (
                    f"{hero_name}: (Rindo, limpando o rosto sujo de terra) Pode cobrar. Com juros.",
                    0.05,
                ),
                (
                    f"{hero_name}: Eu só... eu não ia conseguir voltar sem você. Você sabe disso, né?",
                    0.05,
                ),
                (
                    "Princesa: Eu sei. Você é um desastre sem mim.",
                    0.05,
                ),
            ]
        )

        CLI._limpar_tela()
        print("=" * 60)
        print(f"{' A ÚLTIMA SALA ':^60}")
        print("=" * 60)
        print(arte_vela)
        print("\n\n")
        CLI._imprimir_lento(
            "Narrador: Ele segura a mão dela. Dessa vez, o aperto é devolvido com firmeza. O frio da masmorra não importa mais.\n",
            0.05,
        )
        time.sleep(3)

        CLI._limpar_tela()
        time.sleep(1)

        print("\n\n\n")
        print(" F I M ".center(60))
        time.sleep(3)

        CLI._limpar_tela()

        print(f"{Color.CYAN}=" * 60 + Color.RESET)
        credits_text = " CRÉDITOS - DUNGEONPY "
        print(f"{Color.YELLOW}{credits_text:^60}{Color.RESET}")
        print(f"{Color.CYAN}=" * 60 + f"{Color.RESET}\n")

        time.sleep(0.5)
        print(f"{Color.GREEN}{'DESENVOLVIDO POR:'.center(60)}{Color.RESET}")
        print(f"{Color.ORANGE}{'Alan Mendes Vieira'.center(60)}{Color.RESET}")
        print(f"{Color.CYAN}{'Cicero Jesus Da Silva Gomes'.center(60)}{Color.RESET}")
        print(f"{Color.RED}{'Leôncio Ferreira Flores Neto'.center(60)}{Color.RESET}")
        print(f"{Color.BROWN}{'Paulo Gabriel Leite Landim'.center(60)}{Color.RESET}")
        print(f"{Color.DARK_RED}{'Salomão Rodrigues Silva'.center(60)}{Color.RESET}")

        time.sleep(0.5)
        print(
            "\n\n"
            + f"{Color.CYAN}{'UNIVERSIDADE FEDERAL DO CARIRI (UFCA)'.center(60)}{Color.RESET}"
        )
        print(
            f"{Color.GRAY}{'Disciplina de Programação Orientada a Objetos'.center(60)}{Color.RESET}"
        )
        print(
            f"{Color.YELLOW}{'Professor(a): [Jayr Alencar Pereira]'.center(60)}{Color.RESET}"
        )

        print("\n" + f"{Color.CYAN}=" * 60 + Color.RESET)
        texto_obrigado = " OBRIGADO POR JOGAR DUNGEONPY! "
        print(f"{Color.GREEN}{texto_obrigado.center(60, '*')}{Color.RESET}")
        print(f"{Color.CYAN}=" * 60 + Color.RESET)

        msg_voltar = "[Pressione ENTER para voltar ao Menu Principal]"
        print("\n" + f"{Color.GRAY}{msg_voltar.center(60)}{Color.RESET}")

        CLI._clear_keyboard_buffer()
        CLI._ler_tecla()

    @staticmethod
    def show_battle_reward(
        monster_name: str,
        dropped_items: list[str],
        missed_items: list[str] = None,
        leveled_up: bool = False,
    ) -> None:
        """Exibe a tela de vitória após derrotar um monstro."""
        CLI._limpar_tela()

        print(f"{Color.GREEN}=" * 60)
        print(f"{Color.YELLOW}{'VITÓRIA EM BATALHA!':^60}{Color.RESET}")
        print(f"{Color.GREEN}=" * 60 + f"{Color.RESET}")

        print(
            f"\nO terrível {Color.RED}{monster_name}{Color.RESET} foi derrotado!\n".center(
                60
            )
        )

        if leveled_up:
            msg_lvl = " LEVEL UP! VOCÊ FICOU MAIS FORTE! "
            lvl_spaces = " " * ((60 - len(msg_lvl)) // 2)
            print(
                f"{lvl_spaces}{Color.CYAN} {Color.YELLOW}LEVEL UP! {Color.BLUE}VOCÊ FICOU MAIS FORTE! {Color.RESET}\n"
            )

        print(f" {Color.YELLOW}{'RECOMPENSAS'.center(60, '-')}{Color.RESET}")

        if dropped_items:
            print(f"  {Color.GREEN}• Itens recolhidos:{Color.RESET}")
            for item in dropped_items:
                print(
                    f"      {Color.GREEN}+ {Color.RESET} {Color.CYAN}{item}{Color.RESET}"
                )
        elif not dropped_items and not missed_items:
            print(
                f"  {Color.GREEN}• Itens: {Color.GRAY}Os bolsos do monstro estavam vazios.{Color.RESET}"
            )

        if missed_items:
            print(
                f"\n  {Color.RED} AVISO: SUA MOCHILA ESTÁ MUITO PESADA, BURRÃO HEIN! {Color.RESET}"
            )
            print(
                f"  {Color.GRAY}Você precisou deixar os seguintes itens para trás:{Color.RESET}"
            )
            for item in missed_items:
                print(
                    f"      {Color.DARK_RED}- {Color.RESET} {Color.GRAY}{item}. {Color.RESET}"
                )

        print(f"{Color.GRAY}-" * 60 + f"{Color.RESET}")

        CLI._clear_keyboard_buffer()

        msg_continue = "[Pressione ENTER para continuar a exploração]"
        espacos_cont = " " * ((60 - len(msg_continue)) // 2)
        print(f"\n{espacos_cont}{Color.CYAN}{msg_continue}{Color.RESET}")

        CLI._ler_tecla()

    @staticmethod
    def show_hero_status(status_dict: dict) -> None:
        """Imprime a 'Ficha de Personagem' completa."""
        CLI._limpar_tela()

        barra_hp = CLI._gerar_barra_progresso(
            status_dict["current_life"], status_dict["max_life"], tamanho=15
        )

        nome = status_dict["name"]
        ataque = status_dict["attack"]
        velocidade = status_dict["speed"]
        elemento = status_dict["element"]
        arma = status_dict["equipped_weapon"]

        print("=" * 60)
        print(f"{'FICHA DE PERSONAGEM':^60}")
        print("=" * 60)

        print(f"{'Nome:':^30} {nome:^30}")
        print("-" * 60)

        print(f"      Vida: {barra_hp}")
        print("-" * 60)

        print(f"{'Ataque:':^30} {ataque:^30}")
        print(f"{'Velocidade:':^30} {velocidade:^30}")
        print("-" * 60)

        print(f"{'Elemento:':^30} {elemento:^30}")
        print(f"{'Arma Equipada:':^30} {arma:^30}")
        print("=" * 60)
        print("[Pressione ENTER para voltar]".center(60))
        print("=" * 60)

        CLI._ler_tecla()

    @staticmethod
    def print_room_description(description: str) -> None:
        """Imprime o texto da sala formatado."""
        CLI._limpar_tela()

        CLI._imprimir_lento(description)
        time.sleep(0.5)
        print("\nPressione ENTER para continuar...")
        CLI._ler_tecla()

    @staticmethod
    def show_exploration_menu() -> str:
        """Menu de exploração entre salas."""
        opcoes = [
            f"{Color.GREEN}Avançar para próxima sala{Color.RESET}",
            f"{Color.BROWN}Ver Inventário{Color.RESET}",
            f"{Color.BLUE}Salvar Jogo{Color.RESET}",
            f"{Color.GRAY}Ficha de personagem (em breve){Color.RESET}",
        ]

        while True:
            escolha_idx = CLI._mostrar_menu_interativo(
                titulo=f"{Color.CYAN}O QUE DESEJA FAZER?{Color.RESET}",
                opcoes=opcoes,
            )

            if escolha_idx == 0:
                return "1"

            if escolha_idx == 1:
                return "2"

            if escolha_idx == 2:
                return "3"

            CLI._limpar_tela()
            print(f"{Color.GRAY}=" * 60 + Color.RESET)
            print(f"{Color.YELLOW}{'FICHA DE PERSONAGEM':^60}{Color.RESET}")
            print(f"{Color.GRAY}=" * 60 + Color.RESET)
            print(
                f"\n{Color.GRAY}Essa opção ainda está em desenvolvimento.\n"
                f"Ela ficará disponível em uma próxima atualização!{Color.RESET}\n"
            )
            print(f"{Color.CYAN}[Pressione ENTER para voltar]{Color.RESET}".center(60))
            CLI._clear_keyboard_buffer()
            CLI._ler_tecla()

    @staticmethod
    def _gerar_barra_progresso(
        atual: int,
        maximo: int,
        tamanho: int = 10,
        simbolo_cheio: str = "█",
        simbolo_vazio: str = " ",
    ) -> str:
        """Cria uma barra visual. Ex: [██████    ] 6/10"""
        if maximo <= 0:
            return f"[{simbolo_vazio * tamanho}] 0/0"

        preenchidos = int((atual / maximo) * tamanho)
        vazios = tamanho - preenchidos
        return (
            f"[{simbolo_cheio * preenchidos}{simbolo_vazio * vazios}] {atual}/{maximo}"
        )

    @staticmethod
    def get_combat_choice(
        acoes_do_heroi: dict,
        nome_heroi: str,
        nivel_heroi: int,
        hp_atual: int,
        hp_max: int,
        arte_monstro: str,
        nome_monstro: str,
    ) -> str:
        """Desenha a tela de batalha e pede a ação do jogador."""

        barra_hp = CLI._gerar_barra_progresso(hp_atual, hp_max)

        cor_hp = Color.GREEN if (hp_atual / hp_max) > 0.5 else Color.RED

        cena_batalha = f"""
{arte_monstro}
{nome_monstro.center(60)}

{Color.WHITE}============================================================{Color.RESET}
 {Color.CYAN}Herói: {Color.YELLOW}{nome_heroi} {Color.CYAN}(Nv {nivel_heroi}){Color.RESET}
 {Color.ORANGE}HP: {cor_hp}{barra_hp}{Color.RESET}
{Color.WHITE}============================================================{Color.RESET}
"""

        opcoes_menu_principal = [
            f"{Color.RED}Atacar{Color.RESET}",
            f"{Color.BROWN}Inventário{Color.RESET}",
            f"{Color.GRAY}Fugir (Você não pode fugir ainda!){Color.RESET}",
        ]

        while True:
            escolha_idx = CLI._mostrar_menu_interativo(
                f"{Color.YELLOW}O QUE VOCÊ VAI FAZER?{Color.RESET}",
                opcoes_menu_principal,
                arte_ascii=cena_batalha,
            )

            if escolha_idx == 0:
                textos_ataques = [
                    info["description"] for info in acoes_do_heroi.values()
                ]
                textos_ataques.append("Voltar")

                escolha_ataque_idx = CLI._mostrar_menu_interativo(
                    f"{Color.RED}ESCOLHA SEU GOLPE:{Color.RESET}",
                    textos_ataques,
                    arte_ascii=cena_batalha,
                )

                if escolha_ataque_idx == len(textos_ataques) - 1:
                    continue

                chaves_originais = list(acoes_do_heroi.keys())
                chave_escolhida = chaves_originais[escolha_ataque_idx]

                return chave_escolhida

            elif escolha_idx == 1:
                return "inventario"

            elif escolha_idx == 2:
                CLI._limpar_tela()
                print(cena_batalha)
                print(
                    f"{Color.GREEN}================================================================={Color.RESET}"
                )
                print(
                    f"{Color.CYAN}EU NÃO POSSO FUGIR ANTES DE RESGATAR A {Color.PURPLE}PRINCESAAAAA{Color.RESET}..."
                )
                print(
                    "Eu preciso lutar (ou talvez os devs só não tenham feito essa opção)"
                )
                print(
                    f"{Color.GREEN}=================================================================={Color.RESET}"
                )
                print("(Aperte ENTER para voltar)")
                input()
                continue

    @staticmethod
    def show_inventory(inventory_summary: dict) -> tuple[str, str] | None:
        """Exibe o inventário de forma interativa."""

        items = inventory_summary["items"]

        if not items:
            CLI._limpar_tela()
            print("\n" + f"{Color.BROWN}=" * 60 + Color.RESET)
            print(f"{Color.YELLOW}{'INVENTÁRIO':^60}{Color.RESET}")
            print(f"{Color.BROWN}=" * 60 + Color.RESET)

            empty_msg = "Sua mochila está vazia."
            empty_space = " " * ((60 - len(empty_msg)) // 2)
            print(f"\n{empty_space}{Color.GRAY}{empty_msg}{Color.RESET}")

            CLI._clear_keyboard_buffer()
            msg_voltar = "[Pressione ENTER para voltar...]"
            espacos_voltar = " " * ((60 - len(msg_voltar)) // 2)
            print(f"\n{espacos_voltar}{Color.CYAN}{msg_voltar}{Color.RESET}")
            CLI._ler_tecla()
            return None

        actual_weight = inventory_summary["current_weight"]
        max_weight = inventory_summary["capacity"]
        weight_color = Color.RED if (actual_weight / max_weight) > 0.8 else Color.GREEN

        header = (
            f"{Color.BROWN}Peso: {Color.RESET}"
            f"{weight_color}{actual_weight:.1f}{Color.RESET}/"
            f"{Color.GREEN}{max_weight:.1f}{Color.RESET}"
        )

        action_map = {
            0: "usar",
            1: "ver_descricao",
            2: "descartar",
        }

        action_options = [
            f"{Color.GREEN}Usar / Equipar{Color.RESET}",
            f"{Color.CYAN}Ver descrição{Color.RESET}",
            f"{Color.RED}Descartar{Color.RESET}",
            f"{Color.GRAY}Voltar ao inventário{Color.RESET}",
        ]

        VOLTAR_INVENTARIO = len(action_options) - 1

        while True:
            item_options = [
                f"{Color.YELLOW}{item['name']}{Color.RESET} {Color.GRAY}(peso: {item['weight']}){Color.RESET}"
                for item in items
            ]
            item_options.append(f"{Color.GRAY}Voltar{Color.RESET}")

            VOLTAR_MENU = len(item_options) - 1

            selected_index = CLI._mostrar_menu_interativo(
                titulo=f"{Color.BROWN}INVENTÁRIO{Color.RESET}\n{header}",
                opcoes=item_options,
            )

            if selected_index == VOLTAR_MENU:
                return None

            selected_item = items[selected_index]
            item_name = selected_item["name"]

            while True:
                action_index = CLI._mostrar_menu_interativo(
                    titulo=f"{Color.BROWN}AÇÕES  —  {Color.YELLOW}{item_name}{Color.RESET}",
                    opcoes=action_options,
                )
                if action_index == 1:
                    CLI._limpar_tela()
                    item_description = selected_item.get(
                        "description", "Fé nas malucas, pode dar bom ou ruim."
                    )

                    print(f"{Color.BROWN}=" * 60 + Color.RESET)
                    print(f"{Color.YELLOW}{item_name:^60}{Color.RESET}")
                    print(f"{Color.BROWN}=" * 60 + Color.RESET)

                    print(f"\n{Color.CYAN}{item_description.center(60)}{Color.RESET}\n")

                    CLI._clear_keyboard_buffer()
                    input(
                        f"{Color.GRAY}[Pressione ENTER para voltar às ações]{Color.RESET}".center(
                            60 + len(Color.GRAY) + len(Color.RESET)
                        )
                    )

                    continue

                if action_index == VOLTAR_INVENTARIO:
                    break

                return (item_name, action_map[action_index])

    @staticmethod
    def display_turn_log(
        turn_number: int,
        hero_name: str,
        hero_hp: int,
        hero_max_hp: int,
        monster_name: str,
        monster_hp: int,
        monster_max_hp: int,
        actions: list[str],
        status: dict[str, str],
        extra_status: dict[str, str] = None,  # ← NOVO: ammo, mana, etc.
    ) -> None:
        """
        Exibe o resumo visual de um turno de combate.

        extra_status: dicionário opcional com recursos especiais do herói.
                      Chaves reconhecidas: 'ammo' (Arqueiro), 'mana' (Mago).
                      Ex: {"ammo": "7/10"} ou {"mana": "30/100"}
        """

        print("\n" + f"{Color.YELLOW}" + "=" * 60)
        turn_text = f"TURNO {turn_number}"
        print(f"{Color.YELLOW}{turn_text:^60}{Color.RESET}")
        print(f"{Color.YELLOW}=" * 60 + Color.RESET)

        raw_subtitle = f"{hero_name}: {hero_hp}/{hero_max_hp} HP   |   {monster_name}: {monster_hp}/{monster_max_hp} HP"
        espaces = " " * ((60 - len(raw_subtitle)) // 2)

        cor_hp_heroi = Color.GREEN if (hero_hp / hero_max_hp) > 0.5 else Color.RED
        cor_hp_monstro = (
            Color.DARK_RED if (monster_hp / monster_max_hp) > 0.5 else Color.RED
        )

        str_heroi = f"{Color.CYAN}{hero_name}{Color.RESET}: {cor_hp_heroi}{hero_hp}/{hero_max_hp} HP{Color.RESET}"
        str_monstro = f"{Color.RED}{monster_name}{Color.RESET}: {cor_hp_monstro}{monster_hp}/{monster_max_hp} HP{Color.RESET}"

        print(f"{espaces}{str_heroi}   {Color.GRAY}|{Color.RESET}   {str_monstro}")

        # --- Linha de recursos especiais (Arqueiro: flechas / Mago: mana) ---
        if extra_status:
            resource_parts = []
            if "ammo" in extra_status:
                resource_parts.append(
                    f"{Color.BROWN}🏹 Flechas:{Color.RESET} {Color.YELLOW}{extra_status['ammo']}{Color.RESET}"
                )
            if "mana" in extra_status:
                resource_parts.append(
                    f"{Color.BLUE}✨ Mana:{Color.RESET} {Color.CYAN}{extra_status['mana']}{Color.RESET}"
                )
            if resource_parts:
                print(f"{espaces}{'   '.join(resource_parts)}")

        print(f"{Color.GRAY}-" * 60 + Color.RESET)

        # Status
        if status:
            print(f"\n{Color.MAGENTA}Status:{Color.RESET}")
            for entity_name, state in status.items():
                entity_color = Color.CYAN if entity_name == hero_name else Color.RED
                print(
                    f"  {entity_color}{entity_name}{Color.RESET} {Color.GRAY}→ {Color.RESET} {Color.YELLOW}{state}{Color.RESET}"
                )

        # Ações
        if actions:
            print(f"\n{Color.CYAN}Ações:{Color.RESET}")
            for action in actions:
                colored_action = action.replace(
                    hero_name, f"{Color.CYAN}{hero_name}{Color.GRAY}"
                )
                colored_action = colored_action.replace(
                    monster_name, f"{Color.RED}{monster_name}{Color.GRAY}"
                )
                print(f"  {Color.GRAY}• {colored_action}{Color.RESET}")

        CLI._clear_keyboard_buffer()
        msg_continue = "[Pressione Enter para o próximo turno]"
        cont_spaces = " " * ((60 - len(msg_continue)) // 2)
        print(f"\n{cont_spaces}{Color.CYAN}{msg_continue}{Color.RESET}")
        CLI._ler_tecla()

    @staticmethod
    def display_message(message: str) -> None:
        """Exibe mensagens rápidas do sistema e pausa a tela."""
        print("\n" + f"{Color.BROWN}=" * 60 + Color.RESET)

        print(f"\n{Color.CYAN}{message.center(60)}{Color.RESET}\n")

        print(f"{Color.BROWN}=" * 60 + Color.RESET)

        CLI._clear_keyboard_buffer()
        input(
            f"\n{Color.GRAY}[Pressione ENTER para continuar]{Color.RESET}".center(
                60 + len(Color.GRAY) + len(Color.RESET)
            )
        )


# Area for visual tests with datas pre-setting

if __name__ == "__main__":
    acao = CLI.show_main_menu(True)
    if acao == "1":
        CLI.confirm_overwrite_save()
        CLI.show_exploration_menu()

        CLI.print_room_description(
            description="Um enorme castelo com muitas torres e janelas iluminadas, brilhando no alto da montanha."
        )

        CLI.show_hero_status(
            {
                "name": "Alan",
                "current_life": 10,
                "max_life": 10,
                "attack": 10,
                "speed": 10,
                "element": 10,
                "equipped_weapon": "Matadora",
            }
        )
        nome_heroi, classe_heroi = CLI.ask_hero_info()

        CLI._limpar_tela()
        print(
            f"\n{Color.GREEN}SUCESSO! Herói criado: {nome_heroi} (Classe ID: {classe_heroi}){Color.RESET}"
        )
        print(
            f"{Color.GRAY}Você adentra as profundezas da masmorra... [Pressione ENTER]{Color.RESET}"
        )
        CLI._ler_tecla()

        mochila_falsa = {
            "current_weight": 3.5,
            "capacity": 15.0,
            "items": [
                {"name": "Poção de Vida Menor", "weight": 0.5},
                {"name": "Espada Longa Enferrujada", "weight": 2.0},
                {"name": "Amuleto do Rato", "weight": 1.0},
            ],
        }
        escolha_inventario = CLI.show_inventory(mochila_falsa)
        CLI._limpar_tela()

        CLI.display_turn_log(
            turn_number=1,
            hero_name=nome_heroi,
            hero_hp=25,
            hero_max_hp=50,
            monster_name="Dragão de Fogo Ancião",
            monster_hp=70,
            monster_max_hp=150,
            actions=[
                "O Dragão de Fogo Ancião rugiu e cuspiu chamas!",
                f"{nome_heroi} tentou desviar, mas recebeu 15 de dano!",
            ],
            status={
                nome_heroi: "Queimando (perde 2 HP por turno)",
                "Dragão de Fogo Ancião": "Fúria (+20% de dano)",
            },
            extra_status={"ammo": "7/10"},  # Exemplo com Arqueiro
        )

        acoes_falsas = {
            "1": {"description": "Ataque Básico"},
            "2": {"description": "Golpe Pesado"},
            "3": {"description": "Magia Especial"},
        }

        arte_dragao = r"""
             \||/
             |  @___oo
   /\  /\   / (__,,,,|
  ) /^\) ^\/ _)
  )   /^\/   _)
  )   _ /  / _)
  /\  )/\/ ||
        """

        escolha_combate = CLI.get_combat_choice(
            acoes_do_heroi=acoes_falsas,
            nome_heroi=nome_heroi,
            nivel_heroi=5,
            hp_atual=25,
            hp_max=50,
            arte_monstro=arte_dragao,
            nome_monstro="Dragão de Fogo Ancião",
        )

        CLI.show_battle_reward(
            monster_name="Dragão de Fogo Ancião",
            dropped_items=["Escama de Fogo", "Coração de Dragão"],
            missed_items=["Espada Giga Quebrada"],
            leveled_up=True,
        )

        CLI._limpar_tela()
        print(
            f"{Color.GRAY}Simulando a tela de DERROTA... [Pressione ENTER]{Color.RESET}"
        )
        CLI._ler_tecla()
        CLI.show_game_over()

        CLI._limpar_tela()
        print(
            f"{Color.GRAY}Simulando a tela de VITÓRIA FINAL... [Pressione ENTER]{Color.RESET}"
        )
        CLI._ler_tecla()
        CLI.show_victory(nome_heroi)

        CLI._limpar_tela()
        print(f"{Color.GREEN}=" * 60 + Color.RESET)
        print(f"{Color.YELLOW}{' SIMULAÇÃO DE INTERFACE CONCLUÍDA ':^60}{Color.RESET}")
        print(f"{Color.GREEN}=" * 60 + f"{Color.RESET}\n")

        if escolha_inventario:
            print(
                f" {Color.GRAY}• Inventário testado (Ação escolhida: {escolha_inventario}){Color.RESET}"
            )
        else:
            print(
                f" {Color.GRAY}• Inventário testado (Nenhuma ação, apenas olhou a mochila){Color.RESET}"
            )

        print(
            f" {Color.GRAY}• Combate testado (Ação escolhida: {escolha_combate}){Color.RESET}"
        )
        print(
            f"\n{Color.CYAN}Tudo rodando 100%! Pode integrar com o GameManager.{Color.RESET}".center(
                60 + len(Color.CYAN) + len(Color.RESET)
            )
        )
        print("\n")

    else:
        CLI._limpar_tela()
        print(f"{Color.GRAY}Saindo do jogo... Até a próxima!{Color.RESET}")
