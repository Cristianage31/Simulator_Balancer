# config/game_params.py

# ---------- PLAYER LEVEL ---------------------
PLAYER_BASE_LEVEL_XP_REQUIREMENT = 25.0 # Base XP required to reach level 2, will scale with PLAYER_LEVEL_BASE_XP_MULTIPLIER and PLAYER_LEVELS_XP_ADDITION
PLAYER_LEVELS_THRESHOLD = 10 # Every this amount of levels, the XP multiplier will increase by a multiplier
PLAYER_LEVEL_BASE_XP_MULTIPLIER = 1.18 # ratio for calculating the next level's XP requirement
PLAYER_LEVELS_XP_ADDITION = 0.02 # ratio for calculating the next level's XP requirement
WALK_SPEED_ADDITION = 0.5 # walkspeed increment for every level up
INTIAL_WALKSPEED = 16.0 # start walkspeed

# ---------- TELEPORT ---------------------

WINS_TO_TELEPORT_RATIO = 5.0 # teleport will cost the stage reward times this ratio in wins (4 seconds to do)

# ---------- WALLS ---------------------


FIRST_WALL_HEALTH = 100.0 # Between the first 10 walls, this is the health of the first wall
BASE_WALL_HEALTH_MULTI = 1.41 # Each will be this much stronger than the previous wall
WALL_HEALTH_MULTI_INCREASE = 0.1 # this adds to the BASE_WALL_HEALTH_MULTI every WALL_HEALTH_MULTI_INCREASE_LEVELS
BASE_WIN_REWARD = 1.0 # Between the first 10 walls, this is the reward of the first wall
WIN_REWARD_EXPO = 2.0 # Each will be this much stronger than the previous wall
INITIAL_DELAY = 0.12 # WALL HEALTH DELAY
FADE_TIME = 0.04 # DELAY AFTER THE WALL DELAY
WALL_DELAY = 0.07 # DELAY PER WALL
WALL_EXPONENT = 2.0 # The exponent for the wall health formula, higher means walls get stronger faster
WALL_HEALTH_DISTRUBTION = {
    1: 0.08,
    2: 0.084,
    3: 0.088,
    4: 0.092,
    5: 0.096,
    6: 0.104,
    7: 0.108,
    8: 0.112,
    9: 0.116,
    10: 0.12,
}

# ---------- AURAS ---------------------
AURA_XP_ARTH_START = 1.0 # Amount of auras (xp) from level 1->2
AURA_XP_ARTH_STEP = 2.0 # Amount of auras (xp) from level 2->3, 3->4, etc. (increases by this amount each level) in addition to the AURA_XP_ARTH_START
AURA_LEVEL_MULTIPLIER = 0.1 # Each level of aura increases the multiplier by this amount

# ---------- REBIRTHS ---------------------
REBIRTH_BASE_MULTIPLIER = 1.0 # Base multiplier for each rebirths
REBIRTH_BASE_LEVEL = 10 # Base level requirement for the first rebirth (every this number e.g 10)
REBIRTH_ADD_BASE_MULTI = 1.0 # Each rebirth will increase the multiplier by this amount so,  EX: 3 rebirths has a 4x multi and 100 has a 101x multi

def get_wall_delay(Wall_Count: int):
    return (WALL_DELAY * Wall_Count) + (FADE_TIME) + INITIAL_DELAY

def get_wall_health(Wall_Number: int):
    return FIRST_WALL_HEALTH * ((BASE_WALL_HEALTH_MULTI + WALL_HEALTH_MULTI_INCREASE * (Wall_Number - 1)) ** WALL_EXPONENT)

def calculate_ind_wall_health(Wall_Number: int, Wall_Index: int):
    total_health = 0.0
    total_health += get_wall_health(Wall_Number)
    total_health *= WALL_HEALTH_DISTRUBTION.get(Wall_Index, 0.0)
    return total_health