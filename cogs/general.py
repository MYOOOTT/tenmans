import discord
from discord.ext import commands

class General:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def shutdown(self, ctx):
        await ctx.send("Shutting down...")
        await bot.logout()

    def is_myself(message):
        return message.author == self.bot
    
    @commands.command()
    async def purge(self, ctx, parsed_msg=100):
        deleted = ctx.channel.purge(limit=100, check = is_myself)
        message = await ctx.send('Deleted {} message(s)'.format(len(deleted)))
        await asyncio.sleep(4)
        await message.delete()

def setup(bot):
    bot.add_cog(General(bot))
