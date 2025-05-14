# chest.py

import json
import random
import pygame
import sys

def load_items():
    """Load items from the JSON file."""
    with open("chest_items.json") as file:
        items = json.load(file)
    return items

def draw_chest(screen, itemstock, player, selected_index):
    """Draw the chest interface with three randomly selected items."""
    screen.fill((200, 200, 200))
    font = pygame.font.Font(None, 36)
    title = font.render("Chest - Choose an Item", True, (0, 0, 0))
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

def chest(screen, player):
    items = load_items()
    itemstock = random.sample(items, 3)
    selected_index = 0
    running = True

    while running:
        draw_chest(screen, itemstock, player, selected_index)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_UP:
                    # %len(itemstock) sorgt dafür, dass selected index zu keiner zeit kleiner null oder groeßer len(itemstock) ist
                    selected_index = (selected_index - 1) % len(itemstock)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(itemstock)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    item = itemstock[selected_index]
                    player.add_equipment(item)
                    print(f"Added item: {item}")
                    running = False
                    return False