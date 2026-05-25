import json
import mechanics as m
import screen as s
import leaderboard as lb
import battle as b
import floors as fl
import inventory as inv

history = b.ActionHistory()

player = s.main_menu()

root = fl.FloorNode(player["floor"], "tier_1")

inventory = inv.Inventory()
for item in player["inventory"]:
    inventory.add_item(item,False)

fl.floor_system(player,root,history,inventory)
