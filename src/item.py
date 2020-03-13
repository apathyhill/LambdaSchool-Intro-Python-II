from player import Player

class Item():
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc

    def on_pickup(self, player):
        player.items.append(self)
        player.room_current.items.remove(self)
        player.item_last = self
        player.error_text = f"[You picked up ({self.name})]"

    def on_use(self, player):
        player.error_text = f"[You cannot use this.]"

    def on_drop(self, player):
        player.items.remove(self)
        player.room_current.items.append(self)
        player.item_last = None
        player.error_text = f"[You dropped ({self.name})]"

    def __str__(self):
        return f"{self.name}: {self.desc}"

class Food(Item):
    def __init__(self, name, desc, hp):
        super().__init__(name, desc)
        self.name = name
        self.desc = desc
        self.hp = hp

    def on_use(self, player):
        player.hp = min(player.hp+self.hp, player.hp_max)
        player.error_text = f"[You ate it and got {self.hp} HP!]"
        player.items.remove(self)
        player.item_last = None
        player.game_mode &= ~Player.M_EXAM

    def on_examine(self, player):
        player.error_text = ""
        player.game_mode |= Player.M_EXAM
        player.item_last = self

    def __str__(self):
        return f"[{self.name}: {self.desc} Heals {self.hp} HP.]"