""" Danny wrote most of this:
https://github.com/Rapptz/RoboDanny/blob/master/cogs/utils/checks.py """

from discord.ext import commands
import discord.utils
import json


auths = {}
with open('auth.json', 'r') as authfile:
    auths = json.load(authfile)

def is_owner_check(message):
    return message.author.id == auths["admin"]

def is_owner():
    return commands.check(lambda ctx: is_owner_check(ctx.message))
