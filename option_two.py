import discord
import logging
from discord.ext import commands
import random
from prettytable import PrettyTable

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord_two.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


bot = commands.Bot(command_prefix='?')
player_list = []

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

#---- commands ----
    
@bot.command()
async def tenmans(ctx, *, player: discord.Member=None):
    if (await check_length(ctx)):
        if player == None: #no extra parameter
            await ctx.send(str(ctx.author) + " has joined!")
            player_list.append(ctx.author)
        else:
            await ctx.send(str(player) + " has been added!")
            player_list.append(player)
        await ctx.send(str(10 - len(player_list)) + " spot(s) left")

@bot.command()
async def showlist(ctx):
    table = PrettyTable()
    table.add_column("Players", await concatenize_players(player_list))
    await ctx.send("```" + table.get_string() + "```")

@bot.command()
async def clear(ctx):
    player_list.clear()
    await ctx.send("Clearing player lobby...")

#---- helper functions ----
async def check_length(ctx): #False = too many people
    '''checking if there's too many people in list'''
    if len(player_list) >= 10:
        await ctx.send("Sorry bud, there's too many people")
        return False
    else:
        return True

async def concatenize_players(player_list):
    string_list = []
    for player in player_list:
        string_list.append(str(player))
    return string_list

bot.run('NTIyNDU4Mzk2NjI5MjcwNTMx.DvLRJA.L1O1cqEIylU8WqVSA2EEDyl3htw')

