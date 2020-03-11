import os
import textwrap

os.chdir(os.path.dirname(__file__))

class Player():
    def __init__(self, rooms={}, room_current=None):
        self.game_width = 48
        self.game_mode = 0
        self.game_end = False
        self.name = ""
        self.rooms = rooms
        self.inv = []
        self.score = 0
        self.room_current = room_current
        self.splash_text = textwrap.fill("Type 'start' aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaand your name to start playing!", 32)
        self.error_text = ""
        with open(f"{os.getcwd()}\\txt\\title.txt", encoding="UTF-8") as f:
            self.title_screen_text = f.read()

    def get_input(self):
        print("What will you do?")
        text_input = input(">").split(" ")
        cmd = text_input[0].lower()
        arg = ""
        if len(cmd) > 0:
            arg = " ".join(text_input[1:]).lower()
        self.process_input(cmd, arg)
        
    def process_input(self, cmd, arg):
        self.error_text = "[Unknown command.]"
        if cmd in ["q", "quit", "exit", "end"]: # Global
            self.game_end = True
            return
        if self.game_mode == 0: # Title Screen-only
            if cmd == "start":
                if arg == "":
                    self.error_text = "[Please enter a name.]"
                else:
                    self.error_text = ""
                    self.name = arg.title()[:8]
                    self.game_mode = 1
            elif cmd == "credits":
                self.error_text = "[Created by: Rosie LaSota]"
            else:
                self.error_text = "[Unknown command.]"
            return
        else: 
            if self.game_mode == 1:
                if cmd == "move":
                    if arg == "":
                        self.error_text = "[Please specify a direction.]"
                    else:
                        if arg in self.room_current.rooms_to:
                            if self.room_current.rooms_to[arg] == None:
                                self.error_text = "[No paths in this direction.]"
                            else:
                                self.error_text = ""
                                self.room_current = self.room_current.rooms_to[arg]
                        else:
                            self.error_text = "[Please specify a direction.]"
                elif cmd == "inv":
                    self.game_mode = 2
                    self.error_text = ""
            elif self.game_mode == 2: # Inventory
                if cmd == "aa":
                    print("a")
            return

    def get_info(self):
        print("/"+ ("="*(self.game_width-2)) + "\\")
        print(f"| {self.name.ljust(int(self.game_width/2-3))}  {str(self.score).rjust(int(self.game_width/2-3))} |")
        print("|"+ ("="*(self.game_width-2)) + "|")

    def run(self):
        os.system("cls")
        while not self.game_end:
            if self.game_mode == 0: # Title Screen
                print(self.title_screen_text)
            else:
                self.get_info()
                if self.game_mode == 1:
                    self.splash_text = f"{self.room_current.name}: {self.room_current.desc}"
                elif self.game_mode == 2:
                    if len(self.inv) == 0:
                        self.splash_text = "Inventory: You have no items."
                    else:
                        self.splash_text = f"Inventory: {', '.join([item.name for item in self.inv])}"
                print(self.room_current.screen)
            
            self.splash_text = textwrap.fill(self.splash_text, self.game_width)
            print(self.splash_text+("\n"*(3-self.splash_text.count("\n"))))
            print(self.error_text)
            self.get_input()