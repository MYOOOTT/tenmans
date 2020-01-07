from team import Team
import random

class Lobby():
    def __init__(self, max):
        self.player_list = []
        self.max = max
        self.ON_EACH_TEAM = max / 2
        self.team_one = Team(self.ON_EACH_TEAM)
        self.team_two = Team(self.ON_EACH_TEAM)

    def add(self, player, *args): #args = multiple players
        total_players = (player,) + args #comma to indicate it is a tuple
        for person in total_players:
            assert not person in self, "Player '" + str(person) + "' already exists in the lobby."
            assert len(self.players) + 1 <= self.max, "Lobby at max capacity."
            self.player_list.append(person)


    def remove(self, player):
        self.player_list.remove(player)
        if not (player in self.team_one and player in self.team_two):
            raise ValueError

        try:
            self.team_one.remove(player)
        except ValueError:
            self.team_two.remove(player)
        except Exception as e:
            raise e

    def shuffle(self):
        self.team_one.clear()
        self.team_one.clear()
        random.shuffle(player_list)

        for x in range(len(player_list)):
            if x < (self.max / 2):
                team_one.append(player_list[x])
            else:
                team_two.append(player_list[x])
        
    def get_team_one(self):
        return self.team_one

    def get_team_two(self):
        return self.team_two
    