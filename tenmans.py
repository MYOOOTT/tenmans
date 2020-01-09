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

    #--- commands ---#
    ##################

    @commands.command()
    async def create(self, ctx, num_players:int):
        '''starts up the lobby, use number of TOTAL players.'''
        if type(num_players) == int or num_players % 2 != 0:
            await ctx.send("Lobby created for " + str(num_players) + " total players. Join now!")
            self.lobby = Lobby(num_players)
        else:
            raise commands.UserInputError

    @create.error
    async def create_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to input the number of players on each team.")
        elif isinstance(error.original, AssertionError):
            await ctx.send("Uneven amount of players. This is the TOTAL amount of players, so it should be even!")
        else:
            await ctx.send("Unforeseen error.")
            print(str(type(error)))
            print(error)
    
    @commands.command()
    async def join(self, ctx):
        self.lobby.add(str(ctx.author))
        if self.lobby.spots_left() == 0:
            spots_message = "Lobby is now at max capacity (" + str(self.lobby.max) + ")." 
        else:
            spots_message = str(self.lobby.spots_left()) + " player(s) can join."
        await ctx.send(str(ctx.author) + " has joined!" + " " + spots_message)
    
    @join.error
    async def join_error(self, ctx, error):
        if isinstance(error.original, AttributeError):
            await ctx.send("Be sure to create a lobby first!")
        else:
            print(error)
            await ctx.send("Unexpected error. Try again maybe?")

    @commands.command()
    async def clear(self, ctx):
        self.lobby = None
        await ctx.send("Lobby cleared.")

    

    
