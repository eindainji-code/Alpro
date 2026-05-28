import screen as s
import battle as b
import floors as fl
import inventory as inv
import enemy_queue as eq

while True:

    history = b.ActionHistory() # mulai history aksi

    player = s.main_menu() # membuat karakter

    if player == "exit":
        break # kalau return exit keluar

    if player is None: 
        continue # kalau return none lanjut

    s.clear_terminal()

    inventory = inv.Inventory() # init inventory

    for item in player.inventory:
        inventory.add_item(item, False)

    root = fl.FloorNode(player.floor,fl.get_tier(player.floor)) # mulai root untuk lantai
    enemy_queue = eq.EnemyQueue() # mulai enemy queue
    
    fl.floor_system(player, root, history, inventory, enemy_queue)