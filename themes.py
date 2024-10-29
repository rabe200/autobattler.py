# themes.py

import random

# Define color schemes for each theme
THEMES = {
    "fire_snake": {
        "primary": (255, 69, 0),    # Red-Orange
        "secondary": (255, 140, 0), # Dark Orange
        "highlight": (255, 215, 0)  # Gold
    },
    "water_snake": {
        "primary": (0, 191, 255),   # Deep Sky Blue
        "secondary": (0, 105, 148), # Dark Cyan
        "highlight": (173, 216, 230) # Light Blue
    },
    "earth_snake": {
        "primary": (139, 69, 19),   # Saddle Brown
        "secondary": (85, 107, 47), # Dark Olive Green
        "highlight": (160, 82, 45)  # Sienna
    },
    "air_snake": {
        "primary": (135, 206, 250), # Light Sky Blue
        "secondary": (255, 255, 255), # White
        "highlight": (192, 192, 192) # Silver
    }
}

def pick_random_theme():
    """Randomly pick a theme."""
    return random.choice(list(THEMES.keys()))
