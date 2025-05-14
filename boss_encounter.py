import json

import config
from enemy import Enemy

def load_boss_data(json_file="bosses.json"):
    with open(json_file, "r") as file:
        return json.load(file)

def is_boss_level(dungeon_level):
    return dungeon_level == config.BOSS_LEVEL

def spawn_boss(dungeon, bosses, boss_name, tile_size):
    boss_data = bosses.get(boss_name)
    if not boss_data:
        print(f"Boss '{boss_name}' not found in bosses data.")
        return None  # Return None if boss data is missing

    boss_x, boss_y = dungeon.get_boss_room_position()
    boss_enemy = Enemy(boss_x, boss_y, boss_data, tile_size)
    print(f"Spawned boss: {boss_enemy}")

    return boss_enemy

