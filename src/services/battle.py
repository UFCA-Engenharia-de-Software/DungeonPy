from typing import List
from domain.entity import Entity
from domain.hero import Hero
from domain.monster import Monster
from domain.state import NeutralState
from domain.consumable_item import ConsumableItem


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
            # In the event of a tie, the hero has priority
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

    def _get_archer_ammo_info(self) -> str | None:
        """Returns a formatted ammo string if hero is an Archer, else None."""
        if hasattr(self.hero, "current_ammo") and hasattr(self.hero, "max_ammo"):
            return f"[Flechas: {self.hero.current_ammo}/{self.hero.max_ammo}]"
        return None

    def _execute_hero_action(self, choice: str, turn_log: dict) -> bool:
        """
        Executes the hero's chosen action and enriches the turn_log.

        Returns:
            bool: True if the action consumed the hero's turn (attacks, skills,
                  consumables), False if it was a non-turn action (reserved for
                  future use). Currently all actions consume the turn.
        """
        actions = self.get_available_actions()

        if choice not in actions:
            raise ValueError(f"Ação {choice} é inválida.")

        selected_action = actions[choice]
        action_method = selected_action["method"]
        action_description = selected_action["description"]

        # --- Detect consumable use BEFORE executing ---
        # The action method for consumables points to item.use(), which does NOT
        # receive a target. We detect this by checking if the bound method's owner
        # is a ConsumableItem instance, signaling that the turn is spent healing.
        consumable_item = getattr(action_method, "__self__", None)
        is_consumable_action = isinstance(consumable_item, ConsumableItem)

        # Bloqueia poção de mana para classes sem mana (Guerreiro, Arqueiro).
        # O turno NÃO é consumido — o jogador deve escolher outra ação.
        if (
            is_consumable_action
            and getattr(consumable_item, "recovery_type", "life") == "mana"
        ):
            if not hasattr(self.hero, "current_mana"):
                turn_log["actions"].append(
                    f"⚠️  {self.hero.name} tentou usar '{action_description}', "
                    f"mas não possui mana. Apenas Magos se beneficiam disso."
                )
                turn_log["action_failed"] = True
                return False

        # --- Detect special states BEFORE executing (aim / rage) ---
        was_aiming_before = getattr(self.hero, "is_aiming", False)
        was_enraged_before = getattr(self.hero, "is_enraged", False)

        # --- Snapshot life values to detect damage dealt / received ---
        monster_life_before = self.monster.current_life
        hero_life_before = self.hero.current_life
        monster_status_before = (
            self.monster.current_status.name
            if self.monster.current_status
            else "Neutral"
        )

        # --- Snapshot dodge state before action (Archer) ---

        try:
            action_method(self.monster)
        except TypeError:
            action_method()
        except ValueError as e:
            # "If insufficient resources (no ammunition, no mana, etc.)
            # The turn is NOT consumed — the player must choose another action."
            turn_log["actions"].append(f"⚠️  {self.hero.name}: {e}")
            turn_log["action_failed"] = True
            return False

        # 1. Consumable used: inform recovery and that the turn was spent
        if is_consumable_action:
            recovery_type = getattr(consumable_item, "recovery_type", "life")
            if recovery_type == "mana":
                turn_log["actions"].append(
                    f"🧪 {self.hero.name} usou '{action_description}' e recuperou "
                    f"{consumable_item.recovered_value} de mana. "
                    f"MP: {self.hero.current_mana}/{self.hero.max_mana}. (Turno consumido)"
                )
            else:
                life_recovered = self.hero.current_life - hero_life_before
                turn_log["actions"].append(
                    f"🧪 {self.hero.name} usou '{action_description}' e recuperou "
                    f"{life_recovered} de vida. (Turno consumido)"
                )
            turn_log["hero_used_consumable"] = True
            return True  # Turn is consumed

        # 2. Aiming: Archer sacrificed the turn to focus
        if not was_aiming_before and getattr(self.hero, "is_aiming", False):
            turn_log["actions"].append(
                f"🎯 {self.hero.name} está mirando! Próximo ataque terá acerto "
                f"garantido e dano aumentado. (Turno consumido)"
            )
            turn_log["special_state"] = "aiming"
            ammo_info = self._get_archer_ammo_info()
            if ammo_info:
                turn_log["actions"].append(f"   {ammo_info}")
            return True

        # 3. Rage: Warrior activated fury
        if not was_enraged_before and getattr(self.hero, "is_enraged", False):
            turn_log["actions"].append(
                f"💢 {self.hero.name} entra em FÚRIA! Defesa reduzida, mas próximo "
                f"ataque causará dano dobrado. (Turno consumido)"
            )
            turn_log["special_state"] = "enraged"
            return True

        # 4. Reload: Archer reloaded (no target, turn consumed)
        ammo_after = getattr(self.hero, "current_ammo", None)
        ammo_max = getattr(self.hero, "max_ammo", None)
        if ammo_after is not None and ammo_max is not None:
            ammo_info = f"[Flechas: {ammo_after}/{ammo_max}]"
            # Detect reload: ammo increased without an attack being made
            ammo_before_action = getattr(self, "_ammo_snapshot", ammo_after)
            if (
                ammo_after > ammo_before_action
                and monster_life_before == self.monster.current_life
            ):
                turn_log["actions"].append(
                    f"🔄 {self.hero.name} recarregou a aljava! {ammo_info} (Turno consumido)"
                )
                return True

        # 5. Attack: check if monster dodged / blocked, or if hero missed
        damage_dealt = monster_life_before - self.monster.current_life

        if damage_dealt <= 0:
            # Missed (e.g. dodge mechanic on the monster side or 0-damage edge case)
            turn_log["actions"].append(
                f"💨 {self.hero.name} atacou, mas {self.monster.name} esquivou ou o ataque errou!"
            )
        else:
            attack_msg = (
                f"⚔️  {self.hero.name} executou '{action_description}' "
                f"e causou {damage_dealt} de dano em {self.monster.name}."
            )
            # Append aiming bonus note if hero was aiming before this attack
            if was_aiming_before:
                attack_msg += " (Dano de mira!)"
            turn_log["actions"].append(attack_msg)

        monster_status_after = (
            self.monster.current_status.name
            if self.monster.current_status
            else "Neutral"
        )

        # Se o monstro estava normal e agora tem status, avisa na tela!
        if monster_status_before == "Neutral" and monster_status_after != "Neutral":
            # Manter emojis, pois não dá para trocar as cores
            status_pt = {
                "Burned": "🔥 QUEIMADURA",
                "Frozen": "❄️ CONGELAMENTO",
                "Poison": "☠️ VENENO",
                "Stunned": "⚡ ATORDOAMENTO",
            }
            nome_status = status_pt.get(monster_status_after, monster_status_after)
            turn_log["actions"].append(
                f"✨ O ataque do seu elemento aplicou {nome_status} em {self.monster.name}!"
            )

        # Always append ammo info for Archer after any action
        ammo_info = self._get_archer_ammo_info()
        if ammo_info:
            turn_log["actions"].append(f"   {ammo_info}")

        return True

    def _execute_monster_action(self, turn_log: dict) -> None:
        """
        Executes the monster's attack against the hero and enriches the turn_log,
        reporting dodge (Archer) and block (Warrior) outcomes.
        """
        hero_life_before = self.hero.current_life
        dodge_before = getattr(self.hero, "dodge", False)

        self.monster.strike(self.hero)

        hero_life_after = self.hero.current_life
        damage_taken = hero_life_before - hero_life_after

        # --- Dodge (Archer) ---
        # After damage_received(), the Archer resets self.dodge to False if it dodged.
        # We detect the dodge by checking: was dodge True before, and now life didn't drop.
        dodged = dodge_before and damage_taken == 0
        if dodged:
            turn_log["actions"].append(
                f"💨 {self.hero.name} esquivou do ataque de {self.monster.name}!"
            )
            return

        # --- Block (Warrior) ---
        # Warrior.damage_received sets self.last_blocked = True when a block occurs.
        blocked = getattr(self.hero, "last_blocked", False)
        if blocked:
            turn_log["actions"].append(
                f"🛡️  {self.hero.name} bloqueou o ataque de {self.monster.name}! "
                f"Dano reduzido: -{damage_taken} HP."
            )
            # Reset the flag so it doesn't persist to next turn
            self.hero.last_blocked = False
            return

        # --- Normal hit ---
        if damage_taken > 0:
            turn_log["actions"].append(
                f"🐉 {self.monster.name} atacou {self.hero.name} e causou {damage_taken} de dano."
            )
        else:
            # Hit but dealt no damage (e.g. full armor absorption)
            turn_log["actions"].append(
                f"🐉 {self.monster.name} atacou {self.hero.name}, mas não causou dano!"
            )

    def get_available_actions(self) -> dict:
        return self.hero.get_actions()

    def execute_turn(self, player_choice: str) -> dict:
        turn_log = {
            "turn": self.turn_count + 1,
            "actions": [],
            "status": {},
            "combat_over": False,
            "hero_used_consumable": False,
            "special_state": None,
        }

        # Snapshot ammo at the start of turn for reload detection
        self._ammo_snapshot = getattr(self.hero, "current_ammo", None)

        for entity in self.turn_order:
            # Apply status effects
            self._apply_status_effects(entity)
            turn_log["status"][entity.name] = entity.current_status.name

            # Check if died from status effect
            if self._is_combat_over():
                turn_log["combat_over"] = True
                self.is_combat_active = False
                break

            # Check if can act
            if not self._can_act(entity):
                turn_log["actions"].append(
                    f"😵 {entity.name} está impedido de agir ({entity.current_status.name})."
                )
                continue

            # Execute action
            if entity is self.hero:
                action_succeeded = self._execute_hero_action(player_choice, turn_log)

                # If the action fails (e.g., no ammunition/mana), the entire turn is canceled.
                # The monster does not act and the player chooses again without penalty.
                if not action_succeeded:
                    break

            else:
                self._execute_monster_action(turn_log)

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
