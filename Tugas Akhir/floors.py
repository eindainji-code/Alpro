import random
import time
import json
import battle as b
import mechanics as m


# LOAD ENEMIES
with open("data/enemies.json", "r") as f:

    enemies = json.load(f)

# FLOOR NODE (TREE NODE)
class FloorNode:
    def __init__(self, floor_num, tier):

        self.floor_num = floor_num
        self.tier = tier

        self.left = None
        self.right = None



# GENERATE TREE RECURSIVELY
def generate_tree(current_floor, max_floor):

    # base case
    if current_floor > max_floor:
        return None

    # tier scaling
    if current_floor <= 3:
        tier = "tier_1"

    elif current_floor <= 6:
        tier = "tier_2"

    else:
        tier = "boss"

    # create node
    node = FloorNode(current_floor, tier)

    # recursive calls
    node.left = generate_tree(current_floor + 1, max_floor)

    node.right = generate_tree(current_floor + 1, max_floor)

    return node

# =========================
# FLOOR TRAVERSAL
# =========================

def floor_system(player, root,history):
    history = b.ActionHistory()
    current_floor = root

    while current_floor and player["hp"] > 0:

        print("\n" + "=" * 40)
        print(f"FLOOR {current_floor.floor_num}")
        print(f"TIER: {current_floor.tier}")
        print("=" * 40)

        # generate enemy
        enemy = b.random_enemy(current_floor.tier)

        # start battle
        survived = history.battle(player, enemy)

        #player survives
        if survived:
            player["floor"] += 1
            m.save_player(player)

        # player died
        if not survived:
            break

        # final floor
        if current_floor.left is None and current_floor.right is None:

            print("\nDungeon Cleared!")
            break

        # choose path
        print("\nChoose Path:")
        print("1. Left Path")
        print("2. Right Path")

        choice = input("Choose: ")

        if choice == "1":

            current_floor = current_floor.left

        elif choice == "2":

            current_floor = current_floor.right

        else:

            print("\nInvalid!")
            break





