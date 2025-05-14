# room.py

import pygame
from animation_idle import IdleAnimation
from config import TILE_SIZE, BROWN
from enemy import Enemy, load_enemy_data

class Room:
    def __init__(self, x, y, has_enemy=False, room_type="enemy"):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.has_enemy = has_enemy
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.room_type = room_type
        self.color = BROWN
        self.enemy = None
        self.has_looted = False

        # Initialize room-specific animations based on room type
        self.idle_animation = None
        self._initialize_room_type()
        if has_enemy and room_type == "enemy":
            self._initialize_enemy()

    def _initialize_room_type(self):
        """Set up animations or other properties based on room type."""
        if self.room_type == "house":
            self.idle_animation = IdleAnimation("house", target_height=TILE_SIZE)
            print("Initialized house animation")
        elif self.room_type == "stairs":
            self.idle_animation = IdleAnimation("stairs", target_height=TILE_SIZE)
            print("Initialized stairs animation")
        elif self.room_type == "chest":
            self.idle_animation = IdleAnimation("chest", target_height=TILE_SIZE)
            print("Initialized chest animation")
        else:
            self.idle_animation = None

    def _initialize_enemy(self):
        """Set up an enemy if the room has one and it is an enemy room."""
        enemy_data = load_enemy_data()
        enemy_type = "wolf"  # Define the enemy type, or choose based on room properties
        if enemy_type in enemy_data:
            self.enemy = Enemy(self.x, self.y, enemy_data[enemy_type], TILE_SIZE)
            print("Initialized enemy:", self.enemy)
        else:
            print(f"Warning: Enemy type '{enemy_type}' not found in enemy data.")

    def draw(self, screen):
        # Draw the room itself
        pygame.draw.rect(screen, self.color, self.rect)

        # Draw room-specific animations
        if self.idle_animation:
            self.idle_animation.update()
            self.idle_animation.draw(screen, self.rect.topleft)

        # Draw the enemy if it exists
        if self.enemy:
            self.enemy.draw(screen)
