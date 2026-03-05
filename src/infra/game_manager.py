from typing import List, Optional, TYPE_CHECKING

from domain.hero import Hero
from domain.room import Room
from domain.consumable_item import ConsumableItem
from domain.weapon import Weapon
from domain.grimoire import Grimoire
from services.battle import Battle
from services.hero_factory import HeroFactory
from services.level_factory import LevelFactory

if TYPE_CHECKING:
    from cli import CLI

class GameManager:
    """
    The orchestrator of the DungeonPy game.
    Manages the game state, room progression and the main game loop.
    """

    def __init__(self, cli_instance: 'CLI'):
        self.cli = cli_instance
        self.hero: Optional[Hero] = []
        self.dungeon: List[Room] = []
        self.current_room_index: int = 0
        self.is_running: bool = True

    def start_game(self) -> None:
        """Entry point of the game."""
        self.cli.show_main_menu()
        choice = self.cli.get_main_menu_choice()

        if choice in ["New Game", "Novo Jogo", "1"]:
            self.setup_new_game()
        elif choice in ["Sair", "Exit", "0"]:
            self.is_running = False

    def setup_new_game(self) -> None:
        """Prepares the board for accessing and using the factories."""
        name, hero_class = self.cli.ask_hero_info
        
        self.hero = HeroFactory.create_hero(name, hero_class)

        floors = 5
        self.dungeon = [LevelFactory.create_room(level = i) for i in range(1, floors + 1)]
        self.run_exploration_loop()

    def run_exploration_loop(self):
        """Main dungeon room exploration loop."""

        while self.is_running and self.current_room_index < len(self.dungeon):
            currrent_room = self.dungeon[self.current_room_index]

            self.cli.print_room_description(currrent_room.get_description())

            if currrent_room.monsters:
                survived = self.run_combat_loop(currrent_room)
                if not survived:
                    break
            else:
                self.cli.show_exploration_menu()
                choice = self.cli.get_exploration_choice
            
                if choice in ["Avançar", "Avance"]:
                    self.current_room_index += 1
                    if self.current_room_index >= len(self.dungeon):
                        self.cli.display_message("Parabéns! Você sobreviveu à Dungeon.")
                        self.is_running = False
                elif choice in ["Ver inventário", "Inventory"]:
                    self.open_inventory_menu()
                elif choice in ["Sair", "Exit"]:
                    self.is_running = False

    def run_combat_loop(self, room: Room):
        """Orchestrates the fight in the current room."""

        while room.monsters:
            current_monsters = room.monsters[0]
            battle = Battle(self.hero, current_monsters)

            while battle.is_combat_active:
                actions = self.hero.get_actions()
                choice = self.cli.get_combat_choice(actions)

                turn_log = battle.execute_turn(choice)
                self.cli.display_turn_log(turn_log)

                if not self.hero.is_it_alive:
                    self.cli.show_game_over()
                    self.is_running = False
                    return False
                
            loot = current_monsters.get_loot()
            for item in loot:
                if self.hero.inventory.can_add_item(item):
                    self.hero.inventory.add_item_to_inventory(item)
                else:
                    self.cli.display_message(f"O inventário está cheio! {item.name} foi deixado para trás.")
            
            room._monsters.pop(0)
    
        return True
    
    def open_inventory_menu(self) -> None:
        """Manages the inventory display and interactions."""

        while True:
            summary = self.hero.inventory.get_items_summary()
            item_list = self.hero.inventory.items
            item_index = self.cli.show_inventory(
                items_sum = summary["items"],
                storage_weight = summary["current_weight"],
                capacity = summary["capacity"],
            )
    
            if item_index == -1:
                break

            selected_item = item_list[item_index]
            action = self.cli.ask_item_action(selected_item.name)

            if action == "Voltar":
                continue
            elif action == "descartar":
                self.hero.inventory.remove_item_from_inventory(selected_item)
                self.cli.display_message(f"{self.hero.name} jogou {selected_item.name} no chão.")
            elif action == "usar":
                if isinstance(selected_item, ConsumableItem):
                    selected_item.use(self.hero)
                    self.hero.inventory.remove_item_from_inventory(selected_item)
                    self.cli.display_message(f"{self.hero.name} consumiu {selected_item.name}. HP: {self.hero.current_life}/{self.hero.max_life}.")
                elif isinstance(selected_item, Weapon):
                    try:
                        self.hero.equip_weapon(selected_item)
                        self.cli.display_message(f"{self.hero.name} equipou {selected_item.name}!")
                    except ValueError as e:
                        #IF THE PLAYER ALREADY HAs AN EQUIPPED WEAPON:
                        old_one = self.hero.equipped_weapon
                        self.hero.unequip_weapon()
                        self.hero.equip_weapon(selected_item)
                        self.cli.display_message(f"{self.hero.name} trocou {old_one.name} por {selected_item.name}.")
                    except TypeError as e:
                        #IN CASE ANYONE WHO'S NOT A MAGE TRIES TO EQUIP A GRIMOIRE:
                        self.cli.display_message(str(e))
                
                else:
                    self.cli.display_message("Esse item não pode ser usado agora.")

    def process_room_clear(self) -> None:
        """Handles hero progression after cleaning a room."""

        points_to_upgrade = 1
        attribute_choice = self.cli.ask_upgrade_choice()
        self.hero.upgrade(points_to_upgrade, attribute_choice)