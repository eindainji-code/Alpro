import random

classes = {
    "Mage": {"hp": 18, "att" : 7, "skill" : "fireball"},
    "Barbarian": {"hp": 19, "att": 6, "skill" : "rage"},
    "Knight" : {"hp": 23, "att": 2, "skill" : "protect"},
    "Archer" : {"hp": 16, "att": 9, "skill" : "critical shot"}
}

enemies = {
    "Slime": {"hp": 10, "att": 3},
    "Wolf": {"hp": 12, "att": 4},
    "Zombie": {"hp": 14, "att": 5},
    "Skeleton": {"hp": 12, "att": 7},
    "Skog" : {"hp": 40, "att": 10} # BOSS demo
}
loot = {
    "common": [
        "nearly broken staff", # untuk mage
        "worn-out shield", # untuk knight
        "flimsy sword", # untuk barbarian
        "straight-limb longbow", # untuk archer
        "bandage"
    ],
    "uncommon": [
        "oak staff",
        "bronze sword",
        "copper shield",
        "un-power bow",
        "syringe"
    ],
    "rare" : [
        "Buloke staff",
        "Steel sword",
        "Roman Scutum", #Shield
        "Power bow",
        "Potion"
    ],

    "Legendary" : [
        "Adams staff",
        "Diamond sword",
        "Americanized shield",
        "Artemis's Bow",
        "Witches Brew"
    ] 
}

rarity_chances = {
    "common" : 65,
    "uncommon" : 23,
    "rare" : 7,
    "Legendary" : 5
}

def drop():
    chosen_rarity = random.choices(
        list(rarity_chances.keys()),
        weights=rarity_chances.values()
    )[0]

    item = random.choice(loot[chosen_rarity])

    return chosen_rarity,item

for i in range(100):
    rarity, item = drop()
    print(f"{rarity.upper()} -> {item}")

for kelas, stats in classes.items():
    print(stats["hp"])