import os
from player import Player
from room import Room
from item import Item, Food

os.chdir(os.path.dirname(__file__))

items = {
    "burger": Food("Burger", "An abandoned hamburger.", 5)
}

rooms = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons."),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east.""", items=[items["burger"]]),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm."""),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air."""),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south."""),
}

# Link rooms together
rooms["outside"].rooms_to["n"] = rooms["foyer"]
rooms["foyer"].rooms_to["s"] = rooms["outside"]
rooms["foyer"].rooms_to["n"] = rooms["overlook"]
rooms["foyer"].rooms_to["e"] = rooms["narrow"]
rooms["overlook"].rooms_to["s"] = rooms["foyer"]
rooms["narrow"].rooms_to["w"] = rooms["foyer"]
rooms["narrow"].rooms_to["n"] = rooms["treasure"]
rooms["treasure"].rooms_to["s"] = rooms["narrow"]

Player = Player(rooms=rooms, room_first=rooms["outside"])
Player.run()