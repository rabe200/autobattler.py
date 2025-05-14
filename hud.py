import pygame

from battleLogic import enemy_stats, player_stats
from config import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE


def draw_health_bar(screen, x, y, current_health, max_health, color, width=100, height=10):
    """Draw a health bar at a specific location with a given color and size."""
    health_ratio = max(0, current_health / max_health)
    pygame.draw.rect(screen, (128, 128, 128), (x, y, width, height))  # Background bar (gray)
    pygame.draw.rect(screen, color, (x, y, width * health_ratio, height))  # Health portion


def draw_hud(screen, player, dungeon, enemy=None):
    font = pygame.font.Font(None, 36)

    gold_text = font.render(f"Gold: {player.gold}", True, (255, 255, 0))
    screen.blit(gold_text, (20, 20))  # Position for gold display

    if dungeon is not None:
        level_text = font.render(f"Level: {dungeon.level}", True, (255, 255, 255))
        screen.blit(level_text, (20, 60))  # Position for level display
    else:
        level_text = font.render("Level: N/A", True, (255, 255, 255))
        screen.blit(level_text, (20, 60))


    player_name = player.name
    if player_name in player_stats:
        print("player_name in player_stats valid")
        adjusted_attack = player_stats[player_name]["base_attack"]
        adjusted_speed = player_stats[player_name]["base_speed"]
        adjusted_armor = player_stats[player_name]["base_armor"]
        adjusted_life = player_stats[player_name]["base_life"]

        player_text = font.render(
            f"{enemy.name} - Attack: {round(adjusted_attack)}, Speed: {round(adjusted_speed)}, Armor: {round(adjusted_armor)}, Life: {round(adjusted_life)}",
            True,
            (255, 0, 0)
        )
    else:
        player_text = font.render(
            f"{player.name} - Attack: {player.attack}, Speed: {player.speed}, Armor: {player.armor}, Life: {player.life}",
            True,
            (255, 0, 0)
        )
    screen.blit(player.image, (20, SCREEN_HEIGHT - player.image.get_height() - 20))
    screen.blit(player_text, (TILE_SIZE*2, SCREEN_HEIGHT - 160))

    draw_health_bar(
        screen,
        x= 20,  # Position
        y=SCREEN_HEIGHT - TILE_SIZE-36,  # Position
        current_health=player.life,
        max_health=player.max_life,
        color=(0, 255, 0),  # Green for player
        width=TILE_SIZE,
        height=15
    )

    if enemy:
        draw_health_bar(
            screen,
            x=enemy.x,  # Position
            y=SCREEN_HEIGHT - 520,  # Position
            current_health=enemy.life,
            max_health=enemy.max_life,
            color=(255, 0, 0),  # Red for enemy
            width=TILE_SIZE,
            height=15
        )

        enemy_name = enemy.name
        if enemy_name in enemy_stats:
            defeat_counter = enemy_stats[enemy_name]["defeat_counter"]
            adjusted_attack = enemy_stats[enemy_name]["base_attack"]
            adjusted_speed = enemy_stats[enemy_name]["base_speed"]
            adjusted_armor = enemy_stats[enemy_name]["base_armor"]
            adjusted_life = enemy_stats[enemy_name]["base_life"]

            enemy_text = font.render(
                f"{enemy.name} - Attack: {round(adjusted_attack)}, Speed: {round(adjusted_speed)}, Armor: {round(adjusted_armor)}, Life: {round(adjusted_life)}",
                True,
                (255, 0, 0)
            )
        else:
            enemy_text = font.render(
                f"{enemy.life}",
                True,
                (255, 0, 0)
            )

        # Render the enemy stats text and image
        screen.blit(enemy_text, (enemy.x, SCREEN_HEIGHT - 680))
        screen.blit(enemy.image, (SCREEN_WIDTH - 120, SCREEN_HEIGHT - 120))
