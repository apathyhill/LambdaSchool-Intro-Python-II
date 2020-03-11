import os

class Room():
    def __init__(self, name, desc, screen="outside.txt"):
        self.name = name
        self.desc = desc
        self.rooms_to = {"n": None, "s": None, "e": None, "w": None}
        with open(f"{os.getcwd()}\\txt\\{screen}", encoding="UTF-8") as f:
            self.screen = f.read()
