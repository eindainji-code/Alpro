from mechanics import Character_Creator
from mechanics import loot_drops

player = Character_Creator()

for i in range(20):
    rarity, item = loot_drops()
    print(f"{rarity.upper()} -> {item}") 
