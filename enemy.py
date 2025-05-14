import json
import os
import random
import pygame
from animation_idle import IdleAnimation

ENEMY_DATA = None  # Global variable for enemy data

def load_enemy_data(json_file="enemies.json"):
    """Load enemy data from a JSON file."""
    global ENEMY_DATA
    if ENEMY_DATA is None:
        with open(json_file, "r") as file:
            ENEMY_DATA = json.load(file)
    return ENEMY_DATA

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_data, tile_size, sprite_folder="sprites/enemies"):
        super().__init__()

        # Initialize enemy attributes from the provided enemy data dictionary
        self.name = enemy_data["name"]
        self.life = enemy_data["life"]
        self.attack = enemy_data["attack"]
        self.armor = enemy_data["armor"]
        self.speed = enemy_data["speed"]
        self.level = enemy_data["level"]
        self.max_life = enemy_data["life"]
        self.initial_attack = self.attack  # Store initial attack to reset if needed
        self.defeat_counter = enemy_data.get("defeat-counter", 0)

        # Position and size attributes
        self.x, self.y = x, y
        self.rect = pygame.Rect(self.x, self.y, tile_size, tile_size)

        # Load animations dynamically using IdleAnimation based on the enemy's name
        self.idle_animation = IdleAnimation(f"{self.name}-idle", target_height=tile_size)
        self.attack_animation = IdleAnimation(f"{self.name}-attack", target_height=tile_size)

        # Load a static image for HUD display; use a default if not found
        image_path = f"{sprite_folder}/{self.name}-001.png"  # Define a path for static HUD image
        if os.path.isfile(image_path):
            self.image = pygame.image.load(image_path).convert_alpha()
        else:
            print(f"HUD image for '{self.name}' not found. Loading default HUD image.")
            self.image = pygame.image.load(f"{sprite_folder}/default-avatar.png").convert_alpha()

        # Scale the HUD image to the tile size (adjust as needed for HUD)
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))

        # Track attack state and animation offsets
        self.attacking = False
        self.flipped = False
        self.idle_offset = (0, 0)  # Offset for idle position

    def enter_fight(self):
        """Prepare the enemy for a fight by flipping animation if necessary."""
        if not self.flipped:
            self.flip_idle_animation()
            self.idle_offset = (-10, 0)  # Shift position left by 10 pixels (or adjust as desired)

    def start_attack(self):
        """Trigger the attack animation."""
        self.attacking = True
        self.attack_animation.current_frame = 0  # Reset to the first frame of the attack

    def update_attack(self):
        """Update attack animation and reset to idle after completion."""
        if self.attacking:
            self.attack_animation.update()
            if self.attack_animation.current_frame == len(self.attack_animation.frames) - 1:
                self.attacking = False  # Reset attacking state after animation completes

    def reset_stats(self):
        """Reset the enemy's stats to initial values for a new game."""
        self.attack = self.initial_attack

    def draw(self, screen):
        """Draw the enemy on the screen based on the current state (attacking or idle)."""
        if self.attacking:
            # Draw attack animation with the current attack position
            attack_position = (self.rect.topleft[0], self.rect.topleft[1])
            self.attack_animation.draw(screen, attack_position)
        else:
            # Draw idle animation with the idle offset position
            idle_position = (self.rect.topleft[0] + self.idle_offset[0], self.rect.topleft[1] + self.idle_offset[1])
            self.idle_animation.update()
            self.idle_animation.draw(screen, idle_position)

    def flip_idle_animation(self):
        """Flip the idle animation frames horizontally."""
        if not self.flipped:
            # Flip only the Surface part of each frame in the animation
            self.idle_animation.frames = [
                (pygame.transform.flip(frame[0], False, False), *frame[1:]) for frame in self.idle_animation.frames
            ]
            self.flipped = True
        else:
            # Unflip the frames back to their original state
            self.idle_animation.frames = [
                (pygame.transform.flip(frame[0], True, False), *frame[1:]) for frame in self.idle_animation.frames
            ]
            self.flipped = False

def create_random_enemy(x, y, tile_size, dungeon_level):
    """Create a random enemy using the global enemy data."""
    enemy_data = load_enemy_data()  # Ensure enemy data is loaded
    eligible_enemies = [
        enemy_type for enemy_type, data in enemy_data.items()
        if data["level"] <= dungeon_level
    ]

    if not eligible_enemies:
        raise ValueError(f"No eligible enemies found for dungeon level {dungeon_level}")

    enemy_type = random.choice(eligible_enemies)  # Pick a random enemy type
    return Enemy(x, y, ENEMY_DATA[enemy_type], tile_size)
