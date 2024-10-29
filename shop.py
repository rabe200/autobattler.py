# shop.py

import json
import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE


def draw_shop(screen, items, player, selected_index):
    """Draw the shop interface with item list, player gold, and instructions."""
    screen.fill((200, 200, 200))
    font = pygame.font.Font(None, 36)
    title = font.render("Shop - Buy Items", True, (0, 0, 0))
    screen.blit(title, (20, 20))
    gold_text = font.render(f"Your Gold: {player.gold}", True, (0, 0, 0))
    screen.blit(gold_text, (20, 60))

    for index, item in enumerate(items):
        color = (0, 255, 0) if index == selected_index else (0, 0, 0)
        item_text = font.render(f"{item['name']} - {item['cost']} Gold", True, color)
        effects_text = font.render(
            f"Effects: +{item.get('life', 0)} Life, +{item.get('attack', 0)} Attack, +{item.get('armor', 0)} Armor, +{item.get('speed', 0)} Speed",
            True, color
        )
        screen.blit(item_text, (20, 100 + index * 60))
        screen.blit(effects_text, (20, 130 + index * 60))

    instructions = font.render("UP/DOWN to navigate, ENTER to buy, ESC to exit", True, (0, 0, 0))
    screen.blit(instructions, (20, SCREEN_HEIGHT - 40))
    pygame.display.flip()

def load_shop_items():
    """Load items from a JSON file."""
    with open("shop_items.json") as file:
        return json.load(file)

def draw_shop_image(screen):
    """Draw the shop image in the bottom right corner."""
    chest_image = pygame.image.load("sprites/chest.webp")
    chest_image = pygame.transform.scale(chest_image, (TILE_SIZE * 2, TILE_SIZE * 2))
    screen.blit(chest_image, (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100))
    pygame.display.flip()

def shop(screen, player):
    """Main shop function to handle buying items and keeping shop open until ESCAPE is pressed."""
    items = load_shop_items()
    if not items:
        print("The shop is currently empty.")
        return

    selected_index = 0
    running = True

    while running:
        draw_shop(screen, items, player, selected_index)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_b:
                    running = False
                elif event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(items)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(items)
                elif event.key == pygame.K_RETURN:
                    item = items[selected_index]
                    if player.gold >= item["cost"]:
                        player.gold -= item["cost"]
                        player.add_equipment(item)
                        print(f"Bought {item['name']}!")
                    else:
                        print("Not enough gold.")
