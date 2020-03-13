import os

class Room():
    def __init__(self, name, desc, items=[], screen="outside.txt"):
        self.name = name
        self.desc = desc
        self.items = items
        self.rooms_to = {"n": None, "s": None, "e": None, "w": None}
        with open(f"{os.getcwd()}\\txt\\{screen}", encoding="UTF-8") as f:
            self.screen = f.read()
    def __str__(self, mode=0):
        return f"{self.name}: {self.desc}"
    def get_screen(self):
        return self.screen