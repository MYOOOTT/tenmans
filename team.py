import discord
import random

class Team():
    def __init__(self, max):
        self.max = max
        self.players = []
    
    def get_players(self):
        return self.players
    
    def add(self, player): 
        assert len(self.players) + 1 <= self.max, "Too many players!"
        assert not player in self, "This player already exists in this team."
        self.players.append(player)

    def remove(self, player):
        self.players.remove(player)

    def shuffle(self):
        random.shuffle(self.players)

    def __contains__(self, player):
        return player in self.players

    def __iter__(self):
        return iter(self.players)
    
    def __str__(self):
        return str(self.players)