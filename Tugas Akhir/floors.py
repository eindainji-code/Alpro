import random
import time
import json
import battle as b
import mechanics as m
import screen as s

max_floor = 67

with open("data/enemies.json", "r") as f:

    enemies = json.load(f)

#fungsi untuk lantai-lantai dan memilihnya menggunakan tree
class FloorNode: # node lantai
    def __init__(self, floor_num, tier, floor_type="normal"): # masuknya nomor lantai dan tier lantai

        self.floor_num = floor_num
        self.tier = tier
        self.floor_type = floor_type

        self.left = None
        self.right = None

# fungsi membuat tree secara rekursif
def generate_children(node):

    if node.floor_num >= max_floor:
        return  

    next_floor = node.floor_num + 1

    # tier scaling
    tier = get_tier(next_floor)

    # create ONLY 2 next floors
    types = ["normal", "hard", "rest"]

    left_type = random.choice(types)

    types.remove(left_type)

    right_type = random.choice(types)

    node.left = FloorNode(
        next_floor,
        tier,
        left_type
    )

    node.right = FloorNode(
        next_floor,
        tier,
        right_type
    )

# FLOOR TRAVERSAL
def floor_system(player, root,history,inventory):# sistem lantai 

    current_floor = root
    path_taken = []
    
    while current_floor and player["hp"] > 0:

        print("\n" + "=" * 40)
        print(f"FLOOR {current_floor.floor_num}")
        print(f"TIER: {current_floor.tier}")
        print("=" * 40)

        # REST ROOM
        if current_floor.floor_type == "rest":
            print("\n=== REST AREA ===")

            heal = player["max_hp"] // 2

            player["hp"] += heal

            if player["hp"] > player["max_hp"]:
                player["hp"] = player["max_hp"]

            print(f"Healed {heal} HP!")

            time.sleep(2)

            result = "win"

        # HARD ROOM
        elif current_floor.floor_type == "hard":

            print("\n=== HARD ENCOUNTER ===")

            enemy = b.random_enemy(current_floor.tier)

            enemy["hp"] += 10
            enemy["atk"] += 5

            result = history.battle(player, enemy, inventory)

        # NORMAL ROOM
        else:

            enemy = b.random_enemy(current_floor.tier)

            result = history.battle(player, enemy, inventory)

        # PLAYER SURVIVED
        if result == "win":

            if current_floor.floor_type != "rest":
                print(f"{enemy['name']} defeated!")

            if player["floor"] < max_floor:
                player["floor"] += 1

            m.save_player(player)

        elif result == "lose":
            break

        elif result == "exit":
            print("\nEscaped the dungeon!")
            break

        # final floor
        if current_floor.left is None and current_floor.right is None:

            generate_children(current_floor)

            if current_floor.left is None and current_floor.right is None:

                print("\n=== DUNGEON CLEARED ===")

                break

        # choose path
        while True:

            print("\nChoose Path:")
            print(
                f"1. Left Path "
                f"[{current_floor.left.floor_type.title()}]"
            )

            print(
                f"2. Right Path "
                f"[{current_floor.right.floor_type.title()}]")

            print("3. Exit dungeon")

            choice = input("Choose: ")

            if choice in ["1", "2", "3"]:

                break

            print("\nInvalid!")
            time.sleep(1)

        s.clear_terminal()

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

        elif choice == "3":

            print("\nLeft the dungeon!")
            break

    print("\n=== PATH TAKEN ===")

    if len(path_taken) == 0:
        print("No movements.")

    else:
        show_path(path_taken)

    input("\nPress ENTER to return to the main menu...")
    s.clear_terminal()

def show_path(path, index=0):

    # base case
    if index >= len(path):
        return

    print(f"{path[index]}")

    # recursive call
    show_path(path, index + 1)

def get_tier(floor_num):

    if floor_num <= 20:
        return "tier_1"

    elif floor_num <= 40:
        return "tier_2"

    elif floor_num <= 61:
        return "tier_3"

    elif floor_num <= 66:
        return "boss"

    else:
        return "final_boss"