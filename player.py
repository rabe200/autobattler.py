# player.py

import json
import pygame
from config import TILE_SIZE, BLUE, SCREEN_WIDTH, SCREEN_HEIGHT
from animation_idle import IdleAnimation

PLAYER_DATA = None

def load_player_data(json_file="characters.json"):
    global PLAYER_DATA
    if PLAYER_DATA is None:
        with open(json_file, "r") as file:
            PLAYER_DATA = json.load(file)
    return PLAYER_DATA

class Player:
    def __init__(self, x, y, image_path, player_name, life, attack, armor, speed, gold=0, bonus_armor=0):
        super().__init__()
        self.equipment = []
        player_data = load_player_data()
        if player_name not in player_data:
            raise ValueError(f"Invalid player_name: {player_name}. Must be one of: {list(player_data.keys())}")

        player_info = player_data[player_name]
        self.name = player_info["name"]
        self.life = player_info["life"]
        self.attack = player_info["attack"]
        self.armor = player_info["armor"]
        self.speed = player_info["speed"]
        self.gold = gold
        self.max_life = player_info["life"]
        self.base_armor = self.armor
        self.bonus_armor = bonus_armor

        self.x, self.y = x, y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.color = BLUE
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.attacking = False
        self.last_position = (x, y)

        self.idle_animation = IdleAnimation(f"{player_name}-idle", target_height=TILE_SIZE)
        self.attack_animation = IdleAnimation(f"{player_name}-attack", target_height=TILE_SIZE)
        self.is_first_attack = True

    def start_attack(self):
        self.attacking = True
        self.attack_animation.current_frame = 0

    def update_attack(self):
        if self.attacking:
            self.attack_animation.update()
            if self.attack_animation.current_frame == len(self.attack_animation.frames) - 1:
                self.attacking = False

    def update_last_position(self):
        self.last_position = (self.x, self.y)

    def move(self, dx, dy):
        self.reset_armor()
        self.update_last_position()
        new_x = self.x + dx * TILE_SIZE
        new_y = self.y + dy * TILE_SIZE
        if 0 <= new_x < SCREEN_WIDTH:
            self.x = new_x
        if 0 <= new_y < SCREEN_HEIGHT:
            self.y = new_y

        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        if self.attacking:
            self.draw_attack_animation(screen)
        else:
            self.idle_animation.update()
            self.idle_animation.draw(screen, self.rect.topleft)

    def reset_to_idle(self):
        self.reset_armor()
        self.attacking = False

    def draw_idle_animation(self, screen):
        self.idle_animation.update()
        self.idle_animation.draw(screen, self.rect.topleft)

    def draw_attack_animation(self, screen):
        self.update_attack()
        attack_position = (self.rect.topleft[0], self.rect.topleft[1])
        self.attack_animation.draw(screen, attack_position)

    def check_room_collision(self, rooms):
        """Check if the player collides with any room."""
        for room in rooms:
            if self.rect.colliderect(room.rect):
                return room
        return None

    def add_equipment(self, item):
        """Add equipment to the player and update stats based on item properties."""
        self.equipment.append(item)  # Now this should work since equipment is initialized
        self.life += item.get("life", 0)
        self.attack += item.get("attack", 0)
        self.bonus_armor += item.get("armor", 0)
        self.armor += self.bonus_armor
        self.speed += item.get("speed", 0)


    def reset_armor(self):
        """Reset armor to base_armor + bonus_armor at the start of a fight."""
        self.armor = self.base_armor + self.bonus_armor

def reset_position(self):
        """Reset player position to the last saved coordinates."""
        self.x, self.y = 0, self.y
        self.rect.topleft = (self.x, self.y)
