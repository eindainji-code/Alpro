import json
import mechanics as m


player = m.Choosing() # test untuk membuat karakter

m.loot_drops(player)
m.inventory(player)

m.enemy_action("Zombie")