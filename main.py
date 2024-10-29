# main.py
from collections import defaultdict

import pygame
import sys

from characters import characters
from dungeon import create_new_dungeon
from highscore import load_high_scores, save_high_scores
from shop import shop
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, TILE_SIZE, BROWN, BLACK
from player import Player

enemy_defeats = defaultdict(int)

# Dictionary to track how many times each enemy type has been defeated
enemy_defeats = defaultdict(int)
enemy_initial_attack = {}  # Dictionary to store initial attack values if needed

def update_enemy_stats(enemy):
    """Increase attack power of an enemy type every 3 defeats."""
    enemy_defeats[enemy.name] += 1  # Increment the defeat count

    # Check if the defeat count has reached a multiple of 3
    if enemy_defeats[enemy.name] % 3 == 0:
        enemy.attack += 1  # Increase attack by 1
        print(f"{enemy.name} attack power increased by 1 to {enemy.attack}!")

    # Optionally, store the initial attack value to reset each game
    if enemy.name not in enemy_initial_attack:
        enemy_initial_attack[enemy.name] = enemy.attack  # Store initial attack

def reset_enemy_stats():
    """Reset enemy stats (attack power) at the start of a new game."""
    for enemy_name, initial_attack in enemy_initial_attack.items():
        enemy_defeats[enemy_name] = 0  # Reset defeat counter
        # Reset the attack value to its original value
        for enemy in enemy_name:  # Assuming a list of enemy objects or use `enemy_name`
            if enemy.name == enemy_name:
                enemy.attack = initial_attack

def select_character(screen):
    font = pygame.font.Font(None, 36)
    selected_index = 0
    # Load high scores and pass characters as an argument
    high_scores = load_high_scores(characters)

    while True:
        screen.fill((0, 0, 0))

        for i, char in enumerate(characters):
            color = (255, 255, 255) if i == selected_index else (100, 100, 100)
            char_text = font.render(f"{char['name']} - HP: {char['stats']['life']}, AP: {char['stats']['attack']}", True, color)
            highscore_text = font.render(f"High Score: {high_scores[char['name']]}", True, color)

            screen.blit(char_text, (200, 100 + i * 100))
            screen.blit(highscore_text, (200, 130 + i * 100))

            # Display character image
            char_image = pygame.image.load(char["image_path"]).convert_alpha()
            char_image = pygame.transform.scale(char_image, (TILE_SIZE * 2, TILE_SIZE * 2))
            screen.blit(char_image, (50, 100 + i * 100))

        instructions = font.render("Use UP/DOWN to select, ENTER to choose", True, (255, 255, 255))
        screen.blit(instructions, (100, SCREEN_HEIGHT - 60))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(characters)
                elif event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(characters)
                elif event.key == pygame.K_RETURN:
                    return characters[selected_index]

def step_back(player, dx, dy):
    """Move the player one step back to avoid re-colliding with the room."""
    player.move(-dx, -dy)


def battle(player, enemy):
    """Handle one round of battle."""
    damage = max(0, player.attack - enemy.armor)
    enemy.life -= damage
    print(f"Player attacks! {enemy.name} armor: {enemy.armor}, health: {enemy.life}")

    if enemy.life <= 0:
        enemy_defeats[enemy.name] += 1
        update_enemy_stats(enemy)
        print("defeated times: ", enemy_defeats[enemy.name])
        print("attack power", enemy.attack)
        return "win"

    # Enemy attacks if still alive
    damage = max(0, enemy.attack - player.armor)
    player.life -= damage
    print(f"{enemy.name} attacks! Player armor: {player.armor}, health: {player.life}")

    if player.life <= 0:
        return "lose"

    return "continue"

def draw_health_bar(screen, x, y, current_health, max_health, color, width=100, height=10):
    """Draw a health bar at a specific location with a given color and size."""
    health_ratio = max(0, current_health / max_health)
    pygame.draw.rect(screen, (128, 128, 128), (x, y, width, height))  # Background bar (gray)
    pygame.draw.rect(screen, color, (x, y, width * health_ratio, height))  # Health portion

def draw_hud(screen, player, enemy=None):
    font = pygame.font.Font(None, 36)
    player_stats = f"Gold: {player.gold}"
    gold_text = font.render(player_stats, True, (255, 255, 0))

    # Draw player stats
    screen.blit(gold_text, (20, 20))
    screen.blit(player.image, (20, SCREEN_HEIGHT - player.image.get_height() - 20))

    # Draw player health bar
    draw_health_bar(
        screen,
        x=player.image.get_width() * 3 + 100,  # Position
        y=SCREEN_HEIGHT - 100,  # Position
        current_health=player.life,
        max_health=player.max_life,
        color=(0, 255, 0),  # Green for player
        width=150,
        height=15
    )

    # If in battle, draw enemy health bar
    if enemy:
        draw_health_bar(
            screen,
            x=SCREEN_WIDTH - 250,  # Position
            y=SCREEN_HEIGHT - 120,  # Position
            current_health=enemy.life,
            max_health=enemy.max_life,
            color=(255, 0, 0),  # Red for enemy
            width=150,
            height=15
        )
        enemy_text = font.render(f"{enemy.name}", True, (255, 0, 0))
        screen.blit(enemy_text, (SCREEN_WIDTH - 250, SCREEN_HEIGHT - 140))
        screen.blit(enemy.image, (SCREEN_WIDTH - 120, SCREEN_HEIGHT - 120))


def game_over_screen(screen, player, chosen_character, high_scores):
    """Display the Game Over screen and handle high score display and restart."""
    font = pygame.font.Font(None, 74)
    font_small = pygame.font.Font(None, 36)
    display_scores = False

    # Check and update high score if necessary
    if player.gold > high_scores[chosen_character["name"]]:
        high_scores[chosen_character["name"]] = player.gold
        save_high_scores(high_scores)

    while True:
        screen.fill(BLACK)

        if not display_scores:
            # Display "Game Over" message
            game_over_text = font.render("Game Over", True, (255, 0, 0))
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100))

            instruction_text = font_small.render("Press Enter or Space to see High Scores", True, (255, 255, 255))
            screen.blit(instruction_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2))
        else:
            # Display High Scores
            title_text = font.render("High Scores", True, (255, 255, 255))
            screen.blit(title_text, (SCREEN_WIDTH // 2 - 100, 50))

            for idx, char in enumerate(characters):
                char_name = char["name"]
                score_text = font_small.render(f"{char_name}: {high_scores[char_name]}", True, (255, 255, 255))
                screen.blit(score_text, (SCREEN_WIDTH // 2 - 100, 150 + idx * 50))

            restart_text = font_small.render("Press Enter or Space to Restart", True, (255, 255, 255))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 60))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    if display_scores:
                        return  # Exit to restart the game
                    else:
                        display_scores = True  # Show high scores on the next screen

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Autobattler Roguelite 001")
    clock = pygame.time.Clock()

    chosen_character = select_character(screen)
    high_scores = load_high_scores(characters)
    dungeon_level, rooms_cleared = 1, 0
    dungeon = create_new_dungeon(dungeon_level)
    start_pos = dungeon.get_random_path_position()
    if not start_pos:
        print("No valid starting position found.")
        pygame.quit()
        sys.exit()

    player = Player(
        x=start_pos[0],
        y=start_pos[1],
        image_path=chosen_character["image_path"],
        life=chosen_character["stats"]["life"],
        attack=chosen_character["stats"]["attack"],
        armor=chosen_character["stats"]["armor"],
        speed=chosen_character["stats"]["speed"]
    )
    last_position = (player.x, player.y)
    running = True
    in_battle, current_enemy, current_room, in_shop = False, None, None, False
    reveal_entrance = False
    shop_visited = False
    while running:

        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and in_battle and current_enemy:
                    result = battle(player, current_enemy)
                    if result == "win":
                        print(f"{current_enemy.name} defeated!")
                        player.gold += current_enemy.attack
                        current_room.has_enemy = False
                        current_room.enemy = None
                        current_room.color = BROWN
                        rooms_cleared += 1
                        in_battle = False

                        if rooms_cleared == len(dungeon.rooms):
                            reveal_entrance = True

                    elif result == "lose":
                        game_over_screen(screen, player, chosen_character, high_scores)
                        main()  # Restart the game
                elif event.key == pygame.K_ESCAPE and in_battle:
                    in_battle = False
                    player.x, player.y = last_position
                elif event.key == pygame.K_b and not in_battle:
                    in_shop = True

        if in_shop:
            if not shop_visited:
                print("shop first visited")
                shop(screen,player,shop_visited=False)
                shop_visited=True
                in_shop = False
            else:
                shop(screen,player,shop_visited=True)
                print("shop visited before")
                in_shop = False

        if reveal_entrance and dungeon.entrance_room and player.rect.colliderect(dungeon.entrance_room.rect):
            dungeon_level += 1
            dungeon = create_new_dungeon(dungeon_level)
            rooms_cleared = 0
            reveal_entrance = False
            start_pos = dungeon.get_random_path_position()
            player.x, player.y = start_pos

        keys = pygame.key.get_pressed()

        if not in_battle:
            dx, dy = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT], keys[pygame.K_DOWN] - keys[pygame.K_UP]
            new_x, new_y = player.x + dx * TILE_SIZE, player.y + dy * TILE_SIZE

            if any(path.collidepoint(new_x, new_y) for path in dungeon.paths) or (reveal_entrance and dungeon.entrance_path and any(path.collidepoint(new_x, new_y) for path in dungeon.entrance_path)):
                last_position = (player.x, player.y)
                player.move(dx, dy)

            collided_room = player.check_room_collision(dungeon.rooms)
            if collided_room and collided_room.has_enemy:
                current_enemy, current_room = collided_room.enemy, collided_room
                in_battle = True

        dungeon.draw(screen, reveal_entrance)
        player.draw(screen)
        draw_hud(screen, player, current_enemy if in_battle else None)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()