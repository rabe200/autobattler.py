# battlelogic.py

import random

# Globals for tracking enemy encounters and persistent stats
encountered_enemy_types = set()
enemy_stats = {}
player_stats = {}
def reset_enemy_stats():
    """Reset global dictionaries and sets for a new game."""
    global encountered_enemy_types, enemy_stats
    encountered_enemy_types.clear()
    enemy_stats.clear()

def determine_turn_order(player, enemy):
    """Determine who starts the battle based on speed."""
    enemy_name = enemy.name
    if enemy_name in enemy_stats:
        enemy_speed = enemy_stats[enemy_name]["base_speed"]
    else:
        enemy_speed = enemy.speed
    print(f"{enemy.name} Speed: {enemy_speed}, Player Speed: {player.speed}")
    if player.speed > enemy_speed:
        print("Player starts the battle!")
        return "player"
    elif player.speed < enemy_speed:
        print(f"{enemy.name} starts the battle!")
        return "enemy"
    else:
        return "player" if random.choice([True, False]) else "enemy"

def apply_damage(target, damage):
    """Apply damage to armor first, then to health if armor is depleted."""
    print(f"stats before apply_damage(on {target.name}): life {target.life} armor: {target.armor}")
    if target.armor > 0:
        if damage >= target.armor:
            damage -= target.armor
            target.armor = 0
            target.life -= damage
            print(f"stats after apply_damage(on {target.name} with damage of {damage}]): life {target.life} armor: {target.armor}")
        else:
            target.armor -= damage
    else:
        target.life -= damage


def battle(player, enemy):
    global encountered_enemy_types, enemy_stats, player_stats
    if enemy.name not in encountered_enemy_types:
        print(f"First encounter with enemy: {enemy.name}")
        encountered_enemy_types.add(enemy.name)
        enemy_stats[enemy.name] = {
            "defeat_counter": 0,
            "base_attack": enemy.attack,
            "base_speed": enemy.speed,
            "base_armor": enemy.armor,
            "base_life": enemy.life
        }

        player_stats[player.name] = {
            "defeat_counter": 0,
            "base_attack": player.attack,
            "base_speed": player.speed,
            "base_armor": player.armor,
            "base_life": player.life
        }

    # Reset enemy armor at the beginning of each battle
    enemy.armor = enemy_stats[enemy.name]["base_armor"]

    # Determine turn order
    turn = determine_turn_order(player, enemy)

    return {"turn": turn, "player_attacking": False, "enemy_attacking": False}
