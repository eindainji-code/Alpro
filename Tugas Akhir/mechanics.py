import random
import json

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

def Character_Creator():
    nama = input("Masukkan nama: ")
    list_kelas = list(classes.keys())
    
    for i, kelas in enumerate(list_kelas):
        print(f"{i+1}. {kelas}")
        
    choose = int(input("Choose class: "))

    chosen_class = list_kelas[choose - 1]

    player = {
    "name" : nama,
    "class" : chosen_class,
    **classes[chosen_class]
    }
    with open("data/player.json", "w") as f:
        json.dump(player, f, indent= 4)

    return player

def loot_drops():
    chosen_rarity = random.choices(
        list(rarity_chances.keys()),
        weights=rarity_chances.values()
    )[0]

    item = random.choice(loot[chosen_rarity])

    return chosen_rarity, item