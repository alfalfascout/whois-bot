#!/usr/bin/env python3

"""
A chat bot for Discord
Created by Alan Jacon "alfalfascout"
Using discord.py
"""

import json
import asyncio
import discord
from datetime import datetime
from discord.ext import commands
from cogs import checks


class Botso(commands.Bot):
    def __init__(self, **options):
        super().__init__(**options)
        with open('auth.json', 'r') as authfile:
            self.auths = json.load(authfile)
        self.activeserver = ""
        self.as_members = {}
        self.usies = {}
        self.upsince = datetime.today()

    async def read_usies(self):
        """ Read in the users/descriptions and puts them in the usies dict """
        with open('usies.txt', 'r') as usiestxt:
            oneline = usiestxt.readline()
            while oneline != "":
                if oneline != "\n":
                    usy = oneline.split(' ~=~ ', 1)
                    desc = usy[1].replace('%%%', '\n')
                    desc = desc.rstrip('\n')
                    self.usies.update({usy[0]: desc})
                oneline = usiestxt.readline()
        for server in self.servers:
            if server.id == self.auths["server"]:
                self.activeserver = server
        self.as_members = self.activeserver.members

    async def write_usies(self):
        """ Overwrite the users/descs file with the current usies dict """
        with open('usies.txt', 'w') as usiestxt:
            for usy, desc in self.usies.items():
                filedesc = desc.replace('\n', '%%%')
                usiestxt.write(usy + ' ~=~ ' + filedesc + '\n')

    @asyncio.coroutine
    def process_commands(self, message):
        """ A modification of the original Discord process_commands,
            to allow prefixless messages in pms """
        _internal_channel = message.channel
        _internal_author = message.author

        view = commands.view.StringView(message.content)
        if message.author == self.user:
            return

        prefix = self._get_prefix(message)
        invoked_prefix = prefix

        if not isinstance(prefix, (tuple, list)):
            if not view.skip_string(prefix):
                return
        else:
            invoked_prefix = discord.utils.find(view.skip_string, prefix)
            if invoked_prefix is None:
                if not message.channel.is_private:
                    return
                else:
                    invoked_prefix = ' '

        invoker = view.get_word()
        tmp = {
            'bot': self,
            'invoked_with': invoker,
            'message': message,
            'view': view,
            'prefix': invoked_prefix
        }
        ctx = commands.context.Context(**tmp)
        del tmp

        if invoker in self.commands:
            command = self.commands[invoker]
            self.dispatch('command', command, ctx)
            ctx.command = command
            yield from command.invoke(ctx)
            self.dispatch('command_completion', command, ctx)
        else:
            exc = commands.CommandNotFound('Command "{}" is not found'.format(invoker))
            self.dispatch('command_error', exc, ctx)


description = """I am a whois bot made by alfalfascout on GitHub to help you keep track of your users' descriptions and pronouns until Discord adds official profiles or something."""
bot = Botso(command_prefix=commands.when_mentioned_or("%"),
    formatter=BotsoFormatter(), description=description)


initial_extensions = [
    "cogs.general",
    "cogs.usies"
]


for extension in initial_extensions:
    try:
        bot.load_extension(extension)
    except Exception as e:
        print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))


@bot.command(hidden=True, name="reload")
@checks.is_owner()
async def reload_module(module : str):
    module = module.strip()
    reload_success = True
    try:
        bot.unload_extension(module)
    except Exception as e:
        print('Failed to unload extension {}\n{}: {}'.format(extension, type(e).__name__, e))
    try:
        bot.load_extension(module)
    except Exception as e:
        print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))
        reload_success = False
        await bot.say("Sorry, I couldn't reload it.")
    if reload_success:
        await bot.say("Reloaded the module.")
        print("Reloaded {}.".format(module))


@bot.command(hidden=True, name="load")
@checks.is_owner()
async def load_module(module : str):
    module = module.strip()
    load_success = True
    try:
        bot.load_extension(module)
    except Exception as e:
        print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))
        load_success = False
        await bot.say("Sorry, I couldn't load it.")
    if load_success:
        await bot.say("Loaded the module.")
        print("Loaded {}.".format(module))


@bot.command(hidden=True, name="unload")
@checks.is_owner()
async def unload_module(module : str):
    module = module.strip()
    unload_success = True
    try:
        bot.unload_extension(module)
    except Exception as e:
        print('Failed to unload extension {}\n{}: {}'.format(extension, type(e).__name__, e))
        unload_success = False
        await bot.say("Sorry, I couldn't unload it.")
    if unload_success:
        await bot.say("Unloaded the module.")
        print("Unloaded {}.".format(module))


@bot.command(hidden=True, name="crash")
@checks.is_owner()
async def crash_bot():
    await bot.say("Okay, I'll shut down.")
    await bot.close()
    loop.close()


@bot.event
async def on_ready():
    """ When the bot is up and running, print its username and id
        to the console, then populate the usies dict from usies.txt """
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    await bot.read_usies()
    print('------')


loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(bot.login(bot.auths["token"]))
    loop.run_until_complete(bot.connect())
except Exception as e:
    print("{}: {}".format(type(e).__name__, e))
    loop.run_until_complete(bot.close())
finally:
    loop.close()
