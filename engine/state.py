from config.game_params import INTIAL_WALKSPEED
# engine/state.py
class PlayerState:
    def __init__(self):
        self.clicks = 0.0
        self.punch_power = 0.0
        self.pos_x = 0.0
        self.pos_y = 0.0

        self.wins = 0.0
        
        # 1. Leveling & Speed
        self.level = 1
        self.walkspeed = INTIAL_WALKSPEED
        
        # 2. Rebirth System
        self.rebirth_count = 0
        self.rebirth_multiplier = 1.0
        
        # 3. Gear & Training
        self.gear_level = 0
        self.training_multiplier = 1.0
        
        # 4. Aura Inventory (Keyed by Aura ID to handle duplicates & levels)
        # Structure: {"aura_id": {"name": str, "level": int, "multiplier": float}}
        self.aura_inventory = {}
        self.equipped_aura_id = None

        # Punching
        self.punching_bag_level = 1
        self.punch_cooldown = 0.12
        self.click_cooldown = 0.15  # Auto-clicker frequency (seconds)
        self.click_timer = 0.0      # Accumulator for timing clicks
        
        # Movement & Intent
        self.target_x = None
        self.target_y = None
        self.action_intent = "TRAIN"