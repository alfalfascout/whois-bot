import asyncio
import discord
from cogs import checks
from discord.ext import commands

class UserDescription:
    """ These commands are related to user descriptions. """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def iam(self, ctx, *profile : str):
        """ If you tell me who you are, I'll remember. Syntax: !iam some words about yourself. Include your pronouns! """
        if not profile:
            await self.bot.say("You are.")
        else:
            profile = ctx.message.content.split("!iam ")[1]
            usy = ctx.message.author.id
            self.bot.usies.update({usy: profile})
            await self.bot.write_usies()
            await self.bot.say("Thanks for letting me know.")


    @commands.command(hidden=True)
    @checks.is_owner()
    async def botis(self, *profile : str):
        if profile:
            profile = ctx.message.content.split("!botis ")[1]
            usy = self.bot.user.id
            self.bot.usies.update({usy: profile})
            await self.bot.write_usies()
            await self.bot.say("Thanks for the update.")


    @commands.command(pass_context=True)
    async def iamnot(self):
        """ I'll forget what you told me about you. """
        if ctx.message.author.id in usies:
            del self.bot.usies[ctx.message.author.id]
            await self.bot.say("I forget you.")
            await self.bot.write_usies()
        else:
            await self.bot.say("If I knew who you were, I would forget you.")


    @commands.command(pass_context=True)
    async def whois(self, ctx, usyname : str):
        """ I'll tell you who any person is, if I know them. Syntax: !whois name """

        result = "someone I don't know much about."
        if not usyname:
            """ If the user didn't give a name, don't bother """
            await self.bot.say("A lot of people are.")
        elif ctx.message.mentions:
            """ Get @mentioned users first """
            usy = ctx.message.mentions[0].display_name
            if ctx.message.mentions[0].id in self.bot.usies.keys():
                description = self.bot.usies[ctx.message.mentions[0].id]
            await self.bot.say(usy + " is " + description)
        else:
            """ If nobody was @mentioned, try to match the name to members """
            matches = []
            for as_member in self.bot.as_members:
                if usyname.encode('ascii', 'ignore').lower() in \
                as_member.display_name.encode('ascii', 'ignore').lower():
                    matches.append(as_member)
                elif usyname.encode('ascii', 'ignore').lower() in \
                as_member.name.encode('ascii', 'ignore').lower():
                    matches.append(as_member)
            """ Then return the matches' descriptions, if available """
            if len(matches) > 4:
                await self.bot.say("There are a lot of people \
                    with names like that.")
            elif len(matches) > 1:
                await self.bot.say("I found more than one.")
                for as_member in matches:
                    usy = as_member.display_name
                    if as_member.id in self.bot.usies.keys():
                        result = self.bot.usies[as_member.id]
                    else:
                        result = "someone I don't know much about."
                    await self.bot.say(usy + " is " + result)
            elif len(matches) > 0:
                as_member = matches[0]
                usy = as_member.display_name
                if as_member.id in self.bot.usies.keys():
                    result = self.bot.usies[as_member.id]
                else:
                    result = "someone I don't know much about."
                await self.bot.say(usy + " is " + result)
            else:
                await self.bot.say("I don't know anyone like that.")


def setup(bot):
    bot.add_cog(UserDescription(bot))
