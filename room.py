# room.py

import pygame
from config import TILE_SIZE, RED, GREEN
from enemy import Enemy, load_enemy_data

class Room:
    def __init__(self, x, y, has_enemy=True):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.has_enemy = has_enemy
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = RED if self.has_enemy else GREEN

        # Set up an enemy if the room has one
        if self.has_enemy:
            enemy_type = "wolf"  # Ensure this is a valid type from enemy_data
            self.enemy = Enemy(self.x, self.y, enemy_type, TILE_SIZE)
        else:
            self.enemy = None

    def draw(self, screen):
        # Draw the room itself
        pygame.draw.rect(screen, self.color, self.rect)
        # Draw the enemy if it exists
        if self.enemy:
            self.enemy.draw(screen)
