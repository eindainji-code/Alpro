import random
import json

with open('data/class.json', 'r') as f:
    classes = json.load(f)

with open("data/enemies.json", "r") as f:
    enemies = json.load(f)

print(classes["Mage"]["hp"])

rarity_chances = {
    "common" : 65,
    "uncommon" : 23,
    "rare" : 7,
    "Legendary" : 5
}
