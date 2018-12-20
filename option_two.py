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
notify_list = []
player_list = []
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

#---- commands ----
@bot.command()
async def tenmans(ctx, *players: discord.Member): 
    '''Create/join a ten man lobby.''' 
    global total_players #to avoid unboundlocal error
    if (await check_length(ctx)): 
        if len(players) == 0: #no extra parameter
            await ctx.send(str(ctx.author) + " has joined!")
            total_players += 1
            player_list.append(ctx.author)
        else:
            for x in players:
                await ctx.send(str(x) + " has been added!")
                total_players += 1
                player_list.append(x)
        await ctx.send(str(10 - total_players) + " spot(s) left")

        if (10 - total_players == 0):
            await shuffle(ctx)
            if (len(notify_list) > 0):
                await notify_players(ctx)

@bot.command()
async def team1(ctx, *players: discord.Member):
    global total_players
    if (await check_length(ctx)): 
        if len(players) == 0: 
            await ctx.send(str(ctx.author) + " has joined team one!")
            total_players += 1
            team_one.append(ctx.author)
        else:
            for x in players:
                await ctx.send(str(x) + " has been added to team one!")
                total_players += 1
                team_one.append(x)
        await ctx.send(str(10 - total_players) + " spot(s) left")

    if (10 - total_players == 0):
        await shuffle(ctx)
        if (len(notify_list) > 0):
            await notify_players(ctx)

@bot.command()
async def team2(ctx, *players: discord.Member):
    global total_players
    if (await check_length(ctx)): 
        if len(players) == 0: 
            await ctx.send(str(ctx.author) + " has joined team two!")
            total_players += 1
            team_two.append(ctx.author)
        else:
            for x in players:
                await ctx.send(str(x) + " has been added to team two!")
                total_players += 1
                team_two.append(x)
        await ctx.send(str(10 - total_players) + " spot(s) left")

    if (10 - total_players == 0):
        await shuffle(ctx)
        if (len(notify_list) > 0):
            await notify_players(ctx)

@tenmans.error
async def tenmans_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Sorry, can't find that member. Did you not use @someone?")

@bot.command(name='shuffle') #reason for existing:
async def reshuffle(ctx): #commands cannot call other commands
    '''Shuffles the existing teams.'''
    await shuffle(ctx)

@bot.command()
async def leave(ctx):
    '''Leave the lobby.'''
    player_list.remove(ctx.author)
    try: 
        notify_list.remove(ctx.author)
    except:
        pass #intentionally pass this exception
    
    await ctx.send(str(ctx.author) + " has left the lobby")

@bot.command()
async def remove(ctx, member: discord.Member):
    '''Remove a person from the lobby.'''
    player_list.remove(member)
    try:
        notify_list.remove(member)
    except:
        pass
    
    await ctx.send("Removed " + str(member) + " from the lobby.")
    
@bot.command()
async def showplayers(ctx):
    '''Displays the entire player lobby in a table.'''
    table = PrettyTable()
    player_list.extend(team_one)
    player_list.extend(team_two)
    table.add_column("Players", await concatenize_players(player_list))
    await ctx.send("```" + table.get_string() + "```")

@bot.command()
async def showteams(ctx):
    '''Displays the teams.'''
    team1 = PrettyTable()
    team2 = PrettyTable()
    team1.add_column("Team 1", await concatenize_players(team_one))
    team2.add_column("Team 2", await concatenize_players(team_two))
    await ctx.send("```" + team1.get_string() + "\n" + team2.get_string() + "```")

@bot.command()
async def clear(ctx):
    '''Clears the lobby.'''
    player_list.clear()
    notify_list.clear()
    team_one.clear()
    team_two.clear()
    total_players = 0 
    await ctx.send("Clearing player lobby...")

@bot.command()
async def notifyme(ctx):
    '''The bot will @you when the lobby is full.'''
    notify_list.append(ctx.author)
    await ctx.send("I'll let you know when the game is starting")

@bot.command()
async def shutdown(ctx):
    await ctx.send("Shutting down...")
    await bot.logout()

#---- helper functions ----
async def check_length(ctx): #False = too many people
    '''checking if there's too many people in list'''
    if total_players >= 10:
        await ctx.send("Sorry bud, there's too many people")
        return False

    else:
        return True

async def concatenize_players(player_list):
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

async def shuffle(ctx): #might be good to check if lobby is full or not
    '''puts players into teams'''
    str_players = await concatenize_players(player_list)
    random.shuffle(str_players)
    
    for x in range(len(str_players)):
        if len(team_one) != 5: #hardcoded, should be changed later
            team_one.append(str_players[x])
        else:
            team_two.append(str_players[x])

    table = PrettyTable()
    table.add_column("Team 1", team_one)
    table.add_column("Team 2", team_two)
    table.align = "c"

    result = table.get_string(title="T E N M A N S")
    await ctx.send("Here are the teams\n```" + result + "```")

async def notify_players(ctx):
    mention_str = ""
    for player in notify_list:
        mention_str += " " + player.mention
    await ctx.send("The game is ready" + mention_str)
    
bot.run(config['configurations']['token'])

