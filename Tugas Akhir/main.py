import json
import mechanics as m


player = m.Choosing() # test untuk membuat karakter
enemy = {
    "name": "Skog",
    "hp": 50,
    "atk": 20,
    "def": 10
}
m.battle(player,enemy)