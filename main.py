import discord
import logging
from discord.ext import commands
import yaml
from tenmans import Scrim

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='bot_logs.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix='?')

with open('config.yml', 'r') as stream:
    config = yaml.safe_load(stream)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def shutdown(ctx):
    await ctx.send("Shutting down...")
    await bot.logout()

bot.add_cog(Scrim(bot))
bot.run(config['configurations']['token'])
