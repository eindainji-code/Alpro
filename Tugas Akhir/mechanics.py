import random
import json
import os
import time
import screen as s

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

def enemy_action(enemy_level):

    if enemy_level == "tier_1":
        actions = [
        "attack"
    ]

    elif enemy_level == "tier_2":
        actions = [
        "attack",
        "defend",
        "attack"
    ]

    elif enemy_level == "tier_3":
        actions = [
        "attack",
        "attack",
        "dodge",
        "defend",
        "attack"
    ]
        
    elif enemy_level == "boss":
        actions = [
        "attack",
        "dodge",
        "defend",
        "attack",
        "skill",
        "attack"
    ]

    elif enemy_level == "final_boss":
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

def load_player():

    if not os.path.exists("data/player.json"):
        print("\nNo save file found!")
        return None

    with open("data/player.json", "r") as f:
        players = json.load(f)

    # load first player for now
    return players[0]
