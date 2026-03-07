from typing import List, Optional, TYPE_CHECKING

from domain.hero import Hero
from domain.room import Room
from domain.element import Element
from domain.consumable_item import ConsumableItem
from domain.weapon import Weapon
from domain.grimoire import Grimoire
from services.battle import Battle
from services.hero_factory import HeroFactory
from services.level_factory import LevelFactory

#import game_state
if TYPE_CHECKING:
    from cli import CLI

class GameManager:
    """
    The orchestrator of the DungeonPy game.
    Manages the game state, room progression and the main game loop.
    """

    def __init__(self, cli_instance: 'CLI'):
        self._cli = cli_instance
        self._hero: Optional[Hero] = None
        self._dungeon: List[Room] = []
        self._current_room_index: int = 0
        self._is_running: bool = True

    #STARTING THE GAME:

    def start_game(self) -> None:
        """Entry point of the game."""
        
        choice = self._cli.show_main_menu()

        if choice in ["New Game", "Novo Jogo", "1"]:
            self.setup_new_game()

        elif choice in ["Load Game", "Continuar", "2"]:
            self.load_game()

        elif choice in ["Sair", "Exit", "0"]:
            self._is_running = False

    def setup_new_game(self) -> None:
        """Prepares the board for accessing and using the factories."""
        name, hero_class = self._cli.ask_hero_info()

        #TRANSLATOR:
        class_id = str(hero_class)
        
        if class_id == "1" or class_id == "0": # Using 0 in case of real list index.
            archetype = "warrior"
        elif class_id == "2":
            archetype = "archer"
        elif class_id == "3":
            archetype = "mage"
        else:
            archetype = "warrior" # Just in case (fallback).
        
        self._hero = HeroFactory.create_hero(archetype, name)

        floors = 5
        self._dungeon = [LevelFactory.create_room(level = i) for i in range(1, floors + 1)]
        self.run_exploration_loop()

    #SAVE & LOAD:
    #LEMBRAR DE ADAPTAR ISSO AO CÓDIGO GAME_STATE DE LEÔNCIO!!!

    def save_game(self) -> None:
        """Packages the current game state using the game_state module."""
        if not self._hero:
            return
        
        #success = GameState.save_current_state(
            #hero = self._hero,
            #dungeon = self._dungeon,
            #current_room_index = self._current_room_index
        #)
        success = True #PROVISÓRIO

        if success:
            self._cli.display_message("Jogo salvo com sucesso!")
        else:
            self._cli.display_message("Erro ao salvar o jogo.")

    def load_game(self) -> None:
        """Rebuilds the game from the data found in game_state."""

        #loaded_data = GameState.load_state()
        loaded_data = None #PROVISÓRIO

        if not loaded_data:
            self._cli.display_message("Erro: Save corrompido ou inexistente! Iniciando novo jogo...")
            self.setup_new_game()
            return
        
        self._hero = loaded_data["hero"]
        self._dungeon = loaded_data["dungeon"]
        self._current_room_index = loaded_data["current_room_index"]

        self._cli.display_message(f"Jogo carregado! Bem-vindo de volta, {self._hero.name}.")
        self.run_exploration_loop()


    #LOOPS:

    def run_exploration_loop(self):
        """Main dungeon room exploration loop."""

        # Notepad for remembering rooms.
        last_room_described = -1

        while self._is_running and self._current_room_index < len(self._dungeon):
            current_room = self._dungeon[self._current_room_index]

            if self._current_room_index != last_room_described:
                self._cli.print_room_description(current_room.get_description())
                last_room_described = self._current_room_index

            if current_room.monsters:
                survived = self.run_combat_loop(current_room)

                if not survived:
                    break
            else:
                choice = self._cli.show_exploration_menu()
            
                if choice == "1": #GO FOWARD
                    self._current_room_index += 1

                    if self._current_room_index >= len(self._dungeon):
                        self._cli.show_victory(self._hero.name)
                        self._is_running = False

                elif choice == "2": #OPEN INVENTORY
                    self.open_inventory_menu()

                elif choice == "3": #SAVE GAME
                    self.save_game()

                elif choice == "4": #EXIT
                    self._is_running = False


    def run_combat_loop(self, room: Room):
        """Orchestrates the fight in the current room."""
        room_level = self._current_room_index + 1

        while room.monsters:
            current_monsters = room.monsters[0]
            battle = Battle(self._hero, current_monsters)

            turn_counter = 1

            while battle.is_combat_active:
                hero_status = self._hero.current_status.name if self._hero.current_status else "Neutral"

                actions = self._hero.get_actions()
                choice = self._cli.get_combat_choice(
                    acoes_do_heroi = actions,
                    nome_heroi = self._hero.name,
                    nivel_heroi = room_level,
                    hp_atual = self._hero.current_life,
                    hp_max = self._hero.max_life,
                    arte_monstro = getattr(current_monsters, "art", ""),
                    nome_monstro = current_monsters.name
                )

                if choice == "inventario":
                    self.open_inventory_menu()
                    continue

                turn_result = battle.execute_turn(choice)
                log = turn_result.get("turn_log", {})
                actions_list = log.get("actions", [])

                # CORREÇÃO: Mostramos a tela linda de log de turno para ver a vida descer!
                self._cli.display_turn_log(
                    turn_number = turn_counter,
                    hero_name = self._hero.name,
                    hero_hp = self._hero.current_life,
                    hero_max_hp = self._hero.max_life,
                    monster_name = current_monsters.name,
                    monster_hp = current_monsters.current_life,
                    monster_max_hp = current_monsters.max_life,
                    actions = actions_list,
                    status = {self._hero.name: hero_status} 
                )

                turn_counter += 1

                if not self._hero.is_it_alive():
                    self._cli.show_game_over()
                    self._is_running = False
                    return False
                
            loot = current_monsters.get_loot()
            dropped_names = []
            missed_names = []

            for item in loot:
                if self._hero.inventory.can_add_item(item):
                    self._hero.inventory.add_item_to_inventory(item)
                    dropped_names.append(item.name)
                else:
                    missed_names.append(item.name)
            
            self._cli.show_battle_reward(
                monster_name = current_monsters.name,
                dropped_items = dropped_names,
                missed_items = missed_names,
                leveled_up = True
            )
            
            room.remove_defeated_monster()
    
        return True
    
    def open_inventory_menu(self) -> None:
        """Manages the inventory display and interactions."""

        while True:
            summary = self._hero.inventory.get_items_summary()
            resultado = self._cli.show_inventory(summary)
    
            if not resultado:
                break

            item_name, action = resultado

            item_list = self._hero.inventory.items
            selected_item = next((i for i in item_list if i.name == item_name), None)

            if not selected_item:
                continue

            elif action == "descartar":
                self._hero.inventory.remove_item_from_inventory(selected_item)
                self._cli.display_message(f"{self._hero.name} jogou {selected_item.name} no chão.")

            # IMPLEMENTAR CHECAR DESCRIÇÃO

            elif action == "usar":
                if isinstance(selected_item, ConsumableItem):
                    selected_item.use(self._hero)
                    self._hero.inventory.remove_item_from_inventory(selected_item)
                    self._cli.display_message(f"{self._hero.name} consumiu {selected_item.name}. HP: {self._hero.current_life}/{self._hero.max_life}.")

                elif isinstance(selected_item, Weapon):

                    try:
                        self._hero.equip_weapon(selected_item)
                        self._cli.display_message(f"{self._hero.name} equipou {selected_item.name}!")

                    except ValueError as e:
                        #IF THE PLAYER ALREADY HAs AN EQUIPPED WEAPON:
                        old_one = self._hero.equipped_weapon
                        self._hero.unequip_weapon()
                        self._hero.equip_weapon(selected_item)
                        self._cli.display_message(f"{self._hero.name} trocou {old_one.name} por {selected_item.name}.")

                    except TypeError as e:
                        #IN CASE ANYONE WHO'S NOT A MAGE TRIES TO EQUIP A GRIMOIRE:
                        self._cli.display_message(str(e))
                
                else:
                    self._cli.display_message("Esse item não pode ser usado agora.")

    def process_room_clear(self) -> None:
        """Handles hero progression after cleaning a room."""

        points_to_upgrade = 1
        attribute_choice = self._cli.ask_upgrade_choice()
        self._hero.upgrade(points_to_upgrade, attribute_choice)