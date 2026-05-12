import random
import json
import os
import time

with open('data/class.json', 'r') as f: 
    classes = json.load(f)

with open("data/enemies.json", "r") as f:
    enemies = json.load(f)

with open("data/loot.json", "r") as f:
    loot = json.load(f)

rarity_chances = {
    "common" : 65,
    "uncommon" : 23,
    "rare" : 7,
    "Legendary" : 5
}

player = { #DICTIONARY/HASH TABLE
    "name": "",
    "class": "",
    "hp": 0,
    "max_hp": 0,
    "atk": 0,
    "def": 0,
    "skill": 0,
    "level": 1,
    "exp": 0,
    "inventory": [] #LIST
}

def Character_Creator():
    nama = input("Masukkan nama: ")
    clear_terminal()

    print("=== ALL CHARACTERS ===\n")

    for name_class in classes: #LOOPING

        data = classes[name_class]

        print(f"{name_class}")
        print(f"HP      : {data['hp']}")
        print(f"ATK     : {data['atk']}")
        print(f"DEF     : {data['def']}")
        print(f"SKILL   : {data['skill']}")
        print()

    choice = input("Select character: ")

    if choice not in classes: #SEARCHING
        print("\nClass isn't available!")
        time.sleep(1)
        return
    
    data = classes[choice]
    player["name"] = nama
    player["class"] = choice
    player["hp"] = data["hp"]
    player["max_hp"] = data["hp"]
    player["atk"] = data["atk"]
    player["def"] = data["def"]
    player["skill"] = data["skill"]

    print(f"\nSuccesfully selected {choice}!")
    time.sleep(1)

    with open("data/player.json", "w") as f:
        json.dump(player, f, indent= 4)

    return player

def loot_drops():
    chosen_rarity = random.choices(
        list(rarity_chances.keys()),
        weights=rarity_chances.values()
    )[0]

    item = random.choice(loot[chosen_rarity])

    player["inventory"].append(item)

    print(f"\nYou got an item!: ")
    print(f"{item} [{chosen_rarity.upper()}]")
    time.sleep(1)

def enemy_action(enemies):

    enemy_name = enemies["name"]
    if enemy_name == "Zombie":
        actions = [
        "attack",
        "attack",
        "attack",
        "defend"
    ]

    elif enemy_name == "Skeleton":
        actions = [
        "attack",
        "dodge",
        "attack"
    ]

    elif enemy_name == "Slime":
        actions = [
        "attack",
        "attack",
        "attack"
    ]
        
    elif enemy_name == "Wolf":
        actions = [
        "attack",
        "dodge",
        "defend",
        "attack"
    ]

    elif enemy_name == "Skog":
        actions = [
        "attack",
        "dodge",
        "attack",
        "defend",
        "skill"
    ]

    else:
        actions = [
            "attack"
        ]

    return random.choice(actions)

def clear_terminal():
    os.system("cls")

def loading():
    print("\nLoading", end="")

    for _ in range(3):
        time.sleep(0.5)
        print(".", end="")

    print()

def stats():
    clear_terminal()

    print("=== PLAYER INFO ===")

    print(f"Name        : {player['name']}")
    print(f"Class       : {player['class']}")
    print(f"HP          : {player['hp']}")
    print(f"ATK         : {player['atk']}")
    print(f"DEF         : {player['def']}")
    print(f"LEVEL       : {player['level']}")
    print(f"EXP         : {player['exp']}")

    print("\nPress ENTER to go back.")

def inventory():
    clear_terminal()

    print("=== INVENTORY ===")
    if len(player["inventory"]) == 0:
        print("Inventory's empty")
    else:
        number = 1

        for item in player["inventory"]:
            print(f"{number}. {item}")
            number += 1

    print("\nPress ENTER to go back.")