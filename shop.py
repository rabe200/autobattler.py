# chest.py

import json
import random
import pygame
import sys

from chest import chest

#paths for shop and chest json
SHOP_ITEMS_PATH = "shop_items.json"
CHEST_ITEMS_PATH = "chest_items.json"

def load_items(file_path):
    with open(file_path) as file:
        items = json.load(file)
    return items

def save_items(items, file_path):
    with open(file_path, "w") as file:
        json.dump(items, file, indent=4)

class Shop:
    def __init__(self):
        self.items = load_items(SHOP_ITEMS_PATH)

    def add_item(self, item_name):
        chest_items = load_items(CHEST_ITEMS_PATH)

        for item in self.items:
            if item["name"] == item_name and item["unlocked"]:
                if not any(chest_item["name"] == item_name for chest_item in chest_items):
                    chest_item = {
                        "name": item["name"],
                        "cost": item["initial_cost"],
                        "life": item["life"],
                        "attack": item["attack"],
                        "armor": item["armor"],
                        "speed": item["speed"],
                        "purchase_count": 0
                    }
                    chest_items.append(chest_item)
                    save_items(chest_items, CHEST_ITEMS_PATH)
                    print(f"Item '{item_name}' added to chests for future runs.")
                else:
                    print(f"Item '{item_name}' is already in chest items")
                break

    def unlock_item(self, item_name, player):
        unlockable_items =



def draw_shop(screen, itemstock, player, selected_index):
    """Draw the chest interface with three randomly selected items."""
    screen.fill((200, 200, 200))
    font = pygame.font.Font(None, 36)
    title = font.render("shop - unlock an Item", True, (0, 0, 0))
    screen.blit(title, (20, 20))
    gold_text = font.render(f"Your Gold: {player.gold}", True, (0, 0, 0))
    screen.blit(gold_text, (20, 60))

    for index, item in enumerate(itemstock):
        color = (0, 255, 0) if index == selected_index else (0, 0, 0)
        item_text = font.render(f"{item['name']} - {item['cost']} Gold", True, color)
        effects_text = font.render(
            f"Effects: +{item.get('life', 0)} Life, +{item.get('attack', 0)} Attack, "
            f"+{item.get('armor', 0)} Armor, +{item.get('speed', 0)} Speed",
            True, color
        )
        screen.blit(item_text, (20, 100 + index * 60))
        screen.blit(effects_text, (20, 130 + index * 60))

    instructions = font.render("UP/DOWN to navigate, ENTER to select, ESC to exit", True, (0, 0, 0))
    screen.blit(instructions, (20, screen.get_height() - 40))
    pygame.display.flip()

def shop(screen, player):
    """Main chest function to display items and handle selection."""
    items = load_items()
    itemstock = random.sample(items, 3)
    selected_index = 0
    running = True

    while running:
        draw_shop(screen, itemstock, player, selected_index)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(itemstock)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(itemstock)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    item = itemstock[selected_index]
                    player.add_equipment(item)
                    print(f"Added item: {item}")
                    running = False
                    return False  # Close chest and mark as looted
