# enemy.py
import json
import random
import pygame

ENEMY_DATA = None  # Global variable for enemy data

def load_enemy_data(json_file="enemies.json"):
    """Load enemy data from a JSON file."""
    global ENEMY_DATA
    if ENEMY_DATA is None:
        with open(json_file, "r") as file:
            ENEMY_DATA = json.load(file)
    return ENEMY_DATA

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type, tile_size):
        super().__init__()
        enemy_data = load_enemy_data()  # Ensure enemy data is loaded

        if enemy_type not in enemy_data:
            raise ValueError(f"Invalid enemy_type: {enemy_type}. Must be one of: {list(enemy_data.keys())}")

        # Initialize enemy attributes from the loaded enemy data
        self.name = enemy_data[enemy_type]["name"]
        self.life = enemy_data[enemy_type]["life"]
        self.attack = enemy_data[enemy_type]["attack"]
        self.armor = enemy_data[enemy_type]["armor"]
        self.speed = enemy_data[enemy_type]["speed"]
        self.level = enemy_data[enemy_type]["level"]
        # Load the image from the path in the enemy data
        image_path = enemy_data[enemy_type]["image_path"]
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))  # Scale image to tile size
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        """Draw the enemy on the screen."""
        screen.blit(self.image, self.rect)


def create_random_enemy(x, y, tile_size, dungeon_level):
    """Create a random enemy using the global enemy data."""
    enemy_data = load_enemy_data()  # Ensure enemy data is loaded
    eligible_enemies = [
        enemy_type for enemy_type, data in enemy_data.items()
        if data["level"] <= dungeon_level
    ]

    if not eligible_enemies:
        raise ValueError(f"no eligible enemies fround for dungeon level {dungeon_level}")

    enemy_type = random.choice(eligible_enemies)  # Pick a random enemy type
    return Enemy(x, y, enemy_type, tile_size)
