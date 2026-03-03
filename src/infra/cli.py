import os
import msvcrt


class CLI:
    """
    Classe responsável pela interface visual e interação com o jogador.
    Usa menus interativos com setas do teclado para maior imersão.
    """

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
            tecla = msvcrt.getch()

            if tecla in [b"\xe0", b"\x00"]:
                direcao = msvcrt.getch()
                if direcao == b"H":  # Seta para CIMA
                    indice_atual = (indice_atual - 1) % len(opcoes)
                elif direcao == b"P":  # Seta para BAIXO
                    indice_atual = (indice_atual + 1) % len(opcoes)

            elif tecla == b"\r":  # APENAS o \r, sem o \n que estava causando o bug!
                return indice_atual

    @staticmethod
    def show_main_menu() -> str:
        """Exibe o menu principal com a arte do jogo."""
        arte = r"""
         ____                                  ____
        |  _ \ _   _ _ __   __ _  ___  ___  _ |  _ \ _   _
        | | | | | | | '_ \ / _` |/ _ \/ _ \| || |_) | | | |
        | |_| | |_| | | | | (_| |  __/ (_) | ||  __/| |_| |
        |____/ \__,_|_| |_|\__, |\___|\___/|_||_|    \__, |
                           |___/                     |___/
        """
        opcoes = ["Iniciar Nova Jornada", "Sair do Jogo"]

        escolha_idx = CLI._mostrar_menu_interativo(
            "MENU PRINCIPAL", opcoes, arte_ascii=arte
        )

        return "1" if escolha_idx == 0 else "2"

    @staticmethod
    def ask_hero_info() -> tuple[str, str]:
        """Guia o jogador na criação do personagem."""
        CLI._limpar_tela()
        print("=" * 60)
        print(f"{'CRIAÇÃO DE PERSONAGEM':^60}")
        print("=" * 60 + "\n")

        name = ""
        while not name:
            name = input("Qual o nome do seu Herói? ").strip().title()
            if not name:
                print("O nome não pode ficar em branco!\n")

        opcoes_classe = [
            "Guerreiro (Especialista em combate corpo a corpo e escudos)",
            "Arqueiro  (Rápido, letal e ataca à distância)",
        ]

        escolha_idx = CLI._mostrar_menu_interativo(
            f"Saudações, {name}! Escolha sua vocação:", opcoes_classe
        )

        class_choice = "1" if escolha_idx == 0 else "2"

        # O retorno name vai ser usado na variável nome_heroi na parte de combate e a class_choice para a escolha da classe
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
    def show_victory() -> None:
        """
        O que faz: Imprime tela gloriosa de vitória.
        """
        pass

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
        ataques_falsos = {
            "1": {"description": "Flecha de Fogo", "damage": 10},
            "2": {"description": "Tiro Preciso", "damage": 15},
            "3": {"description": "Chuva de Flechas", "damage": 20},
        }

        # 2. Uma arte de monstro temporária
        slime_art = r"""
          ______
        /        \
       /  O    O  \
      |    \__/    |
       \__________/
    """

        # 3. Chamamos o método de combate
        # Note que passamos dados manuais para simular o estado do jogo
        escolha = CLI.get_combat_choice(
            acoes_do_heroi=ataques_falsos,
            nome_heroi="Paulo Gabriel",
            nivel_heroi=5,
            hp_atual=50,
            hp_max=100,
            arte_monstro=slime_art,
            nome_monstro="Slime Azul",
        )

        # 4. Resultado do teste

        CLI._limpar_tela()
        print(f"O teste funcionou! O 'Battle' receberia a chave: {escolha}")

    else:
        CLI._limpar_tela()
        print("Saindo do jogo... Até a próxima!")
