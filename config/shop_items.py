# config/shop_items.py

# Gears (e.g., Weights, Swords, Dumbbells) that boost base training power
GLOVE_SHOP = [
    {"id": "tier_1_glove", "name": "glove 1", "base_cost": 5.0, "power_bonus_base": 2.0},
    {"id": "tier_2_glove", "name": "glove 2", "base_cost": 25.0, "power_bonus_base": 4.0},
    {"id": "tier_3_glove", "name": "glove 3", "base_cost": 125.0, "power_bonus_base": 8.0},
    {"id": "tier_4_glove", "name": "glove 4", "base_cost": 625.0, "power_bonus_base": 16.0},
    {"id": "tier_5_glove", "name": "glove 5", "base_cost": 5 * 625.0, "power_bonus_base": 32.0},
    {"id": "tier_6_glove", "name": "glove 6", "base_cost": 25 * 625.0, "power_bonus_base": 64.0},
    {"id": "tier_7_glove", "name": "glove 7", "base_cost": 125 * 625.0, "power_bonus_base": 128.0},
    {"id": "tier_8_glove", "name": "glove 8", "base_cost": 625.0 * 625.0, "power_bonus_base": 256.0},
    {"id": "tier_9_glove", "name": "glove 9", "base_cost": 5 * 625.0 * 625.0, "power_bonus_base": 512.0},
    {"id": "tier_10_glove", "name": "glove 10", "base_cost": 25 * 625.0 * 625.0, "power_bonus_base": 1024.0},
]

# Auras that grant multiplicative passive stat boosts
AURA_SHOP = [
    {"id": "aura_orb_1", "name": "Orb 1", "base_cost": 100.0},
    {"id": "aura_orb_2", "name": "Orb 2", "base_cost": 1200.0},
    {"id": "aura_orb_3", "name": "Orb 3", "base_cost": 15000.0},
]