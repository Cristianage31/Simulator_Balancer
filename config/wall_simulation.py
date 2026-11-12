from config.game_params import (FIRST_WALL_HEALTH, BASE_WALL_HEALTH_MULTI, WALL_HEALTH_MULTI_INCREASE)

INITIAL_DELAY = 0.12
FADE_TIME = 0.04
SHAKE_TIME = 0.2
WALL_DELAY = 0.07
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
def get_wall_delay(Wall_Count: int):
    return (WALL_DELAY * Wall_Count) + (FADE_TIME) + INITIAL_DELAY

def get_wall_health(Wall_Number: int):
    return FIRST_WALL_HEALTH * ((BASE_WALL_HEALTH_MULTI + WALL_HEALTH_MULTI_INCREASE * (Wall_Number - 1)) ** (2))

def calculate_ind_wall_health(Wall_Number: int, Wall_Index: int):
    total_health = 0.0
    total_health += get_wall_health(Wall_Number)
    total_health *= WALL_HEALTH_DISTRUBTION.get(Wall_Index, 0.0)
    return total_health