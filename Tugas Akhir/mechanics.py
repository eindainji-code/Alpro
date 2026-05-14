import random
import json
import os
import time

with open('data/classes.json', 'r') as f: 
    classes = json.load(f) # mengambil data dalam classes.json

with open("data/enemies.json", "r") as f:
    enemies = json.load(f) # mengambil data dalam enemies.json

with open("data/loot.json", "r") as f:
    loot = json.load(f) # mengambil data dalam loot.json

rarity_chances = {
    "common" : 65,
    "uncommon" : 23,
    "rare" : 7,
    "Legendary" : 5
} # digunakan untuk peluang mendapatkan sebuah item berdasarkan rarity

def Character_Creator(name, chosen_class): # fungsi untuk membuat karakter
    data = classes[chosen_class] # mengambil data dari class yang dipilih

    player = {
        "name": name,
        "class": chosen_class,
        "hp": data["hp"],
        "max_hp": data["hp"],
        "atk": data["atk"],
        "def": data["def"],
        "skill": data["skill"],
        "character_level" : 1,
        "exp": 0,
        "floor": 1,
        "inventory": []
    } 
 
    return player #mengambilkan sebuah dict player

def Choosing(): # fungsi untuk memilih karakter dan menamakan karakter

    clear_terminal()

    nama = input("Masukkan nama: ")

    print("=== ALL CHARACTERS ===\n")

    for name_class in classes: #looping semua class

        data = classes[name_class]

        print(f"{name_class}") # mengeprint stat semua class
        print(f"HP      : {data['hp']}")
        print(f"ATK     : {data['atk']}")
        print(f"DEF     : {data['def']}")
        print(f"SKILL   : {data['skill']}")
        print()

    choice = input("Select character: ").capitalize() # pilig class dengan nama

    if choice not in classes: # jika class tidak ada menulis class tidak available
        print("\nClass isn't available!")
        time.sleep(1)
        return
    
    print(f"\nSuccesfully selected {choice}!")
    time.sleep(1) # time digunakan supaya pop-up nya bisa dibaca

    player = Character_Creator(nama, choice) # menggunakan player sebagai variabel untuk membuat karakter

    save_player(player) # fungsi save 

    return player

def loot_drops(player):
    chosen_rarity = random.choices(
        list(rarity_chances.keys()),
        weights=rarity_chances.values()
    )[0]

    item = random.choice(loot[chosen_rarity])

    player["inventory"].append(item)

    print(f"\nYou got an item!: ")
    print(f"{item} [{chosen_rarity.upper()}]")
    time.sleep(1)
    save_player(player)

def enemy_action(enemy_name):

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

def Stats(player):
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

def Inventory(player):
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

def save_player(player):

    file_path = "data/player.json"

    with open(file_path, "r") as f:
        players = json.load(f)

    found = False

    for i, p in enumerate(players):

        if p["name"] == player["name"]:
            players[i] = player
            found = True
            break

    if not found:
        players.append(player)

    with open(file_path, "w") as f:
        json.dump(players, f, indent=4)

def battle(player,enemy):
    print("\n=== Battle Start ===\n")
    time.sleep(0.25)

    while player["hp"] > 0 and enemy["hp"] > 0: # loop while untuk mengecek jika player atau enemy masih hidup

        print(f"{player["name"]}'s Turn")
        damage = player['atk'] - enemy['def']

        if damage < 1:
            damage = 1

        enemy["hp"] -= damage

        print(f"{player["name"]}'s attacks!")
        print(f"{enemy["name"]} takes {damage} damage!")
        time.sleep(0.25)

        if enemy["hp"] < 0:
            enemy["hp"] = 0

        print(f"{enemy['name']} HP: {enemy['hp']}\n")
        time.sleep(1)

        if enemy["hp"] <= 0:

            print(f"{enemy['name']} was defeated!")

            loot_drops(player)

            save_player(player)

            break

        print(f"{enemy['name']}'s Turn")

        action = enemy_action(enemy["name"])

        print(f"{enemy['name']} used {action}!")

        time.sleep(1)

        if action == "attack":

            damage = enemy["atk"] - player["def"]

            if damage < 1:
                damage = 1

            player["hp"] -= damage

            if player["hp"] < 0:
                player["hp"] = 0

            print(f"{player['name']} takes {damage} damage!")

        elif action == "defend":

            print(f"{enemy['name']} defended!")

        elif action == "dodge":

            print(f"{enemy['name']} dodged!")

        elif action == "skill":

            skill_damage = enemy["atk"] * 2

            player["hp"] -= skill_damage

            print(f"{enemy['name']} used their skill!")
            print(f"{player['name']} takes {skill_damage} damage!")

        print(f"{player['name']} HP: {player['hp']}\n")

        time.sleep(1)

        # CHECK IF PLAYER DIED
        if player["hp"] <= 0:

            print(f"{player['name']} was defeated...")
            break

