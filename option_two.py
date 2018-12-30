import discord
import logging
from discord.ext import commands
import random
from prettytable import PrettyTable
import yaml

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord_two.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix='?')
total_players = 0
player_list = []
notify_list = []
team_one = []
team_two = []

with open('config.yml', 'r') as stream:
    config = yaml.safe_load(stream)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    
#---- helper functions ----
def lobby_exist():
    async def predicate(ctx):
        if total_players != 0:
            return True
        else:
            await ctx.send("Create a lobby first before using this command")
            return False
    return commands.check(predicate)

def full(): #True = too many people
    '''checking if there's too many people in list'''
    return len(player_list) == total_players

def concatenate_players(player_list):
    '''converts Member models to strings'''
    string_list = []
    for player in player_list:
        string_list.append(str(player))
    return string_list

async def check_list(ctx, member):#true = is in lobby already
    '''checks if player is in lobby already'''
    for player in player_list:
        if member == player:
            await ctx.send("You're already in the lobby")
            return True 
    return False


def shuffle():
    '''puts players into teams'''
    random.shuffle(player_list)
    global team_one
    global team_two

    team_one = []
    team_two = []
    
    for x in range(len(player_list)):
        if x < (total_players / 2):
            team_one.append(player_list[x])
        else:
            team_two.append(player_list[x])
    
    str_teamone = concatenate_players(team_one)
    str_teamtwo = concatenate_players(team_two)
    return concatenate_teams(str_teamone, str_teamtwo)

def concatenate_teams(team1:list, team2:list):
    table =  PrettyTable()
    
    table.add_column("Team 1", team1)
    table.add_column("Team 2", team2)
    
    table.align = "c"

    return table.get_string()

async def notify_players(ctx):
    mention_str = ""
    for player in notify_list:
        mention_str += " " + player.mention
    await ctx.send("The game is ready" + mention_str)

async def spots_left(ctx):
    await ctx.send(str((total_players) - len(player_list)) + " spot(s) left")

def check_team(player: discord.Member, team: list):
    for x in team:
        if player == x:
            return True
    return False

#---- commands ----

@bot.command()
async def create(ctx, num_players:int):
    if num_players % 2 > 0:
        await ctx.send("You need an even # of players to play")
    else:
        global total_players
        total_players = num_players
        await ctx.send("Lobby created for " + total_players + " total players.")
@create.error
async def create_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You need to input the total # of players")
    
@bot.command()
@lobby_exist()
async def join(ctx):
    '''Join the lobby'''
    if (not full()):
        player_list.append(ctx.author)
        await ctx.send(str(ctx.author) + " has joined!")
        await spots_left(ctx)
    else:
        ctx.send("Bro, there's too many people")

@bot.command()
@lobby_exist()
async def add(ctx, *players:discord.Member):
    '''Add a player to the lobby'''
    if (not full()):
        for x in players:
            player_list.append(x)
            await ctx.send(str(x) + " has been added!")
        await spots_left(ctx)
    else:
        ctx.send("Bro, there's too many people")

@bot.command()
async def start(ctx):
    '''Starts the lobby'''
    if full():
        result = shuffle()
        await ctx.send("Here are the teams\n```" + result + "```")
        if (len(notify_list) > 0):
            await notify_players(ctx)
    else:
        await ctx.send("You don't have enough players")

@add.error
async def tenmans_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Sorry, can't find that member. Did you not use @someone?")

@bot.command(name='shuffle')
@lobby_exist()
async def reshuffle(ctx):
    '''Shuffles the existing teams.'''
    result = shuffle()
    await ctx.send("Reshuffled the teams\n```" + result + "```")


@bot.command()
@lobby_exist()
async def leave(ctx):
    '''Leave the lobby.'''
    player_list.remove(ctx.author)
    try: 
        notify_list.remove(ctx.author)
    except:
        pass #intentionally pass this exception
    
    await ctx.send(str(ctx.author) + " has left the lobby")

@bot.command()
@lobby_exist()
async def remove(ctx, member: discord.Member):
    '''Remove a person from the lobby.'''
    player_list.remove(member)
    try:
        notify_list.remove(member)
    except:
        pass
    
    await ctx.send("Removed " + str(member) + " from the lobby.")
    
@bot.command()
@lobby_exist()
async def showlist(ctx):
    '''Displays the lobby in a table.'''
    table = PrettyTable()
    table.add_column("Players", await concatenize_players(player_list))
    await ctx.send("```" + table.get_string() + "```")

@bot.command()
async def reset(ctx):
    '''Clears the lobby.'''
    global total_players
    total_players = 0
    team_one.clear()
    team_two.clear()
    player_list.clear()
    notify_list.clear()
    await ctx.send("Resetting player lobby...")

@bot.command()
@lobby_exist()
async def notifyme(ctx):
    '''The bot will @you when the lobby is full.'''
    notify_list.append(ctx.author)
    await ctx.send("I'll let you know when the game is starting")

@bot.command()
@lobby_exist()
async def showteams(ctx):
    '''Displays the current teams'''
    num_team_members = total_players / 2
    str_teamone = concatenate_players(team_one)
    str_teamtwo = concatenate_players(team_two)
    if (len(team_one) == num_team_members and len(team_two) == num_team_members):
        await ctx.send("```" + concatenate_teams(str_teamone, str_teamtwo) + "```")
    else:
        await ctx.send("Teams haven't been made / not enough players.")

@bot.command()
@lobby_exist()
async def swap(ctx, player1: discord.Member, player2: discord.Member):
    '''Swaps two players on opposite teams'''
    if ((check_team(player1, team_one) and check_team(player2, team_two))):
        team_one.remove(player1)
        team_one.append(player2)
        team_two.append(player1)
        team_two.remove(player2)
        await ctx.send("Swapped " + str(player1) + " and " + str(player2))
    elif ((check_team(player1, team_two) and check_team(player2, team_one))):
        team_one.remove(player2)
        team_one.append(player1)
        team_two.append(player2)
        team_two.remove(player1)
        await ctx.send("Swapped " + str(player1) + " and " + str(player2))
    else:
        await ctx.send("Are you sure that these two are on opposite teams?")

@bot.command()
async def shutdown(ctx):
    await ctx.send("Shutting down...")
    await bot.logout()

bot.run(config['configurations']['token'])

