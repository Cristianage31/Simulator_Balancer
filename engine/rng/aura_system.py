# rng/aura_system.py
import random
from .drop_tables import ORB_SHOP  # Assumes ORB_SHOP is stored here

class AuraOrbSystem:
    def __init__(self, orb_key="aura_orb_1"):
        config = ORB_SHOP.get(orb_key, ORB_SHOP["aura_orb_1"])
        self.cost = config["base_cost"]
        self.drop_table = config["drops"]
        self.position = config["position"]

    def roll_hatch(self, player_cash):
        """
        Attempts to roll an aura from the orb shop if the player has enough cash.
        Returns: (item_name, multiplier, success_bool)
        """
        if player_cash < self.cost:
            return None, 0.0, False
            
        roll = random.random()
        cumulative = 0.0
        
        for drop in self.drop_table:
            name = drop[0]
            mult = drop[1]
            prob = drop[2]
            # drop[3] could be an extra tuning parameter (e.g. rarity scale) if present
            
            cumulative += prob
            if roll <= cumulative:
                return name, mult, True
                
        # Fallback to the first drop item if float rounding issues occur
        fallback = self.drop_table[0]
        return fallback[0], fallback[1], True