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

def loot_drops(player): # fungsi untuk barang yang jatuh dari enemy
    chosen_rarity = random.choices( # menggunakan random untuk membuat variabel chosen_rarity yaitu memilih satu rarity menggunakan weight
        list(rarity_chances.keys()), # mengambil semua keys dalam rarity_chances "common", "uncommon", dst dan membuat menjadi list
        weights=rarity_chances.values() # mengambil value dari rarity_chances dan membuatnya menjadi persen beban
    )[0] # nanti akan mengembalikan list misal ["rare"] dan akan mengambil menggunakan index

    item = random.choice(loot[chosen_rarity]) # membuat variabel item yang menggunakan random lagi akan mengambil loot random berdasarkan rarity diatas

    player["inventory"].append(item) # item akan diappend ke inventory player

    print(f"\nYou got an item!: ")
    print(f"{item} [{chosen_rarity.upper()}]")
    time.sleep(1)
    save_player(player) # save player

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

def battle(player,enemy): # fungsi perlawanan
    print("\n=== Battle Start ===\n")
    time.sleep(0.25)
    enemy_defending = False # boolean mengecek jika musuh lagi defend
    enemy_dodging = False # boolean mengecek jika musuh lagi dodging

    while player["hp"] > 0 and enemy["hp"] > 0: # loop while untuk mengecek jika player atau enemy masih hidup

        print(f"{player["name"]}'s Turn")
        enemy_def = enemy["def"] # variabel untuk defense musuh

        if enemy_defending: # jika enemy lagi defending
            enemy_def = int(enemy_def * 1.5) # defensenya dikali 1.5

        damage = player['atk'] - enemy_def # lalu damagenya adalah jumlah atk dari player - def enemy

        if damage < 1:
            damage = 1

        enemy["hp"] -= damage # hp enemy akan dikurangi damage

        print(f"{player["name"]}'s attacks!")
        print(f"{enemy["name"]} takes {damage} damage!")
        time.sleep(0.25)

        if enemy["hp"] < 0:
            enemy["hp"] = 0

        print(f"{enemy['name']} HP: {enemy['hp']}\n")
        time.sleep(1)

        if enemy["hp"] <= 0: # jika hp enemy 0 atau kurang

            print(f"{enemy['name']} was defeated!") # maka enemy mati

            loot_drops(player) # memanggil drops

            save_player(player) # dan save game

            break

        print(f"{enemy['name']}'s Turn")

        action = enemy_action(enemy["tier"]) # turn enemy

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
            enemy_defending = True

            print(f"{enemy["name"]} is Defending")


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
            save_player(player)
            break

def load_player():

    if not os.path.exists("data/player.json"):
        print("\nNo save file found!")
        return None

    with open("data/player.json", "r") as f:
        players = json.load(f)

    # load first player for now
    return players[0]

def create_enemy(tier, enemy_name):

    enemy = enemies[tier][enemy_name].copy()

    enemy["name"] = enemy_name
    enemy["tier"] = tier

    return enemy
