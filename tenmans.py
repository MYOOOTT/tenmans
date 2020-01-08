import discord
from discord.ext import commands
from prettytable import PrettyTable
from team import Team
from lobby import Lobby

class Scrim(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.lobby = None

    #--- helper functions ---#
    ##########################

    def stringify_teams(self, team1:list, team2:list):
        table = PrettyTable()

        table.add_column("Team 1", team1)
        table.add_column("Team 2", team2)

        table.align = "c"
        return table.get_string()

    '''  THIS NEEDS TO BE IMPLEMENTED IN THE FUTURE
    def lobby_exist(func):
        def wrapper(self, *args, **kwargs):
            assert self.lobby != None, "Make sure lobby exists before doing something!"
            func(self, *args, **kwargs)
        return wrapper

    '''

    #--- commands ---#
    ##################

    @commands.command()
    async def create(self, ctx, num_players:int):
        '''starts up the lobby, use number of TOTAL players.'''
        if type(num_players) == int or num_players // 2 != 0:
            await ctx.send("Lobby created for " + str(num_players) + " total players. Join now!")
            self.lobby = Lobby(num_players)
        else:
            raise commands.UserInputError

    @create.error
    async def create_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to input the number of players on each team.")
        elif isinstance(error, commands.UserInputError):
            await ctx.send("Either you put in an odd number or didn't put in a number. Try again.")
        else:
            await ctx.send("Unforeseen error.")
            print(error)
    
    @commands.command()
    #@lobby_exist
    async def join(self, ctx):
        assert self.lobby != None, "Make sure the lobby exists first!"
        self.lobby.add(str(ctx.author))
        await ctx.send(str(ctx.author) + " has joined!")
    
    @join.error
    async def join_error(self, ctx, error):
        if isinstance(error, AssertionError):
            await ctx.send(error.message)
        else:
            print(error)
            await ctx.send("Unexpected error. Try again maybe?")

    
