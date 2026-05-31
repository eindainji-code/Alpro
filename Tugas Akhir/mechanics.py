import random
import json
import os
import time
import screen as s
import inventory as inv
from character import Character

MAX_FLOOR = 67

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
    "legendary" : 5
} # digunakan untuk peluang mendapatkan sebuah item berdasarkan rarity

weapon_types = {
    "Archer": [
        "straight limb longbow",
        "unpower bow",
        "power bow",
        "artemis's bow"
    ],
    "Mage": [
        "nearly broken staff",
        "oak staff",
        "buloke staff",
        "adams staff"
    ],
    "Knight": [
        "worn out shield",
        "copper shield",
        "roman scutum shield",
        "captain's shield"
    ],
    "Barbarian": [
        "flimsy sword",
        "bronze sword",
        "steel sword",
        "diamond sword"
    ]
} # tipe senjata

equipment_stats = {
    # staffs
    "nearly broken staff": {"atk": 4},
    "oak staff": {"atk": 8},
    "buloke staff": {"atk": 10},
    "adams staff": {"atk": 20},

    # swords
    "flimsy sword": {"atk": 4},
    "bronze sword": {"atk": 8},
    "steel sword": {"atk": 10},
    "diamond sword": {"atk": 20},

    # shields
    "worn-out shield": {"def": 4},
    "copper shield": {"def": 8},
    "roman scutum (shield)": {"def": 10},
    "captain's shield": {"def": 20},

    # bows
    "straight limb longbow": {"atk": 4},
    "un-power bow": {"atk": 8},
    "power bow": {"atk": 10},
    "artemis's bow": {"atk": 20}
}

RARITY_EXP = (
    ("common", 10),
    ("uncommon", 20),
    ("rare", 50),
    ("legendary", 100)
)

with open("data/loot.json", "r") as f:
    loot = json.load(f) # value jumlah exp item berdasarkan rarity

def loot_drops(inventory): # fungsi untuk barang yang jatuh dari enemy
    drop_chance = 0.45
    if random.random() > drop_chance:
        print("\nNo drops!")
        time.sleep(1)
        return
    
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
        if p["name"] == player.name: # cek jika karakter yang mau disave sama dengan karakter yang sudah ada dalam file player
            players[i] = player.to_dict() # jika iya, player sebelumnya akan diganti dengan yang baru
            found = True # found menjadi true
            break

    if not found: # jika sebuah player belum ada dalam file
        players.append(player.to_dict()) # akan append player yang baru dibuat kedalam list

    with open(file_path, "w") as f:
        json.dump(players, f, indent=4)

def load_player(): # fungsi untuk loadkan player
    if not os.path.exists("data/player.json"):
        print("\nNo save file found!")
        return None # jika tidak ada filenya

    with open("data/player.json", "r") as f:
        players = json.load(f)

    if len(players) == 0:
        print("\nNo saved players!")
        time.sleep(2)
        s.clear_terminal()
        return None
    
    # show all players
    print("\n=== SAVED PLAYERS ===\n") # menunjukkan players yang tersave
    for i, player_data in enumerate(players, start=1):
        player = Character.from_dict(player_data)
        # completed dungeon
        if player.floor >= MAX_FLOOR:
            status = "CLEARED"
        else:
            status = f"Floor: {player.floor}"

        print(
            f"{i}. "
            f"{player.name} | "
            f"{player.char_class} | "
            f"{status}"
        )

    # choose player
    while True:
        try:
            choice = int(input("\nChoose Save: "))

            # range validation
            if choice < 1 or choice > len(players):
                print("\nInvalid save!")
                continue
            break

        except ValueError:
            print("\nPlease enter a valid number!")

    # validate
    if choice < 1 or choice > len(players):
        print("\nInvalid save!")
        return None

    # selected player
    player = Character.from_dict(players[choice - 1])

    # completed save check
    if player.floor >= MAX_FLOOR:
        print("\nThis save already cleared the dungeon!")
        time.sleep(2)
        s.clear_terminal()
        return None
    
    # dead player check
    if player.hp <= 0:
        print("\nCharacter is dead!")
        time.sleep(2)
        s.clear_terminal()
        return None

    print(f"\nLoaded {player.name}!")
    s.clear_terminal()
    return player

def check_level_up(player):
    # exp needed formula
    exp_needed = player.level * 50

    while player.exp >= exp_needed:
        player.exp -= exp_needed
        player.level += 1
        print("\n=== LEVEL UP! ===")
        print(
            f"{player.name} "
            f"reached level "
            f"{player.level}!"
        )

        # stat increases
        player.max_hp += 10
        player.atk += 2
        player.defense += 1

        # fully heal on level up
        player.hp = player.max_hp

        print("\nStats Increased!")
        print(f"HP  : {player.max_hp}")
        print(f"ATK : {player.atk}")
        print(f"DEF : {player.defense}")

        # next level requirement
        exp_needed = player.level * 50

def equip_item(player, inventory, item_name):
    item_name =item_name.lower()
    found_item = inventory.search_item(item_name)

    if not found_item:
        return

    player_class = player.char_class
    allowed_weapons = weapon_types[player_class]
    if item_name not in allowed_weapons:
        print("\nYour class cannot equip this!")
        return

    # validate equipment first
    stats = equipment_stats.get(item_name)
    if stats is None:
        print("\nItem cannot be equipped!")
        return

    # remove old stats
    old_item = player.equipped_item
    if old_item:
        old_stats = equipment_stats.get(old_item)

        if old_stats and "atk" in old_stats:
            player.atk -= old_stats["atk"]

        if old_stats and "def" in old_stats:
            player.defense -= old_stats["def"]

    # equip item
    player.equipped_item = item_name

    # apply stats
    if "atk" in stats:
        player.atk += stats["atk"]

    if "def" in stats:
        player.defense += stats["def"]

    print(f"\nEquipped {item_name}!")

def get_item_rarity(item_name):
    for rarity, items in loot.items():
        if item_name in items:
            return rarity

    return None

def scavenge_item(player, inventory, item_name):
    # item exists?
    found_item = inventory.search_item(item_name)

    if not found_item:
        return

    rarity = get_item_rarity(item_name)

    if rarity is None:
        print("\nItem rarity not found!")
        return

    gained_exp = 0

    for rarity_name, exp in RARITY_EXP:
        if rarity == rarity_name:
            gained_exp = exp
            break

    player.exp += gained_exp

    check_level_up(player)

    inventory.remove_item(item_name)

    print(f"\nScavenged {item_name}!")
    print(f"Gained {gained_exp} EXP!")