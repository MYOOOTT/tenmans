import discord
import random

class Team():
    def __init__(self, max):
        self.max = max
        self.players = []
    
    def get_players(self):
        return self.players
    
    #one positional parameter to enforce that at least one player has to be added
    def add(self, player, *args): #args = multiple players
        total_players = (player,) + args #comma to indicate it is a tuple
        for person in total_players:
            assert not person in self, "Player '" + str(person) + "' already exists in this team."
            assert len(self.players) + 1 <= self.max, "Team has exceeded capacity."
            self.players.append(person)

    def remove(self, player):
        self.players.remove(player)

    def shuffle(self):
        random.shuffle(self.players)

    def clear(self):
        self.players.clear()

    def __contains__(self, player):
        return player in self.players

    def __iter__(self):
        return iter(self.players)
    
    def __str__(self):
        return str(self.players)
