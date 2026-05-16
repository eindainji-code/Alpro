import json
import mechanics as m
import screen as s

with open("data/enemies.json", "r") as f:
    enemies = json.load(f) # mengambil data dalam enemies.json

s.main_menu()
enemy = enemies["tier_1"]["Slime"].copy()
enemy["name"] = "Slime"
