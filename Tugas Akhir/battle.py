import time
import mechanics as m
import json
import random
import inventory as inv

with open("data/enemies.json", "r") as f:
    enemies = json.load(f) # mengambil data dalam enemies.json

#membuat fungsi melawan dan historynya menggunakan doubly linked list
class ActionNode: # membuat class node 
    def __init__(self, action):

        self.action = action
        self.next = None
        self.prev = None

class ActionHistory: 
    def __init__(self):

        self.head = None
        self.tail = None

    # tambah action ke doubly linked list
    def add_action(self, action): # fungsi memilih aksi

        new_node = ActionNode(action)

        # node pertama kalau belum ada
        if self.head is None: 

            self.head = new_node
            self.tail = new_node

        # tambah ke belakang
        else:

            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node


    # menampilkan history action
    def show_history(self): # untuk melihat history aksi

        current = self.head

        print("\n=== ACTION HISTORY ===")

        while current:

            print(current.action)

            current = current.next


    # battle system
    def battle(self, player, enemy, inventory): # fungsi melawan

        print("\n=== Battle Start ===\n")
        time.sleep(0.25)
        print(f"{enemy["name"]} appeared!")

        enemy_defending = False #boolean jika musuh defending
        enemy_dodging = False # atau dodging

        while player["hp"] > 0 and enemy["hp"] > 0: # sambil player dan musuh hidup

            # PLAYER TURN
            print(f"\n{player['name']}'s Turn")

            print("1. Attack") # ada 3 pilihan
            print("2. Defend")
            print("3. Inventory")

            choice = input("Choose Action: ")

            # convert menu ke action
            if choice == "1":

                action = "attack"

            elif choice == "2":

                action = "defend"

            elif choice == "3":

                action = "inventory"

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

                if enemy_defending: # jika enemy lagi defending 

                    enemy_def = int(enemy_def * 1.5) # defense musuh kali 1.5

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
            elif current.action == "inventory":

                while True:

                    print("\n=== INVENTORY MENU ===")
                    print("1. Show Inventory")
                    print("2. Search Item")
                    print("3. Use Item")
                    print("4. Remove Item")
                    print("5. Exit Inventory")

                    inv_choice = input("Choose: ")

                    # SHOW INVENTORY
                    if inv_choice == "1":

                        inventory.show_inventory()

                    # SEARCH ITEM
                    elif inv_choice == "2":

                        target = input("\nSearch Item: ").title()

                        inventory.search_item(target)

                    # USE ITEM
                    elif inv_choice == "3":

                        inventory.show_inventory()

                        item_choice = input("\nUse Item: ").title()

                        # POTION
                        if item_choice == "Potion":

                            if inventory.search_item("Potion"):

                                heal_amount = 15

                                player["hp"] += heal_amount

                                if player["hp"] > player["max_hp"]:

                                    player["hp"] = player["max_hp"]

                                inventory.remove_item("Potion")

                                print(f"\n{player['name']} used Potion!")
                                print(f"Healed {heal_amount} HP!")

                        # BANDAGE
                        elif item_choice == "Bandage":

                            if inventory.search_item("Bandage"):

                                heal_amount = 5

                                player["hp"] += heal_amount

                                if player["hp"] > player["max_hp"]:

                                    player["hp"] = player["max_hp"]

                                inventory.remove_item("Bandage")

                                print(f"\n{player['name']} used Bandage!")
                                print(f"Healed {heal_amount} HP!")

                        # SYRINGE
                        elif item_choice == "Syringe":

                            if inventory.search_item("Syringe"):

                                heal_amount = 25

                                player["hp"] += heal_amount

                                if player["hp"] > player["max_hp"]:

                                    player["hp"] = player["max_hp"]

                                inventory.remove_item("Syringe")

                                print(f"\n{player['name']} used Syringe!")
                                print(f"Healed {heal_amount} HP!")

                        # WITCHES BREW
                        elif item_choice == "Witches Brew":

                            if inventory.search_item("Witches Brew"):

                                heal_amount = 40

                                player["hp"] += heal_amount

                                if player["hp"] > player["max_hp"]:

                                    player["hp"] = player["max_hp"]

                                inventory.remove_item("Witches Brew")

                                print(f"\n{player['name']} used Witches Brew!")
                                print(f"Healed {heal_amount} HP!")

                        else:

                            print("\nItem cannot be used!")

                    # REMOVE ITEM
                    elif inv_choice == "4":

                        inventory.show_inventory()

                        target = input("\nRemove Item: ").title()

                        inventory.remove_item(target)

                    # EXIT
                    elif inv_choice == "5":

                        break

                    else:

                        print("\nInvalid!")

                continue

            time.sleep(1)

            # CHECK IF ENEMY DEAD
            if enemy["hp"] <= 0:

                print(f"\n{enemy['name']} was defeated!")

                m.loot_drops(inventory) # memanggil fungsi loot dari mechanics

                player["inventory"] = inventory.to_list() # save ke inventory

                m.save_player(player) # player di save

                return True # kembalikan true

            # ENEMY TURN
            print(f"\n{enemy['name']}'s Turn")

            action = m.enemy_action(enemy["tier"]) # aksi musuh pakai fungsi dari mekanik berdasarkan tiernya

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

def random_enemy(tier): # fungsi untuk mendapatkan enemy yang random
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

