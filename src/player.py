import os
import textwrap
from room import Room

class Player():

    GAME_W = 48
    M_HELP = 1
    M_TITL = 2
    M_MAIN = 4
    M_INVT = 8
    M_EXAM = 16
    M_LOOK = 32
    M_QUIT = 64
    M_MENU = (M_HELP|M_EXAM|M_INVT|M_LOOK)
    
    def __init__(self, rooms={}, room_first=None):
        self.game_mode = Player.M_TITL #1=Help,2=Title,4=Main,8=Inventory (bitwise)
        self.game_end = False

        self.name = "New Player"
        self.rooms = {"title_screen": Room("Welcome", "Type 'start' and your name to begin playing!", screen="title.txt")}
        self.rooms.update(rooms)
        self.room_first = room_first
        print(self.rooms)
        self.room_current = self.rooms["title_screen"]
        self.items = []
        self.item_last = None
        self.hp_max = 20
        self.hp = 15

        self.splash_text = ""
        self.error_text = ""
        with open(f"{os.getcwd()}\\txt\\title.txt", encoding="UTF-8") as f:
            self.title_screen_text = f.read()

    def get_input(self):
        print("What will you do?")
        text_input = input(">").split(" ") # Get input and split it 
        cmd = text_input[0].lower() # Get command
        arg = ""
        if len(cmd) > 0:
            arg = " ".join(text_input[1:]).lower() # Set argument if available
        self.process_input(cmd, arg) # Process command
    
    def process_input(self, cmd, arg):
        self.error_text = "[Unknown command. Type 'help' for all commands.]" # Default "error"
        if cmd == "help": # Set immediately to help mode if need to
            self.cmd_help(0)

        all_cmds = ["quit"] # List of all commands
        if cmd == "quit": # Quit game
            self.cmd_quit()
        if self.game_mode & Player.M_MENU: # Close menus
            all_cmds += ["back"]
            if cmd == "back": # Go back
                self.cmd_menu_disable()
        if self.game_mode & Player.M_TITL: # Title Screen commands
            all_cmds += ["start", "credits"]
            if cmd == "start": # Start game
                self.cmd_start(arg)
            elif cmd == "credits": # Credits
                self.cmd_credits()
        else: 
            if self.game_mode & Player.M_MAIN: # Main game commands
                all_cmds += ["move", "look", "inv", "take", "use", "drop", "examine"]
                if cmd == "move": # Moving
                    self.cmd_move(arg)
                elif cmd == "inv": # Inventory
                    self.cmd_inv_enable()
                elif cmd == "take": # Take Item
                    self.cmd_item_pickup(arg)
                elif cmd == "look": # Take Item
                    self.cmd_room_look_at()
                elif cmd == "drop": # Drop Item
                    self.cmd_item_drop(arg)
                elif cmd == "use": # Use Item
                    self.cmd_item_use(arg)
                elif cmd == "examine": # Examine Item
                    self.cmd_item_examine(arg)

        if self.game_mode & Player.M_HELP: # If in help mode, print all commands
            self.cmd_help(all_cmds)

    def cmd_room_look_at(self):
        self.cmd_help_clear()
        self.error_text = ""
        self.game_mode |= Player.M_LOOK # Set room look flag

    def cmd_inv_enable(self):
        self.cmd_help_clear()
        self.game_mode |= Player.M_INVT # Set Inventory flag
        self.error_text = ""

    def cmd_menu_disable(self):
        if self.game_mode & Player.M_HELP:
            self.game_mode &= ~Player.M_HELP
        elif self.game_mode & Player.M_EXAM:
            self.game_mode &= ~Player.M_EXAM
        elif self.game_mode & Player.M_INVT:
            self.game_mode &= ~Player.M_INVT 
        elif self.game_mode & Player.M_LOOK:
            self.game_mode &= ~Player.M_LOOK
        self.error_text = ""

    def cmd_help(self,l):
        if l == 0:
            self.game_mode = self.game_mode | Player.M_HELP
        elif type(l) == list:
            self.error_text = ""
            self.splash_text = f"All Commands: {', '.join(l)}"

    def cmd_move(self, dir):
        self.cmd_help_clear()
        if dir == "":
            self.error_text = "[Please specify a direction.]"
        else:
            if dir in self.room_current.rooms_to: # Check if direction in room
                if self.room_current.rooms_to[dir] == None:
                    self.error_text = "[No paths in this direction.]"
                else:
                    self.error_text = ""
                    self.room_current = self.room_current.rooms_to[dir]
                    self.cmd_menu_reset()
            else:
                self.error_text = "[Please specify a direction.]"

    def cmd_start(self, name):
        self.cmd_help_clear()
        if name == "":
            self.error_text = "[Please enter a name.]"
        else:
            self.error_text = ""
            self.name = name.title()[:8]
            self.game_mode = Player.M_MAIN
            self.room_current = self.room_first
        
    def cmd_quit(self):
        self.game_mode |= Player.M_QUIT

    def cmd_credits(self):
        self.cmd_help_clear()
        self.error_text = "[Created by: Rosie LaSota]"
    
    def cmd_item_use(self, name):
        self.cmd_help_clear()
        if self.items:
            if name == "it" and self.item_last:
                self.item_last.on_use(self)
            else:
                for i in self.items:
                    if i.name.lower() == name:
                        i.on_use(self)
                        break
        else:
            self.error_text = "[You do not have that.]"

    def cmd_help_clear(self):
        self.game_mode &= ~Player.M_HELP

    def cmd_menu_reset(self):
        self.game_mode &= ~Player.M_MENU

    def cmd_item_pickup(self, name):
        self.cmd_help_clear()
        if self.room_current.items:
            for i in self.room_current.items:
                if i.name.lower() == name:
                    i.on_pickup(self)
                    break
        else:
            self.error_text = "[That item is not in this room.]"

    def cmd_item_examine(self, name):
        self.cmd_help_clear()
        if self.items:
            if name == "it" and self.item_last:
                self.item_last.on_examine(self)
            else:
                for i in self.items:
                    if i.name.lower() == name:
                        i.on_examine(self)
                        break
        else:
            self.error_text = "[You do not have that item.]"

    def cmd_item_drop(self, name):
        self.cmd_help_clear()
        if self.items:
            if name == "it" and self.item_last:
                self.item_last.on_drop(self)
            else:
                for i in self.items:
                    if i.name.lower() == name:
                        i.on_drop(self)
                        break
        else:
            self.error_text = "[You do not have that item.]"

    def get_info(self):
        print(f"╔{'═'*(Player.GAME_W-2)}╗")
        padding = int(Player.GAME_W/2-3)
        print(f"║ {self.name.ljust(padding)}  {f'HP: {self.hp}/{self.hp_max}'.rjust(padding)} ║")
        print(f"╠{'═'*(Player.GAME_W-2)}╣")

    def run(self):
        while not self.game_mode & Player.M_QUIT:
            os.system("cls")
            self.get_info()
            print(self.room_current.screen)
            if not self.game_mode & Player.M_HELP: # Check if not in help
                if self.game_mode & (Player.M_TITL | Player.M_MAIN):
                    self.splash_text = str(self.room_current)
                if self.game_mode & Player.M_LOOK: # Show items in room
                    if len(self.room_current.items) == 0:
                        self.splash_text = "There are no items in this room."
                    else:
                        self.splash_text = f"Items in Room: {', '.join([item.name for item in self.room_current.items])}"
                if self.game_mode & Player.M_INVT: # Show inventory
                    if len(self.items) == 0:
                        self.splash_text = "Inventory: You have no items."
                    else:
                        self.splash_text = f"Inventory: {', '.join([item.name for item in self.items])}"
                if self.game_mode & Player.M_EXAM: # Show item stats
                    if self.item_last:
                        self.splash_text = str(self.item_last)
                    else:
                        self.splash_text = "Something wrong has occurred."
            self.splash_text = textwrap.fill(self.splash_text, Player.GAME_W)
            print(self.splash_text+("\n"*(3-self.splash_text.count("\n"))))
            print(self.error_text)
            self.get_input()
        os.system("cls")
        print("Thanks for playing!")
        exit()
            