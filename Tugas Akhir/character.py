#OOP CHARACTER
class Character:
    def __init__(self,name,char_class,hp,atk,defense,skill):
        self.name = name
        self.char_class = char_class
        self.hp = hp
        self.max_hp = hp
        self.atk = atk
        self.defense = defense
        self.skill = skill
        self.skill_cooldown = 0
        self.level = 1
        self.exp = 0
        self.floor = 1
        self.inventory = []
        self.equipped_item = None

    def to_dict(self): # turns it into a dictionary
        return {
            "name": self.name,
            "class": self.char_class,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "atk": self.atk,
            "def": self.defense,
            "skill": self.skill,
            "cooldown": self.skill_cooldown,
            "character_level": self.level,
            "exp": self.exp,
            "floor": self.floor,
            "inventory": self.inventory,
            "equipped_item": self.equipped_item
        }
    
    @classmethod
    def from_dict(cls, data): # turns data from dictionary to this
        player = cls(
            data["name"],
            data["class"],
            data["max_hp"],
            data["atk"],
            data["def"],
            data["skill"]
        )

        player.hp = data["hp"]
        player.skill_cooldown = data.get("cooldown",0)
        player.level = data["character_level"]
        player.exp = data["exp"]
        player.floor = data["floor"]
        player.inventory = data["inventory"]
        player.equipped_item = data["equipped_item"]

        return player