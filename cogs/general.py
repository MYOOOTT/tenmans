import discord
from discord.ext import commands

class General:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def shutdown(ctx):
        await ctx.send("Shutting down...")
        await bot.logout()

def setup(bot):
    bot.add_cog(General(bot))
