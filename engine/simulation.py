# engine/simulation.py
from engine.state import PlayerState
from .rng.aura_system import AuraOrbSystem
from config.training_stations import TRAINING_STATIONS
from config.game_params import (
    PLAYER_BASE_LEVEL_XP_REQUIREMENT,
    PLAYER_LEVELS_THRESHOLD,
    PLAYER_LEVEL_BASE_XP_MULTIPLIER,
    PLAYER_LEVELS_XP_ADDITION,
    WALK_SPEED_ADDITION,
    INTIAL_WALKSPEED,
    AURA_LEVEL_MULTIPLIER,
    get_wall_delay,
    calculate_ind_wall_health
)

class SimulatorEngine:
    def __init__(self, dt=0.05):
        self.dt = dt
        self.elapsed_time = 0.0
        
        # Player actor state
        self.player = PlayerState()
        
        # World progression (30 sets of 10 walls = 300 total walls)
        self.current_wall_group = 1   # Group tier (1 to 30)
        self.current_wall_index = 1   # Segment inside set (1 to 10)
        self.active_wall_hp = calculate_ind_wall_health(self.current_wall_group, self.current_wall_index)
        
        # Non-accumulating banked wins available upon cashing out
        self.banked_wins = 0.0
        
        # Aura Gacha Subsystem
        self.aura_system = AuraOrbSystem("aura_orb_1")

    def _recalculate_multipliers(self):
        """Updates player training multiplier based on equipped Auras and Gear."""
        if self.player.aura_inventory:
            best_aura_mult = max(
                item["base_mult"] * (1.0 + (item["level"] - 1) * AURA_LEVEL_MULTIPLIER) 
                for item in self.player.aura_inventory.values()
            )
        else:
            best_aura_mult = 1.0
            
        gear_bonus = 1.0 + (self.player.gear_level * 0.3)
        self.player.training_multiplier = (best_aura_mult * gear_bonus) * self.player.rebirth_multiplier

    def _check_level_up(self, power_gained: float):
        """Levels up player and updates movement speed based on working clicks/power."""
        self.player.punch_power = power_gained  # Track power gained per click
        
        level_threshold = PLAYER_BASE_LEVEL_XP_REQUIREMENT * (
            (PLAYER_LEVEL_BASE_XP_MULTIPLIER + (PLAYER_LEVELS_XP_ADDITION * (self.player.level // PLAYER_LEVELS_THRESHOLD))) ** (self.player.level - 1)
        )
        if self.player.clicks >= level_threshold:
            self.player.level += 1
            self.player.walkspeed = INTIAL_WALKSPEED + (self.player.level * WALK_SPEED_ADDITION)

    def _get_total_set_health(self):
        """Calculates total combined health of all 10 walls in the current group set."""
        total_hp = 0.0
        for idx in range(1, 11):
            total_hp += calculate_ind_wall_health(self.current_wall_group, idx)
        return total_hp

    def step(self):
        self.elapsed_time += self.dt
        # ---------------------------------------------------------------------
        # AUTO CLICK
        # ---------------------------------------------------------------------
        base_click_gain = 1.0
        power_per_click = (base_click_gain * self.player.rebirth_multiplier) * self.player.training_multiplier
        self.player.clicks += power_per_click
        self._check_level_up(power_per_click)

        # ---------------------------------------------------------------------
        # WALK TOWARDS GOAL WHILE NOT THERE
        # ---------------------------------------------------------------------
        if self.player.target_x is not None and self.player.target_y is not None:
            dx = self.player.target_x - self.player.pos_x
            dy = self.player.target_y - self.player.pos_y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            
            if distance > 0:
                move_distance = min(self.player.walkspeed * self.dt, distance)
                move_ratio = move_distance / distance
                self.player.pos_x += dx * move_ratio
                self.player.pos_y += dy * move_ratio
                return

        # ---------------------------------------------------------------------
        # 1. ACTION: TRAIN (Grind Punching Bags / Auto-Clicker)
        # ---------------------------------------------------------------------
        if self.player.action_intent == "TRAIN":
            self.player.click_timer += self.dt
            
            # Fire clicks according to the 0.15s auto-clicker interval
            while self.player.click_timer >= self.player.click_cooldown:
                self.player.click_timer -= self.player.click_cooldown
                
                # Get highest unlocked punching bag
                unlocked_stations = [s for s in TRAINING_STATIONS if s["required_gate"] <= self.player.rebirth_count]
                active_station = unlocked_stations[-1] if unlocked_stations else TRAINING_STATIONS[0]
                
                # Power gained per click
                base_click_gain = 1.0
                power_per_click = (base_click_gain * active_station["station_multiplier"]) * self.player.training_multiplier * self.player.rebirth_multiplier
                
                # Add to total clicks (working attack power pool)
                self.player.clicks += power_per_click
                self._check_level_up(power_per_click)

        # ---------------------------------------------------------------------
        # 2. ACTION: BREAK WALLS
        # ---------------------------------------------------------------------
        elif self.player.action_intent == "BREAK_WALL":
            # Damage dealt to wall health is driven directly by total accumulated clicks
            dps = (self.player.clicks * 1.5) * self.player.rebirth_multiplier
            self.active_wall_hp -= dps * self.dt
            
            if self.active_wall_hp <= 0:
                transition_delay = get_wall_delay(self.current_wall_group)
                self.elapsed_time += transition_delay
                
                self.current_wall_index += 1
                
                # Completed a set of 10 walls
                if self.current_wall_index > 10:
                    # Non-accumulating Win Formula: 2^(group - 1)
                    # e.g., Reaching Group 4 sets banked wins strictly to 2^3 = 8
                    self.banked_wins = float(2 ** (self.current_wall_group - 1))
                    
                    self.current_wall_group += 1
                    self.current_wall_index = 1
                
                if self.current_wall_group > 30:
                    self.current_wall_group = 30
                    self.current_wall_index = 10
                    self.active_wall_hp = 0
                else:
                    self.active_wall_hp = calculate_ind_wall_health(
                        self.current_wall_group, 
                        self.current_wall_index
                    )

        # ---------------------------------------------------------------------
        # 3. ACTION: COLLECT REWARD (Cash Out & Teleport Back to Wall 1)
        # ---------------------------------------------------------------------
        elif self.player.action_intent == "COLLECT_REWARD":
            # Banked wins become spendable wins currency
            self.player.wins += self.banked_wins
            self.banked_wins = 0.0
            
            # Teleport back to start line (Wall Group 1, Segment 1)
            self.current_wall_group = 1
            self.current_wall_index = 1
            self.active_wall_hp = calculate_ind_wall_health(self.current_wall_group, self.current_wall_index)

        # ---------------------------------------------------------------------
        # 4. ACTION: HATCH AURAS (Uses Spendable Wins as Currency)
        # ---------------------------------------------------------------------
        elif self.player.action_intent == "HATCH":
            roll_result = self.aura_system.roll_hatch(self.player.wins)
            if roll_result and len(roll_result) >= 3:
                name, mult, success = roll_result[0], roll_result[1], roll_result[2]
                if success and self.player.wins >= self.aura_system.cost:
                    self.player.wins -= self.aura_system.cost
                    aura_id = name.lower().replace(" ", "_")
                    
                    if aura_id in self.player.aura_inventory:
                        self.player.aura_inventory[aura_id]["level"] += 1
                    else:
                        self.player.aura_inventory[aura_id] = {
                            "name": name,
                            "level": 1,
                            "base_mult": mult
                        }
                    self._recalculate_multipliers()

    def get_telemetry_snapshot(self):
        return {
            "elapsed_time": round(self.elapsed_time, 2),
            "level": self.player.level,
            "wins": round(self.player.wins, 2),
            "banked_wins": round(self.banked_wins, 2),
            "clicks": round(self.player.clicks, 2),
            "punch_power": round(self.player.punch_power, 2),
            "wall_group": self.current_wall_group,
            "wall_segment": self.current_wall_index,
            "wall_hp_left": round(self.active_wall_hp, 2),
            "action_intent": self.player.action_intent,
            "walkspeed": self.player.walkspeed,
            "rebirth_count": self.player.rebirth_count,
        }

    def run_to_completion(self, max_time=120.0):
        telemetry_logs = []
        
        while self.elapsed_time < max_time:
            total_set_hp = self._get_total_set_health()
            
            # -----------------------------------------------------------------
            # TUNED AI AGENT DECISION HEURISTIC:
            # -----------------------------------------------------------------
            
            # 1. CASH OUT: If wall health is significantly higher than our clicks,
            # or if we have banked wins and we've climbed past group 3, cash out!
            if (total_set_hp >= (self.player.clicks * 5.0) or self.current_wall_group >= 4) and self.banked_wins > 0:
                self.player.action_intent = "COLLECT_REWARD"
                
            # 2. HATCH / UPGRADE: If we have spendable wins after cashing out, hatch auras
            elif self.player.wins >= self.aura_system.cost and len(self.player.aura_inventory) < 3:
                self.player.action_intent = "HATCH"
                
            # 3. TRAIN: If our click power is lagging behind the wall set requirements, train at bags
            elif (self.player.clicks * 1.5) < (total_set_hp / 10.0):
                self.player.action_intent = "TRAIN"
                
            # 4. BREAK WALLS: Otherwise, keep pushing
            else:
                self.player.action_intent = "BREAK_WALL"
                
            self.step()
            telemetry_logs.append(self.get_telemetry_snapshot())
            
        return telemetry_logs

TycoonSimulation = SimulatorEngine