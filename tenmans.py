import discord
from discord.ext import commands
from prettytable import PrettyTable
from team import Team

class Scrim(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.team_one = None
        self.team_two = None

    #--- helper functions ---#
    ##########################

    def stringify_teams(self, team1:list, team2:list):
        table = PrettyTable()

        table.add_column("Team 1", team1)
        table.add_column("Team 2", team2)

        table.align = "c"
        return table.get_string()

    #--- commands ---#
    ##################

    @commands.command()
    async def create(self, ctx, num_players:int):
        '''Creates the lobby, use number of players on each team, not total.'''
        if type(num_players) == int:
            await ctx.send("Lobby created for " + str(num_players) + " players on each team. Join now!")
            self.team_one = Team(num_players)
            self.team_two = Team(num_players)
        else:
            raise commands.UserInputError

    @create.error
    async def create_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to input the number of players on each team.")
        elif isinstance(error, commands.UserInputError):
            await ctx.send("That's not a number, input the number of players on each team.")
        else:
            await ctx.send("Unforeseen error.")
            print(error)

    

    
    
