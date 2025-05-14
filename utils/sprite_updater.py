# sprite_updater.py

import os
import json

# Path to the sprites directory and JSON file
SPRITE_DIR = "../sprites/enemies"
ENEMIES_JSON = "enemies.json"

# Default stats for new enemies
DEFAULT_STATS = {
    "life": 1,
    "attack": 0,
    "armor": 0,
    "speed": 0,
    "level": 1  # New attribute
}

def load_existing_enemies():
    """Load existing enemies from JSON file, or return an empty dictionary if file does not exist."""
    if os.path.exists(ENEMIES_JSON):
        with open(ENEMIES_JSON, "r") as file:
            return json.load(file)
    return {}

def save_enemies_to_json(enemies):
    """Save enemies dictionary to JSON file."""
    with open(ENEMIES_JSON, "w") as file:
        json.dump(enemies, file, indent=4)

def update_enemies():
    """Update the JSON with any new enemy sprites found in the sprites directory."""
    enemies = load_existing_enemies()
    updated = False

    # Scan the sprites directory for new image files
    for filename in os.listdir(SPRITE_DIR):
        if filename.endswith((".png", ".jpg", ".jpeg", ".webp")):
            enemy_name = filename.rsplit(".", 1)[0]  # Use the file name without extension as the enemy name
            image_path = os.path.join(SPRITE_DIR, filename)

            # Add new enemy if it doesn't exist in the JSON
            if enemy_name not in enemies:
                enemies[enemy_name] = {
                    "name": enemy_name,
                    "image_path": image_path,
                    **DEFAULT_STATS  # Set default stats with level
                }
                updated = True
                print(f"Added new enemy: {enemy_name}")

    # Save to JSON only if there were updates
    if updated:
        save_enemies_to_json(enemies)
        print("Enemies JSON updated successfully.")
    else:
        print("No new enemies found to update.")

if __name__ == "__main__":
    update_enemies()
