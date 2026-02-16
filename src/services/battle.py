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

    def _execute_hero_action(self, choice: str) -> str:
        actions = self.get_available_actions()
        if choice in actions.keys():
            actions[choice](self.monster)
        else:
            raise ValueError(f"Ação {choice} é inválida.")

    def get_available_actions(self) -> dict:
        return self.hero.get_actions()

    def execute_turn(self, player_choice: str) -> dict:
        # Para cada entidade na turn_order:
        #   1. _apply_status_effects
        #   2. _is_combat_over (efeito pode matar)
        #   3. _can_act (stunned pula turno)
        #   4. Se HERÓI → _execute_hero_action(player_choice)
        #      Se MONSTRO → monster.strike(hero)
        #   5. _is_combat_over
        # Retorna dict com log do turno
        turn_log = {
            "turn": self.turn_count + 1,
            "actions": [],
            "status": {},
            "combat_over": False,
        }

        for entity in self.turn_order:
            # 1. Aplica efeitos de status
            self._apply_status_effects(entity)

            turn_log["status"][entity.name] = entity.current_status.name

            # 2. Verifica se o combate acabou (status pode matar)
            if self._is_combat_over():
                turn_log["combat_over"] = True
                self.is_combat_active = False
                break

            # 3. Verifica se pode agir
            if not self._can_act(entity):
                turn_log["actions"].append(
                    f"{entity.name} está impedido de agir ({entity.current_status.name})."
                )
                continue

            # 4. Executa ação
            if entity is self.hero:
                if player_choice == "attack":
                    self.hero.strike(self.monster)
                    executed_action = "attack"
                else:
                    raise ValueError(f"Ação {player_choice} é inválida.")

                turn_log["actions"].append(
                    f"{entity.name} executou a ação '{executed_action}'."
                )

            else:
                entity.strike(self.hero)
                turn_log["actions"].append(f"{entity.name} atacou {self.hero.name}.")

            # 5. Verifica novamente se o combate acabou
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
