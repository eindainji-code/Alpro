import time
import mechanics as m
import json
import random
import screen as s
import encyclopedia as enc
import turn_rotation as tr

#Hash table untuk data healing
item_data = {
    "Potion": {"heal": 20},
    "Bandage": {"heal": 10},
    "Syringe": {"heal": 35},
    "Witches Brew": {"heal": 50}
}

with open("data/enemies.json", "r") as f:
    enemies = json.load(f) # mengambil data dalam enemies.json

#membuat fungsi melawan dan historynya menggunakan doubly linked list
class ActionNode: # membuat class node 
    def __init__(self, action):
        self.action = action
        self.next = None
        self.prev = None

class ActionHistory: # doubly linked list
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

        # tambah ke belakang kalau sudah ada
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

        # circular linked list
        rotation = tr.TurnRotation() # dengan CLL mulai rotasi

        rotation.add_turn("player") # player gerak duluan
        rotation.add_turn("enemy") # lalu musuh

        rotation.start()

        enemy_defending = False #boolean jika musuh defending
        enemy_dodging = False # atau dodging
        player_defending = False # boolean untuk player defend

        while player.hp > 0 and enemy["hp"] > 0: # sambil player dan musuh hidup
            turn = rotation.next_turn() # rotasi akan berganti dari player dan musuh    

            # PLAYER TURN
            if turn == "player":
                print(f"\n{player.name}'s Turn!")
                print("-" * 40)

                print("1. Attack") # ada 7 pilihan
                print("2. Defend")
                print("3. Skill")
                print("4. Inventory")
                print("5. Enemy Info")
                print("6. Stats")
                print("7. Exit")

                choice = input("Choose Action: ") # pilih aksi
                s.clear_terminal()
                # convert menu ke action
                if choice == "1":
                    action = "attack"

                elif choice == "2":
                    action = "defend"

                elif choice == "3":
                    action = "skill"

                elif choice == "4":
                    action = "inventory"

                elif choice == "5":
                    action = "enemy_info"

                elif choice == "6":
                    action = "stats"

                elif choice == "7":
                    action = "exit"
                    
                else:
                    print("\nInvalid!")
                    continue # continue supaya jika pilih salah, bisa pilih lagi

                # simpan action ke doubly linked list
                self.add_action(action)

                # execute latest action
                current = self.tail

                print(f"\nAction Used: {current.action}")

                # attack
                if current.action == "attack":
                    enemy_def = enemy["def"] # enemy's defense is enemy_def
        
                    if enemy_defending: # jika enemy lagi defending 
                        enemy_def = int(enemy_def * 1.5) # defense musuh kali 1.5

                    damage = player.atk - enemy_def # calculate damage

                    if damage < 1:
                        damage = 1

                    if enemy_dodging: # if enemy dodging
                        damage = 0 # does 0 damage
                        print(f"{enemy['name']} dodged the attack!")

                        enemy_dodging = False # after dodged enemy dodging becomes false

                    enemy["hp"] -= damage # enemy health goes down

                    if enemy["hp"] < 0:
                        enemy["hp"] = 0 #if enemy hp is 0 or lower

                    print(f"{player.name} attacks!")
                    print(f"{enemy['name']} takes {damage} damage!")
                    print(f"\n{enemy['name']} HP: {enemy['hp']}")
                    print(f"{player.name} HP: {player.hp}")
                    time.sleep(0.5)
                    enemy_defending = False # so enemy defending isnt stuck on true

                # defend
                elif current.action == "defend":
                    player_defending = True # if player defends
                    print(f"{player.name} is defending!")

                # inventory
                elif current.action == "inventory":
                    while True:
                        equipped = player.equipped_item # check what item is equipped

                        if equipped is None:
                            equipped = "None" # if nothing its none

                        # shows a bit of info
                        print(f"\nEquipped: {equipped}")
                        print(f"Class: {player.char_class}")
                        exp_needed = player.level * 50 
                        remaining_exp = max(0,exp_needed - player.exp)

                        print(
                            f"LEVEL: {player.level} | "
                            f"EXP: {player.exp}/{exp_needed}"
                        )

                        print(f"EXP Needed: {remaining_exp}") 

                        #inventory menu
                        print("\n=== INVENTORY MENU ===") 
                        print("1. Show Inventory") # 6 options
                        print("2. Search Item")
                        print("3. Use Item")
                        print("4. Scavenge Item")
                        print("5. Equip Item")
                        print("6. Exit Inventory")

                        inv_choice = input("Choose: ") # choose
                        s.clear_terminal()
                        # SHOW INVENTORY
                        if inv_choice == "1":
                            inventory.show_inventory() # show inventory function

                        # SEARCH ITEM
                        elif inv_choice == "2":
                            target = input("\nSearch Item: ").strip() # strip so xtra space removed
                            inventory.search_item(target) # search function

                        # USE ITEM
                        elif inv_choice == "3": # use item                           
                            if inventory.head is None: # if nothing in inventory
                                print("\nInventory is empty!") # prints this
                                time.sleep(0.5)
                                continue 

                            inventory.show_inventory() # show inventory function
                            item_choice = input("\nUse Item: ").strip()

                            # check if item exists in hash table above
                            if item_choice in item_data:

                                # check if player has item
                                found_item = inventory.search_item(item_choice)

                                if found_item:
                                    heal_amount = item_data[item_choice]["heal"] # heals based on the data
                                    player.hp += heal_amount

                                    # max hp limit
                                    if player.hp > player.max_hp: # if hp is bigger than max
                                        player.hp = player.max_hp

                                    inventory.remove_item(item_choice) # remove item
                                    print(f"\n{player.name} used {item_choice}!")
                                    print(f"Healed {heal_amount} HP!")

                            else:
                                print("\nItem cannot be used!")

                        # SCAVENGE ITEM
                        elif inv_choice == "4":
                            if inventory.head is None:
                                print("\nInventory is empty!")
                                time.sleep(1)
                                continue

                            inventory.show_inventory()
                            item_name = input("\nScavenge Item: ").strip() # scavenge input
                            m.scavenge_item(player, inventory, item_name)# scavenge function
                            time.sleep(1)

                        #EQUIP ITEM
                        elif inv_choice == "5":
                            if inventory.head is None:
                                print("\nInventory is empty!")
                                time.sleep(0.5)
                                continue

                            inventory.show_inventory()
                            item_name = input("\nEquip Item: ").strip()
                            m.equip_item(player, inventory, item_name) # equip function

                        # EXIT
                        elif inv_choice == "6": # exit
                            break

                        else:
                            print("\nInvalid!")

                    rotation.set_player_turn() # if you exit this menu then its still your turn
                    continue # continue
                
                #CHECK STATS
                elif current.action == "stats":
                    s.Stats(player) # stats function

                    s.clear_terminal()
                    rotation.set_player_turn() # still player turn
                    continue 

                elif current.action == "exit":
                    return "exit" #returns "exit"
                
                #SKILL USAGE
                elif current.action == "skill":
                    if player.floor < player.skill_cooldown: # check skill cooldown
                        remaining = (player.skill_cooldown- player.floor) # cooldown remaining
                        print(f"\nSkill is on cooldown!")
                        print(f"{remaining} floor(s) remaining.")
                        rotation.set_player_turn()
                        continue

                    print(f"\n{player.name} used " 
                          f"{player.skill}!")

                    if player.char_class == "Mage": # if mage skill
                        damage = player.atk * 2
                        enemy["hp"] -= damage

                        print(
                            f"Fireball deals "
                            f"{damage} damage!"
                        )

                    elif player.char_class == "Barbarian": # if barb skill
                        player.atk += 5

                        print("\nAttack increased!")

                    elif player.char_class == "Knight": #if knight skill
                        player_defending = True
                        player.defense += 5

                        print("\nDefense increased!")

                    elif player.char_class == "Archer": # if archer skill
                        damage = player.atk * 3
                        enemy["hp"] -= damage

                        print(
                            f"Critical Shot deals "
                            f"{damage} damage!"
                        )
                    
                    player.skill_cooldown = (player.floor + 7) # skill cooldown is every 7 floors

                #ENCYCLOPEDIA
                elif current.action == "enemy_info":
                    enc.encyclopedia() # encyclopedia function
                    rotation.set_player_turn()
                    continue

                time.sleep(1)

                # CHECK IF ENEMY DEAD
                if enemy["hp"] <= 0:
                    print(f"\n{enemy['name']} was defeated!")

                    # gain exp based on enemies
                    exp_gain = enemy.get("exp", 0)
                    player.exp += exp_gain

                    print(f"\nGained {exp_gain} EXP!")

                    # check level up
                    m.check_level_up(player)

                    # loot
                    m.loot_drops(inventory)

                    player.inventory = inventory.to_list() # save ke inventory
                    m.save_player(player) # player di save
                    return "win" # kembalikan true

            # ENEMY TURN
            elif turn == "enemy":

                print(f"\n{enemy['name']}'s Turn")
                print("-" * 40)

                enemy_defending = False

                action = m.enemy_action(enemy["tier"]) # aksi musuh pakai fungsi dari mekanik berdasarkan tiernya

                print(f"{enemy['name']} used {action}!")

                time.sleep(1)

                if action == "attack": # enemy attacks
                    player_def = player.defense
                    if player_defending:
                        player_def = int(player_def * 1.5)

                    damage = enemy["atk"] - player_def

                    if damage < 1:
                        damage = 1

                    player.hp -= damage

                    if player.hp < 0:
                        player.hp = 0

                    print(f"{player.name} takes {damage} damage!")
                    player_defending = False

                elif action == "defend":
                    enemy_defending = True
                    print(f"{enemy['name']} is Defending!")

                elif action == "dodge":
                    enemy_dodging = True
                    print(f"{enemy['name']} dodged!")

                elif action == "skill":
                    skill_damage = enemy["atk"] * 2
                    player.hp -= skill_damage
                    if player.hp < 0:
                        player.hp = 0

                    print(f"{enemy['name']} used their skill!")
                    print(f"{player.name} takes {skill_damage} damage!")

                print(f"\n{enemy['name']} HP: {enemy['hp']}")
                print(f"{player.name} HP: {player.hp}")
                player_defending = False
                time.sleep(1)

                # CHECK IF PLAYER IS DEAD
                if player.hp <= 0:
                    print(f"\n{player.name} was defeated...")
                    m.save_player(player)
                    return "lose"

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