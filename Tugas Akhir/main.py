import json
import mechanics as m
import screen as s

with open("data/enemies.json", "r") as f:
    enemies = json.load(f) # mengambil data dalam enemies.json

player = s.main_menu()
enemy = m.create_enemy("tier_1", "Goblin")
m.battle(player, enemy)
