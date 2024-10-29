# auto_navigation.py

import random
import pygame

from config import TILE_SIZE

visited_positions = {}  # Dictionary to track how many times each position has been visited
movement_history = []  # List to keep track of the player's path and directions
first_cleared_room = None  # Track the first cleared room

def automated_navigation(player, dungeon, screen, clock, delay=100):
    """
    Navigate the player along a snake-like path, ensuring all tiles are visited at least once.
    Change the color of a tile to black if it is visited more than once.

    Args:
        player: The player object.
        dungeon: The dungeon object containing paths and rooms.
        screen: The Pygame screen object to draw on.
        clock: The Pygame clock to control the frame rate.
        delay: Delay time in milliseconds for visible backtracking.
    """
    global visited_positions, movement_history, first_cleared_room

    current_x, current_y = player.x, player.y
    # Update the visit count for the current position
    visited_positions[(current_x, current_y)] = visited_positions.get((current_x, current_y), 0) + 1

    # Track the first cleared room
    if first_cleared_room is None:
        first_cleared_room = (current_x, current_y)
        print(f"First cleared room set at: {first_cleared_room}")

    # Define possible directions for movement: right, left, down, up
    directions = [
        ((TILE_SIZE, 0), "right"),   # Right
        ((-TILE_SIZE, 0), "left"),   # Left
        ((0, TILE_SIZE), "down"),    # Down
        ((0, -TILE_SIZE), "up")      # Up
    ]

    # Shuffle directions to add some randomness
    random.shuffle(directions)

    # Try moving in each direction
    for (dx, dy), direction_name in directions:
        next_x = current_x + dx
        next_y = current_y + dy

        # Check if the next tile is a valid path and has not been visited
        if any(path.collidepoint(next_x, next_y) for path in dungeon.paths) and (next_x, next_y) not in visited_positions:
            # Move the player to this position
            player.move(dx // TILE_SIZE, dy // TILE_SIZE)
            movement_history.append(((current_x, current_y), direction_name))  # Save the move and direction
            visited_positions[(player.x, player.y)] = visited_positions.get((player.x, player.y), 0) + 1
            print(f"Moving {direction_name} to ({player.x}, {player.y})")
            return

    # If no valid moves, backtrack
    if movement_history:
        # Pop the last move from the history and reverse the direction
        last_position, last_direction = movement_history.pop()
        reverse_direction = {
            "right": (-TILE_SIZE, 0),
            "left": (TILE_SIZE, 0),
            "down": (0, -TILE_SIZE),
            "up": (0, TILE_SIZE)
        }

        dx, dy = reverse_direction[last_direction]
        player.x, player.y = last_position  # Move back to the last position

        if player.gold > 0:
            player.gold -= 1
            print(f"gold decreasted to {player.gold} for backtracking")

        # Draw the backtracking movement on the screen
        screen.fill((255, 255, 255))  # Clear the screen
        dungeon.draw(screen)  # Draw the dungeon
        player.draw(screen)   # Draw the player
        draw_visited_tiles(screen)  # Draw the visited tiles with updated colors
        pygame.display.flip()  # Update the display

        pygame.time.wait(delay)
        clock.tick(60)  # Maintain the frame rate

        # Try the opposite direction after backtracking
        new_x = player.x + dx
        new_y = player.y + dy
        if (new_x, new_y) not in visited_positions and any(path.collidepoint(new_x, new_y) for path in dungeon.paths):
            player.move(dx // TILE_SIZE, dy // TILE_SIZE)
            movement_history.append(((player.x, player.y), last_direction))
            visited_positions[(player.x, player.y)] = visited_positions.get((player.x, player.y), 0) + 1
            print(f"Backtracked to ({player.x}, {player.y}), now trying {last_direction}")
    else:
        print("No moves left in history. All paths may have been visited.")

def draw_visited_tiles(screen):
    """
    Draw the tiles on the screen based on the number of visits.
    """
    for (x, y), visit_count in visited_positions.items():
        if visit_count > 1:
            pygame.draw.rect(screen, (0, 0, 0), (x, y, TILE_SIZE, TILE_SIZE))  # Draw black for tiles visited more than once
        else:
            pygame.draw.rect(screen, (100, 100, 100), (x, y, TILE_SIZE, TILE_SIZE))  # Draw grey for tiles visited once
