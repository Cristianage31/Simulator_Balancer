# config/map_layout.py
SIMULATOR_GATES = [
    {
        "zone_id": "zone_2",
        "position_x": 400.0,
        "position_y": 200.0,
        "required_stat": "speed",
        "stat_threshold": 250.0,     # Must have 250 Speed to pass
        "unlock_cost": 1000.0,       # And/or 1,000 cash
    },
    {
        "zone_id": "zone_3",
        "position_x": 900.0,
        "position_y": 600.0,
        "required_stat": "speed",
        "stat_threshold": 1200.0,
        "unlock_cost": 15000.0,
    },
]