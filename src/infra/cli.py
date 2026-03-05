import os


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

            print("=" * 60)
            print(f"{titulo:^60}")
            print("=" * 60 + "\n")

            for i, opcao in enumerate(opcoes):
                if i == indice_atual:
                    print(f"  ► {opcao} ◄")
                else:
                    print(f"    {opcao}  ")

            print("\n" + "-" * 60)
            print("[Use as setas ↑ ↓ para mover e ENTER para confirmar]")

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

        arte = r"""
                                                             
▄▄▄▄▄▄                                       ▄▄▄▄▄▄▄         
███▀▀██▄                                     ███▀▀███▄       
███  ███ ██ ██ ████▄ ▄████ ▄█▀█▄ ▄███▄ ████▄ ███▄▄███▀ ██ ██ 
███  ███ ██ ██ ██ ██ ██ ██ ██▄█▀ ██ ██ ██ ██ ███▀▀▀▀   ██▄██ 
██████▀  ▀██▀█ ██ ██ ▀████ ▀█▄▄▄ ▀███▀ ██ ██ ███        ▀██▀ 
                        ██                               ██  
                      ▀▀▀                              ▀▀▀   
        """

        # Adicionando vida ao menu: Subtítulo, decoração e versão
        subtitulo = "  Uma jornada de sombras, escolhas e perdas ".center(60)
        versao = "v1.0.0".rjust(58)  # Fica alinhado à direita

        arte_completa = f"{arte}\n{subtitulo}\n\n{versao}\n"

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
        print("=" * 60)
        print(f"{' O DESPERTAR ':^60}")
        print("=" * 60 + "\n")

        # Um pequeno toque de RPG de mesa antes de pedir o nome
        print("Uma voz antiga e cansada ecoa na escuridão da sua mente...\n")
        time.sleep(1)

        name = ""
        while not name:
            name = (
                input("— Diga-me, alma errante... qual é o seu nome? \n> ")
                .strip()
                .title()
            )
            if not name:
                print("— Não tenha medo. Fale seu nome...\n")

        # Arte das 3 armas lado a lado (Pure ASCII para não bugar)
        arte_classes = r"""
      [ GUERREIRO ]          [ ARQUEIRO ]            [ MAGO ]
        
        o==}=====>             >>--->                   S2
        
       Vida:  150            Vida:  100             Vida:   80
       Ataque: 30            Ataque: 35             Ataque: 50
       Veloc:  10            Veloc:  25             Veloc:  15
        """

        opcoes_classe = [
            "Guerreiro (Especialista em combate corpo a corpo e escudos)",
            "Arqueiro  (Rápido, letal e ataca à distância)",
            "Mago      (Especialista em magias e poder explosivo)",
        ]

        # Passamos a arte_classes para o nosso motor de menu interativo
        escolha_idx = CLI._mostrar_menu_interativo(
            f"Saudações, {name}... Qual caminho você trilhou?",
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

        arte_game_over = r"""
    ██████   ███████ ███    ███ ███████     ███████ ██    ██ ███████ ██████
    ██       ██   ██ ████  ████ ██          ██   ██  ██  ██  ██      ██   ██
    ██   ███ ███████ ██ ████ ██ █████       ██   ██   █  █   █████   ██████
    ██    ██ ██   ██ ██  ██  ██ ██          ██   ██    ██    ██      ██   ██
    ██████   ██   ██ ██      ██ ███████     ███████    ██    ███████ ██   ██
        """

        narrativa = (
            "\nSeu corpo cai ao chão frio da masmorra...\n"
            "As sombras se aproximam enquanto sua visão escurece.\n"
            "\nA princesa continua aguardando por um herói...\n"
        )

        opcoes = [
            "Tentar Novamente",
            "Voltar ao Menu Principal",
        ]

        escolha_idx = CLI._mostrar_menu_interativo(
            "VOCÊ FOI DERROTADO...",
            opcoes,
            arte_ascii=arte_game_over + narrativa,
        )

        return "1" if escolha_idx == 0 else "2"

    @staticmethod
    def _imprimir_lento(texto: str, atraso: float = 0.05) -> None:
        """
        Gera o efeito de máquina de escrever (RPG clássico).
        """
        import sys
        import time

        for char in texto:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(atraso)
        print()  # Quebra a linha no final

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
            print(f"{' A ÚLTIMA SALA ':^60}")
            print("=" * 60)
            print(arte_vela)
            print("\n")

            for texto, atraso in linhas:
                CLI._imprimir_lento(texto, atraso)

            print("\n" + "[...]".center(60))
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

        print("=" * 60)
        print(f"{' CRÉDITOS - DUNGEONPY ':^60}")
        print("=" * 60 + "\n")

        time.sleep(0.5)
        print("DESENVOLVIDO POR:".center(60))
        print("Alan Mendes Vieira".center(60))
        print("Cicero Jesus Da Silva Gomes".center(60))
        print("Leôncio Ferreira Flores Neto".center(60))
        print("Paulo Gabriel Leite Landim".center(60))
        print("Salomão Rodrigues Silva".center(60))

        time.sleep(0.5)
        print("\n\n" + "UNIVERSIDADE FEDERAL DO CARIRI (UFCA)".center(60))
        print("Disciplina de Programação Orientada a Objetos".center(60))
        print("Professor(a): [Jayr Alencar Pereira]".center(60))

        print("\n" + "=" * 60)
        print(" OBRIGADO POR JOGAR DUNGEONPY!".center(60, "*"))
        print("=" * 60)

        print("\n" + "[Pressione ENTER para voltar ao Menu Principal]".center(60))

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

        print("=" * 60)
        print(f"{'VITÓRIA EM BATALHA!':^60}")
        print("=" * 60)

        print(f"\nO terrível {monster_name} foi derrotado!\n".center(60))

        # Efeito visual caso o jogador tenha subido de nível
        if leveled_up:
            print("🌟 LEVEL UP! VOCÊ FICOU MAIS FORTE! 🌟".center(60))
            print()

        print(" RECOMPENSAS ".center(60, "-"))

        # Verifica se o monstro dropou algo ou não
        if dropped_items:
            print("  • Itens recolhidos:")
            for item in dropped_items:
                print(f"      + {item}")
        elif not dropped_items and not missed_items:
            print("  • Itens: Os bolsos do monstro estavam vazios.")

        if missed_items:
            print("\n  ⚠️ AVISO: SUA MOCHILA ESTÁ MUITO PESADA, BURRÃO HEIN! ⚠️")
            print("  Você precisou deixar os seguintes itens para trás:")
            for item in missed_items:
                print(f"      - {item} (Perdido nas sombras)")

        print("-" * 60)

        # Pausa a tela até o jogador ler os espólios e apertar Enter
        print("\n" + "[Pressione ENTER para continuar a exploração]".center(60))
        CLI._ler_tecla()  # Usamos aquele nosso leitor multiplataforma para pausar!

    @staticmethod
    def show_hero_status(status_dict: dict) -> None:
        """
        O que recebe: Um dicionário com todos os status atuais do herói.
        O que faz: Imprime a "Ficha de Personagem" completa e espera uma tecla para voltar.
        Precisa imprimir a ficha bem formatada mostrando os status: "Nome, Vida atual em relação a máxima, ataque, velocidade, e arma atual equipada."
        Para isso, é necessário criar um dict na classe hero, por isso, esse método será opcional e implementado apenas se sobrar tempo
        """
        pass

    # Exploração e Inventário
    @staticmethod
    def print_room_description(description: str) -> None:
        """
        O que recebe: O texto da sala.
        O que faz: Imprime o texto formatado com quebra de linha inteligente
                   e uma borda visual para imersão.
        """
        pass

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

        # Montamos a "Cena" da batalha juntando o Monstro e o HUD do Herói
        cena_batalha = f"""
{arte_monstro}
{nome_monstro.center(60)}

============================================================
 Herói: {nome_heroi} (Nv {nivel_heroi})
 HP: {barra_hp}
============================================================
"""

        opcoes_menu_principal = [
            "Atacar",
            "Inventário",
            "Fugir (Você não pode fugir ainda!)",
        ]

        while True:
            escolha_idx = CLI._mostrar_menu_interativo(
                "O QUE VOCÊ VAI FAZER?", opcoes_menu_principal, arte_ascii=cena_batalha
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
                    "ESCOLHA SEU GOLPE:", textos_ataques, arte_ascii=cena_batalha
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
                print("============================================================")
                print("EU NÃO POSSO FUGIR ANTES DE RESGATAR A PRINCESA...")
                print(
                    "Eu PRECISA lutar (ou talvez os devs só não tenham feito essa opção)! (Aperte ENTER para voltar)"
                )
                print("============================================================")
                input()
                continue  # Volta pro menu principal

    @staticmethod
    def show_inventory(inventory_summary: dict) -> tuple[str, str] | None:
        """
        Exibe o inventário de forma interativa usando o menu padrão da CLI.

        Recebe:
            inventory_summary: dict retornado por Inventory.get_items_summary()

        Retorna:
            (item_name, action) ou None
        """

        items = inventory_summary["items"]

        # Caso inventário vazio
        if not items:
            print("\n" + "=" * 60)
            print(f"{'INVENTÁRIO':^60}")
            print("=" * 60)
            print("\nInventário vazio.")
            input("\nPressione Enter para voltar...")
            return None

        # ===== MENU PRINCIPAL DO INVENTÁRIO =====

        header = (
            f"Peso: "
            f"{inventory_summary['current_weight']:.1f}/"
            f"{inventory_summary['capacity']:.1f}"
        )

        options = [f"{item['name']} (peso: {item['weight']})" for item in items]

        options.append("Voltar")

        selected_index = CLI._mostrar_menu_interativo(
            titulo=f"INVENTÁRIO\n{header}",
            opcoes=options,
        )

        # Se escolheu Voltar
        if selected_index == len(options) - 1:
            return None

        selected_item = items[selected_index]
        item_name = selected_item["name"]

        # ===== SUBMENU DE AÇÕES =====

        action_options = [
            "Usar / Equipar",
            "Ver descrição",
            "Descartar",
            "Voltar",
        ]

        action_index = CLI._mostrar_menu_interativo(
            titulo=f"AÇÕES - {item_name}",
            opcoes=action_options,
        )

        if action_index == 3:
            return None

        action_map = {
            0: "usar",
            1: "ver_descricao",
            2: "descartar",
        }

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

        print("\n" + "=" * 60)
        print(f"{f'TURNO {turn_number}':^60}")
        print("=" * 60)

        # Subtitle estilo inventário
        subtitle = (
            f"{hero_name}: {hero_hp}/{hero_max_hp} HP"
            f"   |   "
            f"{monster_name}: {monster_hp}/{monster_max_hp} HP"
        )
        print(f"{subtitle:^60}")
        print("-" * 60)

        # Status
        if status:
            print("\nStatus:")
            for entity_name, state in status.items():
                print(f"  {entity_name} → {state}")

        # Ações
        if actions:
            print("\nAções:")
            for action in actions:
                print(f"  {action}")

        print("\n" + "=" * 60)
        input("\nPressione Enter para continuar...")


# --- ÁREA DE TESTE ---
# ====================================================================
# ÁREA DE TESTES VISUAIS E EXEMPLO DE USO PARA A EQUIPE
# (Este código só roda se você executar o cli.py diretamente)
# Eu sei que assusta galera, mas podem pedi
# ====================================================================
if __name__ == "__main__":
    acao = CLI.show_main_menu()

    if acao == "1":
        nome_heroi, classe_heroi = CLI.ask_hero_info()

        CLI._limpar_tela()
        print(f"\nSUCESSO! Herói criado: {nome_heroi} (Classe ID: {classe_heroi})")
        print("A masmorra te aguarda...")

        # Informações para conseguir inicializar o menu de combate sem precisar importar as classes do projeto
        # 1. Criamos um dicionário de ataques falso, simulando o que o Herói enviaria

        CLI.show_victory(nome_heroi)

        CLI.show_battle_reward(
            monster_name="irineu", dropped_items=[], missed_items=None, leveled_up=True
        )

        CLI._limpar_tela()

        # ---------------------------------------------------------
        # TESTE 1: LOG DE TURNO (display_turn_log)
        # ---------------------------------------------------------
        # O GameManager/Battle vai extrair os dados reais e passar assim:
        CLI.display_turn_log(
            turn_number=3,
            hero_name=nome_heroi,
            hero_hp=35,
            hero_max_hp=50,
            monster_name="Rei Goblin",
            monster_hp=12,
            monster_max_hp=80,
            actions=[
                f"{nome_heroi} usou Golpe Certeiro e causou 15 de dano!",
                "Rei Goblin tentou revidar, mas errou o ataque!",
            ],
            status={
                "Rei Goblin": "Sangrando (perde 2 HP por turno)",
                nome_heroi: "Focado (+10% de acerto)",
            },
        )

        # ---------------------------------------------------------
        # TESTE 2: MENU DE INVENTÁRIO (show_inventory)
        # ---------------------------------------------------------
        # O GameManager vai pedir o dicionário pro Inventory e mandar pra CLI assim:
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

        # ---------------------------------------------------------
        # RESULTADOS DOS TESTES
        # ---------------------------------------------------------
        CLI._limpar_tela()
        print("=" * 60)
        print(f"{'RESULTADO DOS TESTES':^60}")
        print("=" * 60)

        if escolha_inventario:
            item, acao = escolha_inventario
            print(f"\nO jogador decidiu {acao.upper()} o item: {item}")
        else:
            print("\nO jogador apenas olhou a mochila e apertou 'Voltar'.")

        print("\nTudo funcionando perfeitamente! Pode integrar com o GameManager.")
        CLI._limpar_tela()
        CLI.show_game_over()

    else:
        CLI._limpar_tela()
        print("Saindo do jogo... Até a próxima!")
