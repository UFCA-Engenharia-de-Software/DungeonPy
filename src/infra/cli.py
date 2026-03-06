import os
import sys
import time
import textwrap


class Color:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    RESET = "\033[0m"

    # --- Cores Escuras / Clássicas ---
    DARK_RED = "\033[31m"
    DARK_GREEN = "\033[32m"
    DARK_BLUE = "\033[34m"

    # --- Cores Neutras ---
    WHITE = "\033[97m"
    GRAY = "\033[90m"  # Ótimo para textos de sistema ou dicas
    BLACK = "\033[30m"

    # --- Cores Especiais (Tabela de 256 cores) ---
    BROWN = "\033[38;5;130m"  # Um marrom real, perfeito para portas, baús e mochilas
    ORANGE = "\033[38;5;208m"  # Laranja vibrante (fogo, dano crítico)
    PURPLE = "\033[38;5;93m"  # Um roxo mais sombrio e fechado que o Magenta


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

            # ---------------------------------------------------------
            # Exatamente a mesma lógica do teste que funcionou!
            # ---------------------------------------------------------
            acao = CLI._ler_tecla()

            if acao == "UP":
                indice_atual = (indice_atual - 1) % len(opcoes)
            elif acao == "DOWN":
                indice_atual = (indice_atual + 1) % len(opcoes)
            elif acao == "ENTER":
                return indice_atual

    @staticmethod
    def show_main_menu() -> str:
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

        # Adicionando vida ao menu: Subtítulo, decoração e versão
        subtitle = "  Uma jornada de sombras, escolhas e perdas ".center(60)
        subtitle_colored = f"{Color.CYAN}{subtitle}{Color.RESET}"
        version = "v1.0.0".rjust(58)  # Fica alinhado à direita
        version_colored = f"{Color.YELLOW}{version}{Color.RESET}"

        arte_completa = f"{art_colored}\n{subtitle_colored}\n\n{version_colored}\n"

        opcoes = ["Iniciar Nova Jornada", "Sair do Jogo"]

        escolha_idx = CLI._mostrar_menu_interativo(
            "M E N U   P R I N C I P A L", opcoes, arte_ascii=arte_completa
        )

        return "1" if escolha_idx == 0 else "2"

    @staticmethod
    def ask_hero_info() -> tuple[str, str]:
        """Guia o jogador na criação do personagem."""

        """Guia o jogador na criação do personagem com imersão e arte."""
        import time

        CLI._limpar_tela()
        print(f"{Color.CYAN}=" * 60)
        print(f"{' O DESPERTAR ':^60}")
        print("=" * 60 + f"{Color.RESET}\n")

        # Um pequeno toque de RPG de mesa antes de pedir o nome
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

        # Arte das 3 armas lado a lado (Pure ASCII para não bugar)
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

        # Passamos a arte_classes para o nosso motor de menu interativo
        escolha_idx = CLI._mostrar_menu_interativo(
            f"{Color.CYAN}Saudações, {Color.YELLOW}{name}{Color.CYAN}... Qual caminho você trilhou?{Color.RESET}",
            opcoes_classe,
            arte_ascii=arte_classes,
        )

        # Mapeia o índice (0, 1, 2) para a string correta ("1", "2", "3")
        class_choice = str(escolha_idx + 1)

        return name, class_choice

    # Menus simples
    @staticmethod
    def show_game_over() -> str:
        """
        Exibe a tela de derrota de forma interativa.

        Retorna:
            "1" -> Tentar novamente
            "2" -> Voltar ao menu principal
        """

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
        """
        Gera o efeito de máquina de escrever (RPG clássico).
        Se o jogador apertar ENTER, pula o efeito e imprime a linha inteira.
        Create the effect of typewriter
        If Player press ENTER, jump the effect and print the whole line
        """
        import sys
        import time
        import os

        jump = False

        if os.name == "nt":
            import msvcrt

            for char in text:
                sys.stdout.write(char)
                sys.stdout.flush()

                if not jump:
                    # Verifica se tem tecla na fila sem pausar o código
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
                # Desativa o ECHO (para não pular linha na tela) e ativa modo não-canônico
                new_settings = termios.tcgetattr(fd)
                new_settings[3] = new_settings[3] & ~termios.ECHO & ~termios.ICANON
                termios.tcsetattr(fd, termios.TCSADRAIN, new_settings)

                for char in text:
                    sys.stdout.write(char)
                    sys.stdout.flush()

                    if not jump:
                        # Espera por 'delay' segundos. Se tiver input, o select nos avisa!
                        i, _, _ = select.select([sys.stdin], [], [], delay)
                        if i:
                            ch = sys.stdin.read(1)
                            if ch in ["\n", "\r"]:
                                jump = True
            finally:
                # Devolve o terminal ao normal!
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        print()  # Quebra a linha no final da frase

    @staticmethod
    def show_victory(hero_name: str) -> None:
        """
        Exibe o final narrativo e melancólico do jogo, seguido pelos créditos.
        """
        import time

        # Âncora visual triste para a sala
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
            """Função interna para desenhar a tela limpa a cada cena."""
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

        # ==========================================
        # ROTEIRO DA CUTSCENE FINAL (Dividido em Atos)
        # ==========================================

        # Ato 1: A Chegada
        _tocar_cena(
            [
                (
                    "Narrador: O Herói adentra a uma pequena sala. Ao longe, ele avista a princesa.",
                    0.04,
                ),
                (
                    "Narrador: Seu corpo parecia estar intacto, mas o silêncio do lugar era ensurdecedor...",
                    0.06,
                ),
                (
                    f"{hero_name}: Eu... eu finalmente cheguei... depois de tanto tempo...",
                    0.05,
                ),
            ]
        )

        # Ato 2: A Descoberta
        _tocar_cena(
            [
                (
                    "Narrador: Ele se aproxima, tentando chamá-la de longe. Mas quanto mais perto chegava,",
                    0.04,
                ),
                (
                    "Narrador: mais o frio da sala o consumia. Ele se ajoelha próximo ao seu rosto.",
                    0.05,
                ),
                (
                    f"{hero_name}: Ei, princesa... eu sei que você está bem, não tá?",
                    0.06,
                ),
            ]
        )

        # Ato 3: O Desespero
        _tocar_cena(
            [
                (
                    "Narrador: Os olhos dela estavam fechados. O herói estava cansado demais para raciocinar.",
                    0.05,
                ),
                (f"{hero_name}: Ei, por favor, acorda... acorda, por favor.", 0.05),
                (f"{hero_name}: Eu não posso... não posso voltar sem você.", 0.07),
                (
                    "Narrador: O desespero tomou conta. Ele tocou sua mão, mas nada acontecia.",
                    0.06,
                ),
            ]
        )

        # Ato 4: As Memórias
        _tocar_cena(
            [
                (f"{hero_name}: Você não pode ter... por favor, não.", 0.06),
                (f"{hero_name}: Você é forte. É a mais forte que eu conheço.", 0.05),
                (
                    f"{hero_name}: Lembra de quando brincávamos? Você sempre foi a durona...",
                    0.05,
                ),
                (
                    f"{hero_name}: Sempre sabia o que me dizer quando eu estava mal.",
                    0.05,
                ),
            ]
        )

        # Ato 5: A Declaração
        _tocar_cena(
            [
                (
                    f"{hero_name}: Sempre ajudou todo mundo...até alguém como eu... não importa o que falassem,",
                    0.05,
                ),
                (
                    f"{hero_name}: ou o que diziam sobre mim. Você nunca deixou as pessoas tirarem de você o que você era,",
                    0.05,
                ),
                (
                    f"{hero_name}: não importa o quão difícil fosse, o quanto zombavam,",
                    0.05,
                ),
                (
                    f"{hero_name}: você nunca deixou de ajudar aos outros, de me ajudar.",
                    0.05,
                ),
            ]
        )

        # Ato 6: A Despedida
        _tocar_cena(
            [
                (f"{hero_name}: Eu deveria ter ficado mais tempo com você...", 0.07),
                (f"{hero_name}: Não deveria ter me afastado...", 0.07),
                (f"{hero_name}: Não deveria ter te deixado sozinha...", 0.08),
                (
                    f"{hero_name}: Talvez... a força que eu ganhei para chegar até aqui",
                    0.05,
                ),
                (f"{hero_name}: tenha vindo de você.", 0.06),
            ]
        )

        # Ato 7: O Fim (Única cena sem o ler_tecla no loop, tratado manualmente)
        CLI._limpar_tela()
        print("=" * 60)
        print(f"{' A ÚLTIMA SALA ':^60}")
        print("=" * 60)
        print(arte_vela)
        print("\n\n")
        CLI._imprimir_lento(
            f"{hero_name}: Então... por favor... não me deixe agora.", 0.1
        )
        time.sleep(3)  # Pausa longa dramática no escuro

        # ==========================================
        # TELA DE CRÉDITOS
        # ==========================================
        CLI._limpar_tela()
        time.sleep(1)

        print("\n\n\n")
        print(" F I M ".center(60))
        time.sleep(3)

        CLI._limpar_tela()

        # Aqui no futuro você pode dar o play na música triste!

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
        print(f"{Color.PURPLE}{'Salomão Rodrigues Silva'.center(60)}{Color.RESET}")

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

        # O prompt do jogador em uma cor neutra
        msg_voltar = "[Pressione ENTER para voltar ao Menu Principal]"
        print("\n" + f"{Color.GRAY}{msg_voltar.center(60)}{Color.RESET}")

        CLI._clear_keyboard_buffer()
        # Usamos o leitor multiplataforma para esperar a ação do jogador
        CLI._ler_tecla()

    @staticmethod
    def show_battle_reward(
        monster_name: str,
        dropped_items: list[str],
        missed_items: list[str] = None,
        leveled_up: bool = False,
    ) -> None:
        """
        O que faz: Exibe a tela de vitória após derrotar um monstro, mostrando os espólios (loot) e XP.

        O que recebe:
            - monster_name (str): O nome do monstro derrotado.
            - dropped_items (list[str]): Uma lista apenas com os NOMES dos itens (Ex: ["Poção de Cura", "Adaga"]).
            - leveled_up (bool): Passar True se o herói subiu de nível nessa luta.
        """
        CLI._limpar_tela()

        print(f"{Color.GREEN}=" * 60)
        print(f"{Color.YELLOW}{'VITÓRIA EM BATALHA!':^60}{Color.RESET}")
        print(f"{Color.GREEN}=" * 60 + f"{Color.RESET}")

        print(
            f"\nO terrível {Color.RED}{monster_name}{Color.RESET} foi derrotado!\n".center(
                60
            )
        )

        # Efeito visual caso o jogador tenha subido de nível
        if leveled_up:
            msg_lvl = " LEVEL UP! VOCÊ FICOU MAIS FORTE! "
            lvl_spaces = " " * ((60 - len(msg_lvl)) // 2)
            print(
                f"{lvl_spaces}{Color.CYAN} {Color.YELLOW}LEVEL UP! {Color.BLUE}VOCÊ FICOU MAIS FORTE! {Color.RESET}\n"
            )

        print(f" {Color.YELLOW}{'RECOMPENSAS'.center(60, '-')}{Color.RESET}")

        # Verifica se o monstro dropou algo ou não
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

        CLI._ler_tecla()  # Usamos aquele nosso leitor multiplataforma para pausar!

    @staticmethod
    def show_hero_status(status_dict: dict) -> None:
        """
        O que recebe: Um dicionário com todos os status atuais do herói.
        O que faz: Imprime a "Ficha de Personagem" completa e espera uma tecla para voltar.
        Mostra os status: "Nome, Vida atual em relação a máxima, ataque, velocidade, e arma atual equipada."
        """
        CLI._limpar_tela()

        # Criar barra de vida
        barra_hp = CLI._gerar_barra_progresso(
            status_dict["current_life"], status_dict["max_life"], tamanho=15
        )

        # Monta a ficha de personagem
        nome = status_dict["name"]
        ataque = status_dict["attack"]
        velocidade = status_dict["speed"]
        elemento = status_dict["element"]
        arma = status_dict["equipped_weapon"]

        print("=" * 60)
        print(f"{'FICHA DE PERSONAGEM':^60}")
        print("=" * 60)

        # Nome
        print(f"{'Nome:':^30} {nome:^30}")
        print("-" * 60)

        # Vida
        print(f"      Vida: {barra_hp}")
        print("-" * 60)

        # Ataque e Velocidade lado a lado
        print(f"{'Ataque:':^30} {ataque:^30}")
        print(f"{'Velocidade:':^30} {velocidade:^30}")
        print("-" * 60)

        # Elemento e Arma
        print(f"{'Elemento:':^30} {elemento:^30}")
        print(f"{'Arma Equipada:':^30} {arma:^30}")
        print("=" * 60)
        print("[Pressione ENTER para voltar]".center(60))
        print("=" * 60)

        CLI._ler_tecla()

    # Exploração e Inventário
    @staticmethod
    def print_room_description(description: str) -> None:
        """
        O que recebe: O texto da sala.
        O que faz: Imprime o texto formatado com quebra de linha inteligente
                   e uma borda visual para imersão.
        """
        CLI._limpar_tela()

        CLI._imprimir_lento(description)
        time.sleep(0.5)
        print("\nPressione ENTER para continuar...")
        CLI._ler_tecla()

    @staticmethod
    def show_exploration_menu() -> str:
        """
        O que faz: Imprime "O que deseja fazer? 1. Avançar para próxima sala | 2. Ver Inventário | 3. Ficha de personagem (apenas se der tempo)".
        O que devolve: A string "1" ou "2".
        """
        pass

    @staticmethod
    def _gerar_barra_progresso(
        atual: int,
        maximo: int,
        tamanho: int = 10,
        simbolo_cheio: str = "█",
        simbolo_vazio: str = " ",
    ) -> str:
        """Cria uma barra visual. Ex: [██████    ] 6/10"""
        # Evita divisão por zero se o máximo for 0
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
        """
        O que faz: Desenha a tela de batalha completa e pede a ação do jogador.

        Caminho para adicionar cada argumento na chamada do menu:

        ACOES_DO_HEROI  = instancia_arquetipo_heroi.get_actions()

        NOME_HEROI = variável que guarda o nome recolhido do usuário após o método: ask_hero_info()

        NIVEL_HEROI = Passar o nível que foi passado para a criação do level em que ele está. Ex: (create_room(level = 1, enviroment..)) Esse 1 que foi passado é o que deve ser passado no nível do heroi.

        HP_ATUAL = instancia_arquetipo_heroi.current_life

        HP_MAX = instancia_arquetipo_heroi.max_life

        arte_monstro = sala_level1_criada.monsters[0 ou 1, depende de qual monstro está enfrentadno].art

        nome_monstro = sala_level1_criada.monsters[0 ou 1, depende de qual monstro está enfrentadno].name
        """

        barra_hp = CLI._gerar_barra_progresso(hp_atual, hp_max)

        cor_hp = Color.GREEN if (hp_atual / hp_max) > 0.5 else Color.RED

        # Montamos a "Cena" da batalha juntando o Monstro e o HUD do Herói
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
                # Extrai apenas as descrições do dicionário para mostrar na tela
                textos_ataques = [
                    info["description"] for info in acoes_do_heroi.values()
                ]
                textos_ataques.append(
                    "Voltar"
                )  # Opção salvadora caso o jogador clique errado!

                # Mostra o submenu mantendo a arte do monstro na tela
                escolha_ataque_idx = CLI._mostrar_menu_interativo(
                    f"{Color.RED}ESCOLHA SEU GOLPE:{Color.RESET}",
                    textos_ataques,
                    arte_ascii=cena_batalha,
                )

                # Se ele clicou em "Voltar" (a última opção da lista)
                if escolha_ataque_idx == len(textos_ataques) - 1:
                    continue  # Volta para o início do 'while' (Menu Principal)

                # Se ele escolheu um ataque, pegamos a chave original do dicionário (ex: "1", "2")
                chaves_originais = list(acoes_do_heroi.keys())
                chave_escolhida = chaves_originais[escolha_ataque_idx]

                return chave_escolhida  # O Battle vai receber "1", "2" ou outro número para ativar o método!

            # --- SE ESCOLHEU INVENTÁRIO ---
            elif escolha_idx == 1:
                return "inventario"

            # --- SE ESCOLHEU FUGIR ---
            elif escolha_idx == 2:
                # Easter Egg: Mantém a cena, avisa que não dá, pede um Enter e volta pro menu!
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
                continue  # Volta pro menu principal

    @staticmethod
    def show_inventory(inventory_summary: dict) -> tuple[str, str] | None:
        """
        Exibe o inventário de forma interativa usando o menu padrão da CLI.

        Recebe:
            inventory_summary: dict retornado por Inventory.get_items_summary()

        Retorna:
            (item_name, action) -> quando o jogador escolhe usar/equipar/descartar um item.
            None               -> quando o jogador escolhe "Voltar" no menu de itens.
        """

        items = inventory_summary["items"]

        # Inventário vazio: sem itens, sem navegação
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

        # Dados de cabeçalho (peso) — calculados uma vez fora dos loops
        actual_weight = inventory_summary["current_weight"]
        max_weight = inventory_summary["capacity"]
        weight_color = Color.RED if (actual_weight / max_weight) > 0.8 else Color.GREEN

        header = (
            f"{Color.BROWN}Peso: {Color.RESET}"
            f"{weight_color}{actual_weight:.1f}{Color.RESET}/"
            f"{Color.GREEN}{max_weight:.1f}{Color.RESET}"
        )

        # Mapa fixo: índice da ação → string reconhecida pelo GameManager/Battle
        action_map = {
            0: "usar",
            1: "ver_descricao",
            2: "descartar",
        }

        # Submenu de ações já colorido
        action_options = [
            f"{Color.GREEN}Usar / Equipar{Color.RESET}",
            f"{Color.CYAN}Ver descrição{Color.RESET}",
            f"{Color.RED}Descartar{Color.RESET}",
            f"{Color.GRAY}Voltar ao inventário{Color.RESET}",
        ]

        VOLTAR_INVENTARIO = len(action_options) - 1

        # Loop externo: lista de itens
        # Permanece ativo até o jogador escolher "Voltar" neste nível.
        while True:
            item_options = [
                f"{Color.YELLOW}{item['name']}{Color.RESET} {Color.GRAY}(peso: {item['weight']}){Color.RESET}"
                for item in items
            ]
            item_options.append(f"{Color.GRAY}Voltar{Color.RESET}")

            VOLTAR_MENU = len(item_options) - 1  # constante semântica

            selected_index = CLI._mostrar_menu_interativo(
                titulo=f"{Color.BROWN}INVENTÁRIO{Color.RESET}\n{header}",
                opcoes=item_options,
            )

            # Jogador quer sair do inventário completamente
            if selected_index == VOLTAR_MENU:
                return None

            selected_item = items[selected_index]
            item_name = selected_item["name"]

            # Loop interno: submenu de ações
            while True:
                action_index = CLI._mostrar_menu_interativo(
                    titulo=f"{Color.BROWN}AÇÕES  —  {Color.YELLOW}{item_name}{Color.RESET}",
                    opcoes=action_options,
                )

                if action_index == VOLTAR_INVENTARIO:
                    break  # ← sai só do loop interno; loop externo continua

                # Ação real selecionada → entrega resultado ao chamador
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
    ) -> None:
        """
        Exibe o resumo visual de um turno de combate.
        """

        print("\n" + f"{Color.YELLOW}" + "=" * 60)
        turn_text = f"TURNO {turn_number}"
        print(f"{Color.YELLOW}{turn_text:^60}{Color.RESET}")
        print(f"{Color.YELLOW}=" * 60 + Color.RESET)

        raw_subtitle = f"{hero_name}: {hero_hp}/{hero_max_hp} HP   |   {monster_name}: {monster_hp}/{monster_max_hp} HP"
        espaces = " " * ((60 - len(raw_subtitle)) // 2)

        # Pintando a vida dinamicamente
        cor_hp_heroi = Color.GREEN if (hero_hp / hero_max_hp) > 0.5 else Color.RED
        cor_hp_monstro = (
            Color.DARK_RED if (monster_hp / monster_max_hp) > 0.5 else Color.RED
        )

        str_heroi = f"{Color.CYAN}{hero_name}{Color.RESET}: {cor_hp_heroi}{hero_hp}/{hero_max_hp} HP{Color.RESET}"
        str_monstro = f"{Color.RED}{monster_name}{Color.RESET}: {cor_hp_monstro}{monster_hp}/{monster_max_hp} HP{Color.RESET}"

        # Imprimindo o subtítulo perfeitamente centralizado
        print(f"{espaces}{str_heroi}   {Color.GRAY}|{Color.RESET}   {str_monstro}")
        print(f"{Color.GRAY}-" * 60 + Color.RESET)

        # Status
        if status:
            print(f"\n{Color.MAGENTA}Status:{Color.RESET}")
            for entity_name, state in status.items():
                enitity_color = Color.CYAN if entity_name == hero_name else Color.RED
                print(
                    f"  {enitity_color}{entity_name}{Color.RESET} {Color.GRAY}→ {Color.RESET} {Color.YELLOW}{state}{Color.RESET}"
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


# ====================================================================
# ÁREA DE TESTES VISUAIS E SIMULAÇÃO DE FLUXO PARA A EQUIPE
# (Este código só roda se você executar o cli.py diretamente)
# ====================================================================
if __name__ == "__main__":
    # --- PASSO 1: MENU PRINCIPAL ---
    acao = CLI.show_main_menu()

    if acao == "1":

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

        # --- PASSO 3: TESTE DE INVENTÁRIO (Preparação antes da luta) ---
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

        # --- PASSO 4: TESTE DE COMBATE ---
        # 4.1 O Log de Turno (Apresentando o status da luta)
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
        )

        # 4.2 A Escolha de Ação do Jogador
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

        # --- PASSO 5: RECOMPENSA (Simulando a morte do monstro) ---
        CLI.show_battle_reward(
            monster_name="Dragão de Fogo Ancião",
            dropped_items=["Escama de Fogo", "Coração de Dragão"],
            missed_items=["Espada Giga Quebrada"],
            leveled_up=True,
        )

        # --- PASSO 6: FINAIS (Testando as telas de conclusão) ---
        # Testando primeiro o Game Over
        CLI._limpar_tela()
        print(
            f"{Color.GRAY}Simulando a tela de DERROTA... [Pressione ENTER]{Color.RESET}"
        )
        CLI._ler_tecla()
        CLI.show_game_over()

        # Testando a tela de Vitória (Cutscene + Créditos)
        CLI._limpar_tela()
        print(
            f"{Color.GRAY}Simulando a tela de VITÓRIA FINAL... [Pressione ENTER]{Color.RESET}"
        )
        CLI._ler_tecla()
        CLI.show_victory(nome_heroi)

        # --- RESUMO FINAL DA SIMULAÇÃO ---
        CLI._limpar_tela()
        print(f"{Color.GREEN}=" * 60 + Color.RESET)
        print(f"{Color.YELLOW}{' SIMULAÇÃO DE INTERFACE CONCLUÍDA ':^60}{Color.RESET}")
        print(f"{Color.GREEN}=" * 60 + f"{Color.RESET}\n")

        # Mostrando de forma segura o que o jogador escolheu
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
