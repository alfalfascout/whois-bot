import asyncio
import discord
from cogs import checks
from datetime import datetime
from discord.ext import commands

class General:
    """ Basic bot commands. """
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def uptime(self):
        """ How long the bot has been online, more or less. """
        now = datetime.today()
        uptime_dt = now - self.bot.upsince
        uptime_string = "I've been up for "
        if uptime_dt.days > 13:
            uptime_string += str(uptime_dt.days / 7) + " weeks."
        elif uptime_dt.days > 1:
            uptime_string += str(uptime_dt.days) + " days."
        elif uptime_dt.seconds > 7200:
            uptime_string += str(int(uptime_dt.seconds / 3600)) + " hours."
        elif uptime_dt.seconds >= 120:
            uptime_string += str(int(uptime_dt.seconds / 60)) + " minutes."
        elif uptime_dt.seconds < 120:
            uptime_string += "a minute or so."
        await self.bot.say(uptime_string)


def setup(bot):
    bot.add_cog(General(bot))
