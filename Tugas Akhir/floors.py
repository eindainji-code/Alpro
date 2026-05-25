import random
import time
import json
import battle as b
import mechanics as m


with open("data/enemies.json", "r") as f:

    enemies = json.load(f)

#fungsi untuk lantai-lantai dan memilihnya menggunakan tree
class FloorNode: # node lantai
    def __init__(self, floor_num, tier): # masuknya nomor lantai dan tier lantai

        self.floor_num = floor_num
        self.tier = tier

        self.left = None
        self.right = None

# fungsi membuat tree secara rekursif
def generate_children(node):

    next_floor = node.floor_num + 1

    # tier scaling
    if next_floor <= 10:

        tier = "tier_1"

    elif next_floor <= 20:

        tier = "tier_2"

    else:

        tier = "boss"

    # create ONLY 2 next floors
    node.left = FloorNode(next_floor, tier)

    node.right = FloorNode(next_floor, tier)

# FLOOR TRAVERSAL
def floor_system(player, root,history,inventory):# sistem lantai 

    current_floor = root
    path_taken = []

    while current_floor and player["hp"] > 0:

        print("\n" + "=" * 40)
        print(f"FLOOR {current_floor.floor_num}")
        print(f"TIER: {current_floor.tier}")
        print("=" * 40)

        # generate enemy
        enemy = b.random_enemy(current_floor.tier) # mengambil musuh acak

        # start battle
        survived = history.battle(player, enemy, inventory)
        print("Battle function returned!")
        print(f"{enemy['name']} defeated!")

        #player survives
        if survived: #jika player hidup 
            player["floor"] += 1 # lantainya di .json +1
            m.save_player(player)

        # player died
        if not survived:
            break

        # final floor
# generate next floors dynamically
        if current_floor.left is None and current_floor.right is None:

            generate_children(current_floor)

        # choose path
        print("\nChoose Path:")
        print("1. Left Path")
        print("2. Right Path")

        choice = input("Choose: ")

        if choice == "1":

            path_taken.append(
                f"Floor {current_floor.floor_num} -> Left"
            )

            current_floor = current_floor.left

        elif choice == "2":

            path_taken.append(
                f"Floor {current_floor.floor_num} -> Right"
            )

            current_floor = current_floor.right

        else:

            print("\nInvalid!")
            break

    print("\n=== PATH TAKEN ===")

    for path in path_taken:
        print(path)




