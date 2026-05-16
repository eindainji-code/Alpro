import random
import json
import os
import time
import mechanics as m

with open('data/classes.json', 'r') as f: 
    classes = json.load(f) # mengambil data dalam classes.json

with open("data/enemies.json", "r") as f:
    enemies = json.load(f) # mengambil data dalam enemies.json

with open("data/loot.json", "r") as f:
    loot = json.load(f) # mengambil data dalam loot.json


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

def main_menu():

    print("\n=== Welcome to PLACEHOLDER ===\n")
    
    while True:
        print("=== MAIN MENU ===")
        print("1. New Game")
        print("2. Load Game")
        print("3. Exit")

        choice = int(input("Please choose: "))

        if choice == 1:
            player = Choosing()

            print(f"\nWelcome {player["name"]}")
            break

        if choice == 2:
            player = m.load_player()

            if player:
                print(f"\nLoaded {player["name"]}")
                break

        if choice == 3:
            print("\nGoodbye")
            exit()

        else:
            print("\nInvalid\n")

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

    m.save_player(player) # fungsi save 

    return player