import random
import pygame

from enemy import create_random_enemy
from room import Room
from config import TILE_SIZE, SCREEN_WIDTH, BROWN, ENEMY_NUMBER, HOUSE_NUMBER, STAIRS_NUMBER, CHEST_NUMBER


class Dungeon:
    def __init__(self, level=1, row_y=TILE_SIZE, is_boss_level=False):
        self.level = level
        self.row_y = row_y  # Fixed row position
        self.paths = []
        self.rooms = []

        if is_boss_level:
            self.create_boss_row()  # Create a boss level layout
        else:
            self.create_row()  # Create a regular dungeon row

    def create_row(self):
        """Create a horizontal row of path tiles from left to right for a regular dungeon."""
        path_x = 0
        first_path = pygame.Rect(path_x, self.row_y, TILE_SIZE, TILE_SIZE)
        self.paths.append(first_path)
        path_x += TILE_SIZE

        enemy_number = ENEMY_NUMBER
        house_number = HOUSE_NUMBER
        stairs_number = STAIRS_NUMBER
        chest_number = CHEST_NUMBER

        while path_x < SCREEN_WIDTH:
            if enemy_number > 0:
                enemy_number -= 1
                path_rect = pygame.Rect(path_x, self.row_y, TILE_SIZE, TILE_SIZE)
                self.paths.append(path_rect)
                room = Room(path_x, self.row_y, has_enemy=True, room_type="enemy")
                room.enemy = create_random_enemy(path_x, self.row_y, TILE_SIZE, self.level)
                self.rooms.append(room)
            elif house_number > 0:
                house_number -= 1
                path_rect = pygame.Rect(path_x, self.row_y, TILE_SIZE, TILE_SIZE)
                self.paths.append(path_rect)
                room = Room(path_x, self.row_y, has_enemy=False, room_type="house")
                self.rooms.append(room)
            elif stairs_number > 0:
                stairs_number -= 1
                path_rect = pygame.Rect(path_x, self.row_y, TILE_SIZE, TILE_SIZE)
                self.paths.append(path_rect)
                room = Room(path_x, self.row_y, has_enemy=False, room_type="stairs")
                self.rooms.append(room)
            elif chest_number > 0:
                chest_number -= 1
                path_rect = pygame.Rect(path_x, self.row_y, TILE_SIZE, TILE_SIZE)
                self.paths.append(path_rect)
                room = Room(path_x, self.row_y, has_enemy=False, room_type="chest")
                self.rooms.append(room)
            path_x += TILE_SIZE

    def create_boss_row(self):
        """Create a simplified dungeon row for a boss encounter."""
        path_x = 0
        for i in range(5):  # Add 4 regular path tiles
            path_rect = pygame.Rect(path_x, self.row_y, TILE_SIZE, TILE_SIZE)
            self.paths.append(path_rect)
            path_x += TILE_SIZE

        # Create the boss room at the end of the path
        boss_room_rect = pygame.Rect(path_x, self.row_y, TILE_SIZE, TILE_SIZE)
        self.paths.append(boss_room_rect)
        boss_room = Room(path_x, self.row_y, has_enemy=True, room_type="boss")
        self.rooms.append(boss_room)

    def draw(self, screen):
        for path in self.paths:
            pygame.draw.rect(screen, BROWN, path)
        for room in self.rooms:
            room.draw(screen)

    def get_start_pos(self):
        if self.paths:
            start_room = self.paths[0]
            return start_room.x, start_room.y
        else:
            print("No rooms available for start position.")
            return None

    def get_boss_room_position(self):
        """Get the position of the boss room."""
        if self.rooms and self.rooms[-1].room_type == "boss":
            return self.rooms[-1].rect.topleft
        return None


def create_new_dungeon(dungeon_level, is_boss_level=False):
    """Factory function to create a new dungeon, optionally a boss level."""
    return Dungeon(level=dungeon_level, is_boss_level=is_boss_level)
