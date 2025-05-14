import json

# Load the JSON data from a file
with open('../enemies.json', 'r') as file:
    enemies = json.load(file)

# Add "defeat-counter" to each enemy
for enemy_key, enemy_data in enemies.items():
    enemy_data["defeat-counter"] = 0

# Save the modified data back to the JSON file
with open('../enemies.json', 'w') as file:
    json.dump(enemies, file, indent=4)

print("Updated JSON with defeat-counter added to each enemy.")