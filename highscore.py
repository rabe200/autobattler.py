# highscore.py

import json
import os

def load_high_scores(characters):
    """Load high scores for each character, returning 0 as default if file doesn't exist."""
    if not os.path.exists("highscores.json"):
        # Create default scores for each character
        return {char["name"]: 0 for char in characters}

    with open("highscores.json", "r") as file:
        return json.load(file)

def save_high_scores(high_scores):
    """Save the high scores to a JSON file."""
    with open("highscores.json", "w") as file:
        json.dump(high_scores, file)
