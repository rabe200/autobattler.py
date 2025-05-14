# animation_files.py

import pygame
import json
import os

class AnimationFiles:
    def __init__(self, folder_path):
        self.folder_path = "../sprites/spriteSheets"
        self.images = {}  # Dictionary to store images with file name as key
        self.data = {}    # Dictionary to store JSON data with file name as key
        self.load_files()

    def load_files(self):
        for filename in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, filename)
            file_base, file_ext = os.path.splitext(filename)

            if file_ext.lower() == '.png':
                # Load and store the image
                self.images[file_base] = pygame.image.load(file_path).convert_alpha()

            elif file_ext.lower() == '.json':
                # Load and store JSON data
                with open(file_path) as f:
                    self.data[file_base] = json.load(f)

    def get_image(self, name):
        """Get the image by name (without extension)"""
        return self.images.get(name)

    def get_data(self, name):
        """Get the JSON data by name (without extension)"""
        return self.data.get(name)

# Example usage:
# animation_files = AnimationFiles('animations')
# frog_image = animation_files.get_image('frog1-spritesheet')
# frog_data = animation_files.get_data('frog1-spritesheet')
