import json

class Character:
    def __init__(self, name, hp, atk, defense, level=1, exp=0):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.defense = defense
        self.level = level
        self.exp = exp

    def attack_enemy(self, enemy):
        damage = self.atk - enemy.defense

        if damage < 0:
            damage = 0

        enemy.hp -= damage

        print(f"{self.name} menyerang {enemy.name}")
        print(f"Damage: {damage}")
        print(f"HP {enemy.name} tersisa: {enemy.hp}")

    def gain_exp(self, amount):
        self.exp += amount
        print(f"{self.name} mendapatkan {amount} EXP")

        # Jika EXP mencapai 100 maka naik level
        if self.exp >= 100:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.exp = 0

        # Stat bertambah saat level up
        self.hp += 20
        self.atk += 5
        self.defense += 2

        print(f"\n{self.name} LEVEL UP!")
        print(f"Level sekarang: {self.level}")
        print(f"HP: {self.hp}")
        print(f"ATK: {self.atk}")
        print(f"DEF: {self.defense}")

    def to_dict(self):
        return {
            "name": self.name,
            "hp": self.hp,
            "atk": self.atk,
            "defense": self.defense,
            "level": self.level,
            "exp": self.exp
        }


# Membuat object player dan musuh
player = Character("Hero", 100, 25, 5)
zombie = Character("Zombie", 50, 10, 2)

# Simulasi attack
player.attack_enemy(zombie)

# Setelah menang mendapatkan EXP
player.gain_exp(100)

# Save data ke JSON
with open("character.json", "w") as file:
    json.dump(player.to_dict(), file, indent=4)

print("\nData character berhasil disimpan ke character.json")