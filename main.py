# main.py
import pygame
import sys

from characters import characters
from dungeon import create_new_dungeon
from highscore import load_high_scores
from shop import shop
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, TILE_SIZE, BROWN, BLACK
from player import Player


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

            screen.blit(char_text, (100, 100 + i * 100))
            screen.blit(highscore_text, (100, 130 + i * 100))

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
        return "win"

    # Enemy attacks if still alive
    damage = max(0, enemy.attack - player.armor)
    player.life -= damage
    print(f"{enemy.name} attacks! Player armor: {player.armor}, health: {player.life}")

    if player.life <= 0:
        return "lose"

    return "continue"

def draw_hud(screen, player, enemy=None):
    font = pygame.font.Font(None, 36)
    player_stats_1 = f"HP: {player.life} AP: {player.attack}"
    player_stats_2 = f"DF: {player.armor} SP: {player.speed}"
    player_text_1 = font.render(player_stats_1, True, (255, 0, 0))
    player_text_2 = font.render(player_stats_2, True, (255, 0, 0))
    gold_text = font.render(f"Gold: {player.gold}", True, (255, 0, 0))

    screen.blit(player_text_1, (player.image.get_width() * 3 + 100, SCREEN_HEIGHT - 40))
    screen.blit(player_text_2, (player.image.get_width() * 3 + 100, SCREEN_HEIGHT - 80))
    screen.blit(gold_text, (player.image.get_width() * 2, 20))
    player_image_y = SCREEN_HEIGHT - player.image.get_height() * 2
    player_image = pygame.transform.scale(player.image, (TILE_SIZE * 2, TILE_SIZE * 2))
    screen.blit(player_image, (20, player_image_y))

    # Display enemy stats if in a battle
    if enemy:
        enemy_text = font.render(f"{enemy.name} - HP: {enemy.life} AP: {enemy.attack} DF: {enemy.armor}", True, (255, 0, 0))
        screen.blit(enemy_text, (SCREEN_WIDTH - 550, SCREEN_HEIGHT - 60))
        enemy_image = pygame.transform.scale(enemy.image, (TILE_SIZE * 2, TILE_SIZE * 2))
        screen.blit(enemy_image, (SCREEN_WIDTH - 120, SCREEN_HEIGHT - 120))

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
    # Set player starting position
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
    player.start_pos = dungeon.get_random_path_position()

    running = True
    in_battle, current_enemy, current_room, in_shop = False, None, None, False
    reveal_entrance = False

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
                        player.gold += current_enemy.attack  # Reward gold equivalent to enemy's attack power
                        current_room.has_enemy = False
                        current_room.enemy = None
                        current_room.color = BROWN  # Change room to path tile color
                        rooms_cleared += 1  # Increment cleared rooms
                        in_battle = False

                        # Reveal entrance if all rooms are cleared
                        if rooms_cleared == len(dungeon.rooms):
                            reveal_entrance = True

                    elif result == "lose":
                        print("Game Over!")
                        pygame.time.wait(2000)
                        main()  # Restart the game
                        if player.gold > high_scores[selected_character["name"]]:
                            high_scores[selected_character["name"]] = player.gold
                            save_high_scores(high_scores)
                elif event.key == pygame.K_ESCAPE and in_battle:
                    # Leave room without fighting
                    print("Left the room.")
                    in_battle = False
                    # Move player one step back to avoid re-triggering collision
                    player.x, player.y = last_position
                elif event.key == pygame.K_b and not in_battle:
                    in_shop = True

        if in_shop:
            shop(screen, player)
            in_shop = False

        # Check if player is in the entrance room to trigger new dungeon
        if reveal_entrance and dungeon.entrance_room and player.rect.colliderect(dungeon.entrance_room.rect):
            print("Entering new dungeon!")
            dungeon_level += 1
            dungeon = create_new_dungeon(dungeon_level)
            rooms_cleared = 0
            reveal_entrance = False
            start_pos = dungeon.get_random_path_position()
            player.x, player.y = start_pos

        keys = pygame.key.get_pressed()

        # Player movement on path tiles
        # Player movement on path tiles
        if not in_battle:
            dx, dy = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT], keys[pygame.K_DOWN] - keys[pygame.K_UP]
            new_x, new_y = player.x + dx * TILE_SIZE, player.y + dy * TILE_SIZE

            # Allow movement on both standard and newly revealed paths
            if any(path.collidepoint(new_x, new_y) for path in dungeon.paths) or (reveal_entrance and dungeon.entrance_path and any(path.collidepoint(new_x, new_y) for path in dungeon.entrance_path)):
                last_position = (player.x, player.y)  # Save the current position
                player.move(dx, dy)

            # Check for room collision
            collided_room = player.check_room_collision(dungeon.rooms)
            if collided_room and collided_room.has_enemy:
                current_enemy, current_room = collided_room.enemy, collided_room
                print(f"Encountered {current_enemy.name}. Press Enter to fight or Escape to leave.")
                in_battle = True


        # Draw the dungeon, player, HUD, and entrance room if revealed
        dungeon.draw(screen, reveal_entrance)
        player.draw(screen)
        draw_hud(screen, player, current_enemy if in_battle else None)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
