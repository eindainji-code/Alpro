import json
import mechanics as m
import screen as s
import leaderboard as lb
import battle as b
import floors as fl
import inventory as inv

while True:

    history = b.ActionHistory()

    player = s.main_menu()

    if player == "exit":
        break

    # if menu returns nothing
    if player is None:
        continue

    s.clear_terminal()

    inventory = inv.Inventory()

    for item in player["inventory"]:
        inventory.add_item(item, False)

    root = fl.FloorNode(
        player["floor"],
        fl.get_tier(player["floor"])
    )

    fl.floor_system(player, root, history, inventory)