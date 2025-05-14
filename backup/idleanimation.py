# animation_idle.py

import pygame
import json
import os

class IdleAnimation:
    def __init__(self, name, target_height=None, spritesheet_folder="sprites/spriteSheets"):
        """Initialize the animation with dynamically loaded spritesheet and JSON data."""
        self.frames = []
        self.target_height = target_height
        self.name = name
        self.spritesheet_folder = spritesheet_folder
        self.current_frame = 0
        self.last_update_time = pygame.time.get_ticks()

        # Load spritesheet image and JSON data
        self.load_spritesheet_data()

    def load_spritesheet_data(self):
        """Load and scale frames based on the provided name for spritesheet and JSON."""
        # Define file paths
        image_path = os.path.join(self.spritesheet_folder, f"{self.name}-idle.png")
        json_path = os.path.join(self.spritesheet_folder, f"{self.name}-idle.json")

        # Load spritesheet image
        spritesheet_image = pygame.image.load(image_path).convert_alpha()

        # Load JSON data
        with open(json_path) as f:
            sprite_data = json.load(f)

        # Extract and optionally scale frames
        for frame_name, frame_info in sprite_data["frames"].items():
            frame_rect = frame_info["frame"]
            x, y, w, h = frame_rect["x"], frame_rect["y"], frame_rect["w"], frame_rect["h"]
            frame_image = spritesheet_image.subsurface(pygame.Rect(x, y, w, h))

            # Scale frame if target height is specified
            if self.target_height:
                scale_factor = self.target_height / h
                new_width = int(w * scale_factor)
                frame_image = pygame.transform.scale(frame_image, (new_width, self.target_height))

            duration = frame_info.get("duration", 100)  # Default to 100ms if duration not specified
            self.frames.append((frame_image, duration))

    def update(self):
        """Update the animation frame based on the duration."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.frames[self.current_frame][1]:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update_time = current_time

    def draw(self, screen, position):
        """Draw the current frame of the animation at the specified position."""
        screen.blit(self.frames[self.current_frame][0], position)
