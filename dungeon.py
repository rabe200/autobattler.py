# dungeon.py

import random
import pygame

import player
from auto_navigation import visited_positions
from enemy import create_random_enemy
from room import Room
from config import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, BROWN, INITIAL_ROOM_COUNT, ROOM_INCREMENT_PER_LEVEL

class Dungeon:
    def __init__(self, level=1):
        self.level = level
        self.rooms = []
        self.paths = []
        self.entrance_room = None
        self.entrance_path = []
        self.generate_dungeon()

    def generate_dungeon(self):
        """Generate rooms and connect them with paths."""
        num_rooms = INITIAL_ROOM_COUNT + (self.level - 1) * ROOM_INCREMENT_PER_LEVEL
        current_x = random.randint(2, (SCREEN_WIDTH // TILE_SIZE) - 2) * TILE_SIZE
        current_y = random.randint(1, (SCREEN_HEIGHT // TILE_SIZE) - 4) * TILE_SIZE
        last_vertical = False
        visited_positions = set()
        visited_positions.add((current_x, current_y))

        for i in range(num_rooms):
            # Create room with an enemy
            room = Room(current_x, current_y, has_enemy=True)
            room.enemy = create_random_enemy(current_x, current_y, TILE_SIZE,self.level)
            self.rooms.append(room)

            retries = 0
            while retries < 10:
                # Alternate between vertical and horizontal positioning
                if last_vertical:
                    new_x = current_x + random.choice([-2, 2]) * TILE_SIZE
                    new_y = current_y
                else:
                    new_x = current_x
                    new_y = current_y + random.choice([-2, 2]) * TILE_SIZE
                    new_y = max(TILE_SIZE, min(new_y, SCREEN_HEIGHT - TILE_SIZE * 3))

                last_vertical = not last_vertical

                # Check if the new position is valid and unvisited
                if (new_x, new_y) not in visited_positions and TILE_SIZE <= new_x < SCREEN_WIDTH - TILE_SIZE and TILE_SIZE <= new_y < SCREEN_HEIGHT - TILE_SIZE:
                    visited_positions.add((new_x, new_y))
                    break
                retries += 1

            if retries >= 10:
                print(f"Could not find a valid position for room {i + 2}. Stopping generation.")
                break

            self.add_path(room, new_x, new_y)
            current_x, current_y = new_x, new_y

        # After creating all regular rooms, create the hidden entrance room
        self.create_hidden_entrance_room()

        print(f"Total rooms generated: {len(self.rooms)}. Total paths: {len(self.paths)}.")

    def add_path(self, from_room, to_x, to_y):
        current_x, current_y = from_room.x, from_room.y
        self.paths.append(pygame.Rect(current_x, current_y, TILE_SIZE, TILE_SIZE))

        while current_x != to_x:
            current_x += TILE_SIZE if to_x > current_x else -TILE_SIZE
            self.paths.append(pygame.Rect(current_x, current_y, TILE_SIZE, TILE_SIZE))

        while current_y != to_y:
            current_y += TILE_SIZE if to_y > current_y else -TILE_SIZE
            self.paths.append(pygame.Rect(current_x, current_y, TILE_SIZE, TILE_SIZE))

    def draw(self, screen, reveal_entrance=False):
        # Draw paths
        for path in self.paths:
            pygame.draw.rect(screen, BROWN, path)

        # Draw rooms and enemies within them
        for room in self.rooms:
            room.draw(screen)

        if reveal_entrance and self.entrance_room:
            for path in self.entrance_path:
                pygame.draw.rect(screen, BROWN, path)
            self.entrance_room.draw(screen)

    def get_random_path_position(self):
        available_paths = [path for path in self.paths if not any(room.rect.colliderect(path) for room in self.rooms)]
        if available_paths:
            path = random.choice(available_paths)
            return path.x, path.y
        return None

    def create_hidden_entrance_room(self):
        """Create an entrance room with a hidden path to it, within defined viewport boundaries."""
        last_room = self.rooms[-1]  # Start from the last room in the list
        num_path_tiles = random.randint(1, 8)
        current_x, current_y = last_room.x, last_room.y

        # Create the path leading to the entrance room
        for _ in range(num_path_tiles):
            direction = random.choice(["up", "down", "left", "right"])
            if direction == "up" and current_y > TILE_SIZE:
                current_y -= TILE_SIZE
            elif direction == "down" and current_y < SCREEN_HEIGHT - TILE_SIZE * 3:
                current_y += TILE_SIZE
            elif direction == "left" and current_x > TILE_SIZE:
                current_x -= TILE_SIZE
            elif direction == "right" and current_x < SCREEN_WIDTH - TILE_SIZE:
                current_x += TILE_SIZE
            self.entrance_path.append(pygame.Rect(current_x, current_y, TILE_SIZE, TILE_SIZE))

        # Create the entrance room at the end of the path, ensuring it's within bounds
        entrance_x = max(TILE_SIZE, min(current_x, SCREEN_WIDTH - TILE_SIZE * 2))
        entrance_y = max(TILE_SIZE, min(current_y, SCREEN_HEIGHT - TILE_SIZE * 3))
        self.entrance_room = Room(entrance_x, entrance_y, has_enemy=False)
        self.entrance_room.color = (0, 0, 255)  # Unique color to represent the entrance room

# Function to create a new dungeon with increasing rooms
def create_new_dungeon(dungeon_level):
    visited_positions.clear()
    dungeon = Dungeon(level=dungeon_level)
    return dungeon
