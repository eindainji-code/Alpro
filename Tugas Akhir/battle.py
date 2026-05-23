import time
import mechanics as m
import json
import random

with open("data/enemies.json", "r") as f:
    enemies = json.load(f) # mengambil data dalam enemies.json

class ActionNode:
    def __init__(self, action):

        self.action = action
        self.next = None
        self.prev = None

class ActionHistory:
    def __init__(self):

        self.head = None
        self.tail = None

    # tambah action ke doubly linked list
    def add_action(self, action):

        new_node = ActionNode(action)

        # node pertama
        if self.head is None:

            self.head = new_node
            self.tail = new_node

        # tambah ke belakang
        else:

            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node


    # menampilkan history action
    def show_history(self):

        current = self.head

        print("\n=== ACTION HISTORY ===")

        while current:

            print(current.action)

            current = current.next


    # battle system
    def battle(self, player, enemy):

        print("\n=== Battle Start ===\n")
        time.sleep(0.25)

        enemy_defending = False
        enemy_dodging = False

        while player["hp"] > 0 and enemy["hp"] > 0:

            # PLAYER TURN
            print(f"\n{player['name']}'s Turn")

            print("1. Attack")
            print("2. Defend")
            print("3. Heal")

            choice = input("Choose Action: ")

            # convert menu ke action
            if choice == "1":

                action = "attack"

            elif choice == "2":

                action = "defend"

            elif choice == "3":

                action = "heal"

            else:

                print("\nInvalid!")
                continue

            # simpan action ke doubly linked list
            self.add_action(action)

            # execute latest action
            current = self.tail

            print(f"\nAction Used: {current.action}")

            # ATTACK
            if current.action == "attack":

                enemy_def = enemy["def"]

                if enemy_defending:

                    enemy_def = int(enemy_def * 1.5)

                damage = player["atk"] - enemy_def

                if damage < 1:
                    damage = 1

                enemy["hp"] -= damage

                if enemy["hp"] < 0:
                    enemy["hp"] = 0

                print(f"{player['name']} attacks!")
                print(f"{enemy['name']} takes {damage} damage!")

                enemy_defending = False

            # DEFEND
            elif current.action == "defend":

                print(f"{player['name']} is defending!")

            # HEAL
            elif current.action == "heal":

                player["hp"] += 10

                if player["hp"] > player["max_hp"]:
                    player["hp"] = player["max_hp"]

                print(f"{player['name']} healed!")

            print(f"\n{enemy['name']} HP: {enemy['hp']}")
            print(f"{player['name']} HP: {player['hp']}")

            time.sleep(1)

            # CHECK IF ENEMY DEAD
            if enemy["hp"] <= 0:

                print(f"\n{enemy['name']} was defeated!")

                m.loot_drops(player)

                m.save_player(player)

                return True

            # ENEMY TURN
            print(f"\n{enemy['name']}'s Turn")

            action = m.enemy_action(enemy["tier"])

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

                print(f"{enemy['name']} is Defending!")

            elif action == "dodge":

                enemy_dodging = True

                print(f"{enemy['name']} dodged!")

            elif action == "skill":

                skill_damage = enemy["atk"] * 2

                player["hp"] -= skill_damage

                if player["hp"] < 0:
                    player["hp"] = 0

                print(f"{enemy['name']} used their skill!")
                print(f"{player['name']} takes {skill_damage} damage!")

            print(f"\n{player['name']} HP: {player['hp']}")

            time.sleep(1)

            # CHECK IF PLAYER IS DEAD
            if player["hp"] <= 0:

                print(f"\n{player['name']} was defeated...")

                m.save_player(player)

                return False

def random_enemy(tier):
    # random enemy name
    enemy_name = random.choice(
        list(enemies[tier].keys())
    )

    # copy enemy data
    enemy_data = enemies[tier][enemy_name].copy()

    # add extra info
    enemy_data["name"] = enemy_name
    enemy_data["tier"] = tier

    return enemy_data

