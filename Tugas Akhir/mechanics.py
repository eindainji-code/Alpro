import random
import json
import os
import time
import screen as s
import inventory as inv

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

def loot_drops(inventory): # fungsi untuk barang yang jatuh dari enemy
    chosen_rarity = random.choices( # menggunakan random untuk membuat variabel chosen_rarity yaitu memilih satu rarity menggunakan weight
        list(rarity_chances.keys()), # mengambil semua keys dalam rarity_chances "common", "uncommon", dst dan membuat menjadi list
        weights=rarity_chances.values() # mengambil value dari rarity_chances dan membuatnya menjadi persen beban
    )[0] # nanti akan mengembalikan list misal ["rare"] dan akan mengambil menggunakan index

    item = random.choice(loot[chosen_rarity]) # membuat variabel item yang menggunakan random lagi akan mengambil loot random berdasarkan rarity diatas

    inventory.add_item(item) # item akan diappend ke inventory player

    print(f"\nYou got an item!: ")
    print(f"{item} [{chosen_rarity.upper()}]\n")
    time.sleep(1)

def enemy_action(enemy_level): # fungsi untuk aksi yang akan dilaksanakan oleh musuh

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

def save_player(player): # fungsi save 

    file_path = "data/player.json" # menyetor file kedalam variabel

    with open(file_path, "r") as f: # membuka file dalam read mode
        players = json.load(f) # lalu, load player

    found = False # boolean untuk mengecek jika sebuah player sudah diketemui

    for i, p in enumerate(players): # loop melalui semua player dalam file

        if p["name"] == player["name"]: # cek jika karakter yang mau disave sama dengan karakter yang sudah ada dalam file player
            players[i] = player # jika iya, player sebelumnya akan diganti dengan yang baru
            found = True # found menjadi true
            break

    if not found: # jika sebuah player belum ada dalam file
        players.append(player) # akan append player yang baru dibuat kedalam list

    with open(file_path, "w") as f:
        json.dump(players, f, indent=4)

def load_player():

    if not os.path.exists("data/player.json"):

        print("\nNo save file found!")

        return None

    with open("data/player.json", "r") as f:

        players = json.load(f)

    # show all players
    print("\n=== SAVED PLAYERS ===\n")

    for i, player in enumerate(players, start=1):

        print(
            f"{i}. "
            f"{player['name']} | "
            f"{player['class']} | "
            f"Floor: {player['floor']}"
        )

    # choose player
    choice = int(input("\nChoose Save: "))

    # validate
    if choice < 1 or choice > len(players):

        print("\nInvalid save!")

        return None

    # selected player
    player = players[choice - 1]

    # dead player check
    if player["hp"] <= 0:

        print("\nCharacter is dead!")

        return None

    print(f"\nLoaded {player['name']}!")

    return player