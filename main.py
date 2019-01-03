import discord
import logging
from discord.ext import commands
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

bot.load_extension("cogs.tenmans")
bot.load_extension("cogs.general")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


bot.run(config['configurations']['token'])

 
