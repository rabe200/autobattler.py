# player.py

import pygame
from config import TILE_SIZE, BLUE, SCREEN_WIDTH, SCREEN_HEIGHT

class Player:
    def __init__(self, x, y, image_path, life, attack, armor, speed, gold=0):
        super().__init__()
        self.name = "Werner"  # Default name; can be customized if needed
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))  # Scale to fit tile size
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.color = BLUE

        # Stats
        self.life = life
        self.attack = attack
        self.armor = armor
        self.speed = speed
        self.gold = gold
        self.equipment = []

    def add_equipment(self, item):
        self.equipment.append(item)
        self.life += item.get("life", 0)
        self.attack += item.get("attack", 0)
        self.armor += item.get("armor", 0)
        self.speed += item.get("speed", 0)

    def move(self, dx, dy):
        new_x = self.x + dx * TILE_SIZE
        new_y = self.y + dy * TILE_SIZE
        if 0 <= new_x < SCREEN_WIDTH:
            self.x = new_x
        if 0 <= new_y < SCREEN_HEIGHT:
            self.y = new_y

        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_room_collision(self, rooms):
        for room in rooms:
            if self.rect.colliderect(room.rect):
                return room
        return None
