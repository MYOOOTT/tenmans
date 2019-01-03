import discord
import logging
from discord.ext import commands
import random
from prettytable import PrettyTable

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord_one.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


bot = commands.Bot(command_prefix='?')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def scramble_teams(ctx, *, arg):
    player_list = ctx.message.content.split()
    player_list.pop(0) #first index includes the command itself
    if len(player_list) > 10:
        print(player_list)
        await ctx.send("Ya got too many people. Try again.")
    elif len(player_list) < 10:
        await ctx.send("Did you miss someone?")
    else:
        random.shuffle(player_list)
        team_one = []
        team_two = []
        for x in range(len(player_list)):
            if x < 5:
                team_one.append(player_list[x])
            else:
                team_two.append(player_list[x])
                
        table = PrettyTable()
        table.add_column("Team 1", team_one)
        table.add_column("Team 2", team_two)
        table.align = "c"

        result = table.get_string(title="T E N M A N S")
        print(result)
        await ctx.send("```" + result + "```")

bot.run('NTIyNDU4Mzk2NjI5MjcwNTMx.DvLRJA.L1O1cqEIylU8WqVSA2EEDyl3htw')

