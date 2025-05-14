# main.py

import pygame
import sys

import time

import boss_encounter
import config
from battleLogic import battle, reset_enemy_stats, apply_damage
from dungeon import create_new_dungeon
from highscore import load_high_scores, save_high_scores
from hud import draw_hud
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TILE_SIZE, BROWN, BLACK
from player import Player, load_player_data, reset_position
import chest

characters = load_player_data()


def select_character(screen):
    font = pygame.font.Font(None, 36)
    selected_index = 0
    high_scores = load_high_scores(characters)

    character_keys = list(characters.keys())  # Get a list of keys from the dictionary

    while True:
        screen.fill((0, 0, 0))

        for i, key in enumerate(character_keys):
            character = characters[key]
            is_selected = (i == selected_index)
            color = (255, 255, 255) if is_selected else (100, 100, 100)
            image_x = 50
            image_y = 100 + i * 150
            image_size = TILE_SIZE - 30

            if is_selected:
                pygame.draw.rect(screen, (255, 215, 0), (image_x - 5, image_y - 5, image_size + 10, image_size + 10), 3)

            stats = character["stats"] if "stats" in character else character
            character_text = font.render(
                f"{character['name']} - HP: {stats['life']}, AP: {stats['attack']}",
                True, color
            )
            highscore_text = font.render(
                f"High Score: {high_scores[character['name']]}",
                True, color
            )

            screen.blit(character_text, (200, 100 + i * 150))
            screen.blit(highscore_text, (200, 130 + i * 150))

            char_image = pygame.image.load(character["image_path"]).convert_alpha()
            char_image = pygame.transform.scale(char_image, (image_size, image_size))
            screen.blit(char_image, (image_x, image_y))

        instructions = font.render("Use UP/DOWN to select, ENTER to choose", True, (255, 255, 255))
        screen.blit(instructions, (100, SCREEN_HEIGHT - 60))

        # Update the display once per loop
        pygame.display.flip()

        # Event handling for input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(character_keys)
                elif event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(character_keys)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return characters[character_keys[selected_index]]


def game_over_screen(screen, player, chosen_character, high_scores):
    font = pygame.font.Font(None, 74)
    font_small = pygame.font.Font(None, 36)
    display_scores = False

    if player.gold > high_scores[chosen_character["name"]]:
        high_scores[chosen_character["name"]] = player.gold
        save_high_scores(high_scores)

    while True:
        screen.fill(BLACK)

        if not display_scores:
            game_over_text = font.render("You died", True, (255, 0, 0))
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100))
            instruction_text = font_small.render("Press Enter to continue", True, (255, 255, 255))
            screen.blit(instruction_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2))
        else:
            title_text = font.render("High Scores", True, (255, 255, 255))
            screen.blit(title_text, (SCREEN_WIDTH // 2 - 100, 50))

            for idx, (char_key, char_data) in enumerate(characters.items()):
                char_name = char_data["name"]
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
                        return
            else:
                display_scores = True

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Autobattler Roguelite 001")
    clock = pygame.time.Clock()
    reset_enemy_stats()
    chosen_character = select_character(screen)
    high_scores = load_high_scores(characters)
    dungeon_level, rooms_cleared = 1, 0
    dungeon_finished = False
    dungeon = create_new_dungeon(dungeon_level)
    bosses = boss_encounter.load_boss_data()
    start_pos = dungeon.get_start_pos()
    player = Player(
        x=start_pos[0],
        y=start_pos[1],
        image_path=chosen_character["image_path"],
        life=chosen_character["life"],
        attack=chosen_character["attack"],
        armor=chosen_character["armor"],
        speed=chosen_character["speed"],
        player_name=chosen_character["name"],
    )
    print(f"mainGameLoop, armor player: {player.armor} \n")
    boss_encounter_active = False

    in_battle, current_enemy, current_room, in_shop, in_chest_room = False, None, None, False, False
    battle_state = {"turn": None, "player_attacking": False, "enemy_attacking": False}

    running = True

    while running:
        screen.fill((0, 0, 0))

        # Check for Boss Level and setup
        # Check if the current level is the boss level
        if dungeon_level % config.BOSS_LEVEL == 0 and not boss_encounter_active:
            dungeon = create_new_dungeon(dungeon_level, is_boss_level=True)
            player.x, player.y = dungeon.get_start_pos()
            if dungeon.level <= config.BOSS_LEVEL:
                current_enemy = boss_encounter.spawn_boss(dungeon, bosses, config.BOSS_NAME, TILE_SIZE)
                print(f"level: {dungeon_level} - spawning{current_enemy}")
            else:
                current_enemy = boss_encounter.spawn_boss(dungeon, bosses, config.BOSS_NAME_2, TILE_SIZE)
                print(f"level: {dungeon_level} - spawning{current_enemy}")
            if current_enemy is None:
                print("Error: current_enemy is None after spawn_boss.")
            else:
                print(f"Boss spawned successfully: {current_enemy.name}")

            boss_encounter_active = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if in_battle and current_enemy and not battle_state["player_attacking"] and not battle_state["enemy_attacking"]:
                        battle_state = battle(player, current_enemy)
                    else:
                        print("space key pressed")
                elif event.key == pygame.K_ESCAPE and in_battle:
                    in_battle = False
                    reset_position(player)


        # Battle Logic and Animation
        if in_battle:
            if battle_state["turn"] == "player" and not battle_state["player_attacking"]:
                player.start_attack()
                battle_state["player_attacking"] = True

            if player.attacking:
                player.update_attack()
            else:
                if battle_state["player_attacking"]:
                    apply_damage(current_enemy, player.attack)
                    print(f"Player attacks! {current_enemy.name} armor: {current_enemy.armor}, health: {current_enemy.life}")
                    if current_enemy.life <= 0:
                        player.gold += current_enemy.attack
                        current_room.has_enemy = False
                        current_room.enemy = None
                        current_room.color = BROWN
                        rooms_cleared += 1
                        in_battle = False
                        player.reset_to_idle()
                        print("Enemy defeated!")
                        player.x += TILE_SIZE * 2
                        player.rect.topleft = (player.x, player.y)
                    if rooms_cleared == len(dungeon.rooms):
                        dungeon_finished = True
                    if current_enemy.life > 0:
                        battle_state["player_attacking"] = False
                        battle_state["turn"] = "enemy"

            if battle_state["turn"] == "enemy" and not battle_state["enemy_attacking"]:
                current_enemy.start_attack()
                battle_state["enemy_attacking"] = True
            if current_enemy.attacking:
                current_enemy.update_attack()
            else:
                if battle_state["enemy_attacking"]:
                    apply_damage(player, current_enemy.attack)
                    print(f"{current_enemy.name} attacks! Player armor: {player.armor}, health: {player.life}")
                    if player.life <= 0:
                        print("Player defeated!")
                        game_over_screen(screen, player, chosen_character, high_scores)
                        main()
                    battle_state["enemy_attacking"] = False
                    battle_state["turn"] = "player"

        # Handle end of boss encounter
        if boss_encounter_active and not in_battle and current_enemy and current_enemy.life <= 0:
            current_enemy = None
            print("Boss defeated!")
            boss_encounter_active = False
            dungeon = create_new_dungeon(dungeon_level)
            player.x, player.y = dungeon.get_start_pos()

        # Check for shop visit
        if in_chest_room:
            in__chest_room = chest.chest(screen, player)

        # Dungeon transition
        if dungeon_finished:
            in_battle = False
            dungeon_level += 1
            dungeon = create_new_dungeon(dungeon_level)
            rooms_cleared = 0
            start_pos = dungeon.get_start_pos()
            player.x, player.y = start_pos
            dungeon_finished = False
            pygame.event.clear()
            time.sleep(0.1)
        # Chest room logic
        if in_chest_room:
            in_chest_room = False
            rooms_cleared += 1
            if rooms_cleared == len(dungeon.rooms):
                dungeon_finished = True

        keys = pygame.key.get_pressed()

        if not in_battle and not in_chest_room:
            dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d] or keys[pygame.K_SPACE]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
            dy = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])
            new_x, new_y = player.x + dx * TILE_SIZE, player.y + dy * TILE_SIZE

            if any(path.collidepoint(new_x, new_y) for path in dungeon.paths):
                player.move(dx, dy)

            collided_room = player.check_room_collision(dungeon.rooms)
            if collided_room and collided_room.has_enemy and not in_battle and dungeon.level % config.BOSS_LEVEL != 0:
                print(current_enemy, collided_room.enemy)
                current_enemy, current_room = collided_room.enemy, collided_room
                print(current_enemy, collided_room.enemy)
                current_enemy.enter_fight()
                in_battle = True
                battle_state = {"turn": "player" if player.speed > current_enemy.speed else "enemy",
                                "player_attacking": False, "enemy_attacking": False}
                player.x -= TILE_SIZE
                player.rect.topleft = (player.x, player.y)
            elif collided_room and collided_room.has_enemy and not in_battle and dungeon_level % config.BOSS_LEVEL == 0:
                print(current_enemy.name)
                current_enemy.enter_fight()
                in_battle = True
                battle_state = {"turn": "player" if player.speed > current_enemy.speed else "enemy",
                                "player_attacking": False, "enemy_attacking": False}
                player.x -= TILE_SIZE
                player.rect.topleft = (player.x, player.y)

            elif collided_room and collided_room.room_type == "chest" and not collided_room.has_looted:
                print("Entered chest room")
                collided_room.has_looted = True
                in_chest_room = True

        # Draw everything
        dungeon.draw(screen)
        player.draw(screen)
        if current_enemy:
            current_enemy.draw(screen)
        draw_hud(screen, player, dungeon, current_enemy if in_battle else None)
        pygame.display.flip()

        clock.tick(FPS)

if __name__ == "__main__":
    main()