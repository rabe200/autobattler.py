# animation_idle.py

import pygame
import json
import os

class IdleAnimation:
    def __init__(self, name, target_height=None, spritesheet_folder="sprites/spriteSheets", default_name="frog-warrior-idle"):
        self.frames = []
        self.target_height = target_height
        self.name = name.replace(" ", "-").lower()
        print(f"enemy name inside animation file :::: {self.name} \n")
        self.spritesheet_folder = spritesheet_folder
        self.current_frame = 0
        self.last_update_time = pygame.time.get_ticks()

        if not self.load_spritesheet_data(name):
            print(f"Animation '{self.name}' not found. Loading default animation '{default_name}' instead.")
            self.load_spritesheet_data(default_name)

    def load_spritesheet_data(self, name):
        image_path = os.path.join(self.spritesheet_folder, f"{self.name}.png")
        json_path = os.path.join(self.spritesheet_folder, f"{self.name}.json")

        """debugging"""
        print(f"Checking image path: {image_path}")
        print(f"Checking JSON path: {json_path}")
        if not os.path.isfile(image_path) or not os.path.isfile(json_path):
            return False
        """debugging"""

        spritesheet_image = pygame.image.load(image_path).convert_alpha()

        with open(json_path) as f:
            sprite_data = json.load(f)

        self.frames = []
        for frame_name, frame_info in sprite_data["frames"].items():
            frame_rect = frame_info["frame"]
            x, y, w, h = frame_rect["x"], frame_rect["y"], frame_rect["w"], frame_rect["h"]
            frame_image = spritesheet_image.subsurface(pygame.Rect(x, y, w, h))

            if self.target_height:
                scale_factor = self.target_height / h
                new_width = int(w * scale_factor)
                frame_image = pygame.transform.scale(frame_image, (new_width, self.target_height))

            duration = frame_info.get("duration", 100)
            self.frames.append((frame_image, duration))
        return bool(self.frames)

    def update(self):
        if not self.frames:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.frames[self.current_frame][1]:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update_time = current_time

    def draw(self, screen, position):
        #draw the current frame
        if self.frames:
            screen.blit(self.frames[self.current_frame][0], position)
        else:
            print(f"Warning: No frames to draw for animation '{self.name}'.")
