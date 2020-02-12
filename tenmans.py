import discord
from discord.ext import commands
from prettytable import PrettyTable
from team import Team
from lobby import Lobby
import re

class Scrim(commands.Cog):
    pattern_object = re.compile(r"<@!(\d*)>")
    CREATE_LOBBY_MESSAGE = "Be sure to create a lobby first using the `?create` command!"

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

    def extract_id(self, players):
        new_list = []
        for person in players:
            matched = re.match(Scrim.pattern_object, person)
            if matched:
                print("Searching for USER with this ID:", matched.group(1))
                user = self.bot.get_user(int(matched.group(1)))
                new_list.append(user.name)
            else:
                new_list.append(person)
        
        return new_list


    #--- commands ---#
    ##################

    @commands.command()
    async def create(self, ctx, num_players:int):
        '''Starts up the lobby, use number of TOTAL players.'''
        self.lobby = Lobby(num_players)
        await ctx.send("Lobby created for " + str(num_players) + " total players. Use ?join to enter now or ?add NAME_HERE to add someone!")

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
        '''Join an existing lobby.'''
        self.lobby.add(str(ctx.author.name))
        if self.lobby.spots_left() == 0:
            spots_message = "Lobby is now at max capacity (" + str(self.lobby.max) + ")." 
        else:
            spots_message = str(self.lobby.spots_left()) + " player(s) can join."
        await ctx.send(str(ctx.author.name) + " has joined!" + " " + spots_message)
    
    @join.error
    async def join_error(self, ctx, error):
        if isinstance(error.original, AttributeError):
            await ctx.send(Scrim.CREATE_LOBBY_MESSAGE)
        elif isinstance(error.original, AssertionError):
            await ctx.send(error.original.args)
        else:
            print(error)
            await ctx.send("Unexpected error. Try again maybe?")

    @commands.command()
    async def add(self, ctx, player, *args):
        '''Add another player by @ing them or with a custom name.'''
        total_players = (player,) + args #to consider player a part of a tuple
        print("Before extract id:" ,str(total_players))
        total_players = self.extract_id(total_players)
        self.lobby.add(*total_players)
        await ctx.send("Added " + str(total_players) + ".")

    
        
    @commands.command()
    async def clear(self, ctx):
        '''Reset the lobby.'''
        self.lobby = None
        await ctx.send("Lobby cleared.")
    
    @commands.command()
    async def remove(self, ctx, player):
        '''Removes another player. This command is case sensitive!'''
        self.lobby.remove(player)
        await ctx.send("Removed " + str(player))
    
    @remove.error 
    async def remove_error(self, ctx, error):
        if isinstance(error.original, AttributeError):
            await ctx.send(Scrim.CREATE_LOBBY_MESSAGE)
        if isinstance(error.original, AssertionError):
            await ctx.send(error.original.args)
        elif isinstance(error.original, ValueError):
            await ctx.send("Player is not in the list! Usernames are case senstive!")
        else:
            print(error)
            await ctx.send("Unexpected error. Try again maybe?")

    @commands.command()
    async def showlist(self, ctx):
        '''Outputs a list of the players in the lobby.'''
        table = PrettyTable()
        table.add_column("Players", self.lobby.player_list)
        await ctx.send("```" + table.get_string() + "```")
    
    @showlist.error 
    async def showlist_error(self, ctx, error):
        if isinstance(error.original, AttributeError):
            await ctx.send(Scrim.CREATE_LOBBY_MESSAGE)
        elif isinstance(error.original, AssertionError):
            await ctx.send(error.original.args)
        else:
            print(error)
            await ctx.send("Unexpected error. Try again maybe?")

    @commands.command()
    async def showteams(self, ctx):
        '''Outputs a table of the teams.'''
        table = PrettyTable()
        table.add_column("Team 1", self.lobby.get_team_one().get_players())
        table.add_column("Team 2", self.lobby.get_team_two().get_players())
        await ctx.send("```" + table.get_string() + "```")
    
    @showteams.error 
    async def showteam_error(self, ctx, error):
        if isinstance(error.original, AttributeError):
            await ctx.send(Scrim.CREATE_LOBBY_MESSAGE)
        elif isinstance(error.original, AssertionError):
            await ctx.send(error.original.args)
        else:
            print(error)
            await ctx.send("Unexpected error. Try again maybe?")

    @commands.command()
    async def swap(self, ctx, player1, player2):
        '''Swaps two players on opposite teams.'''
        self.lobby.swap(player1, player2)
        await ctx.invoke(self.showteams)
    
    @swap.error 
    async def swap_error(self, ctx, error):
        if isinstance(error.original, AttributeError):
            await ctx.send(Scrim.CREATE_LOBBY_MESSAGE)
        if isinstance(error.original, AssertionError):
            await ctx.send(error.original.args)
        elif isinstance(error.original, ValueError):
            await ctx.send("Player is not in the team(s)! Usernames are case senstive!")
        else:
            print(error)
            await ctx.send("Unexpected error. Try again maybe?")

    @commands.command()
    async def shuffle(self, ctx):
        '''Shuffles the lobby.'''
        self.lobby.shuffle()
        await ctx.invoke(self.showteams)
    