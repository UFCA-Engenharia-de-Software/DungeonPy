from typing import List
from domain.entity import Entity
from domain.hero import Hero
from domain.monster import Monster
from domain.state import NeutralState


class Battle:
    """
    Orchestrates the turn-based combat flow between Hero and Monster.

    Responsibilities:
        - Determine the order of attack based on speed.
        - Apply status effects at the beginning of each turn.
        - Check if a participant can act (e.g., Stunned prevents action).
        - Detect the end of combat (death of one side).
        - Collect loot in case of victory.
    """

    def __init__(self, hero: Hero, monster: Monster):
        self.hero = hero
        self.monster = monster
        self.turn_count = 0
        self.is_combat_active = True
        self.turn_order = self._determine_turn_order()

    @property
    def hero(self):
        return self._hero

    @hero.setter
    def hero(self, input):
        if not isinstance(input, Hero):
            raise TypeError("Entrada não é instância de 'Hero'")
        self._hero = input

    @property
    def monster(self):
        return self._monster

    @monster.setter
    def monster(self, input):
        if not isinstance(input, Monster):
            raise TypeError("Entrada não é instância de 'Monster'")
        self._monster = input

    def _determine_turn_order(self) -> List:
        if self.hero.speed > self.monster.speed:
            return [self.hero, self.monster]
        elif self.monster.speed > self.hero.speed:
            return [self.monster, self.hero]
        else:
            # Ao ocorrer um empate o herói tem prioridade
            return [self.hero, self.monster]

    def _apply_status_effects(self, entity: Entity) -> None:
        current_effect = entity.current_status
        if current_effect.duration_turns > 0:
            current_effect.apply_effect(entity)
        else:
            entity.set_status(NeutralState())

    def _can_act(self, entity: Entity) -> bool:
        return True if not entity.current_status.prevents_action() else False

    def _is_combat_over(self) -> bool:
        self.hero.is_active = self.hero.is_it_alive()
        self.monster.is_active = self.monster.is_it_alive()

        return not self.hero.is_active or not self.monster.is_active

    def _execute_hero_action(self, choice: str, turn_log: dict) -> None:
        actions = self.get_available_actions()

        if choice not in actions:
            raise ValueError(f"Ação {choice} é inválida.")

        selected_action = actions[choice]
        action_method = selected_action["method"]
        action_description = selected_action["description"]

        """
        Executes the action.
        Some actions require a target (strike)
        Others do not (rage, aim, reload)
        """
        try:
            action_method(self.monster)
        except TypeError:
            action_method()

        turn_log["actions"].append(f"{self.hero.name} executou '{action_description}'.")

    def get_available_actions(self) -> dict:
        return self.hero.get_actions()

    def execute_turn(self, player_choice: str) -> dict:
        turn_log = {
            "turn": self.turn_count + 1,
            "actions": [],
            "status": {},
            "combat_over": False,
        }

        for entity in self.turn_order:
            # Apply status effects
            self._apply_status_effects(entity)
            turn_log["status"][entity.name] = entity.current_status.name

            # Check if died from effect
            if self._is_combat_over():
                turn_log["combat_over"] = True
                self.is_combat_active = False
                break

            # Check if can act
            if not self._can_act(entity):
                turn_log["actions"].append(
                    f"{entity.name} está impedido de agir ({entity.current_status.name})."
                )
                continue

            # Execute action
            if entity is self.hero:
                self._execute_hero_action(player_choice, turn_log)
            else:
                entity.strike(self.hero)
                turn_log["actions"].append(f"{entity.name} atacou {self.hero.name}.")

            # Check again for end of combat
            if self._is_combat_over():
                turn_log["combat_over"] = True
                self.is_combat_active = False
                break

        combat_result = self.get_combat_result()
        self.turn_count += 1

        return {
            "result": combat_result["result"],
            "loot": combat_result["loot"],
            "turn_log": turn_log,
        }

    def get_combat_result(self) -> dict:
        if self._is_combat_over():
            return (
                {"result": "victory", "loot": self.monster.get_loot()}
                if self.hero.is_active
                else {"result": "defeat", "loot": []}
            )

        return {"result": "ongoing", "loot": []}
