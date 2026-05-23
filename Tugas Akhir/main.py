import json
import mechanics as m
import screen as s
import leaderboard as lb
import battle as b
import floors as fl

history = b.ActionHistory()
root = fl.generate_tree(1,5)
player = s.main_menu()
fl.floor_system(player,root,history)
