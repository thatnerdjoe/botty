# Import python stdlib modules
import os
import logging
import json
from time import time

# Import python modules
import discord
from discord.ext import commands, menus


"""
*******************************************************************************

Overview: This is the bot's core infrastructure; it will create the basic 
instance of the Discord bot which loads extensions to implement cogs. 
Extensions are hot-swappable portions of code conducive to development.
Cogs are the classes that contain the added commands, event listeners, and 
attributes of these extensions.

Authors: Joe Miller (@thatnerdjoe), Houghton Mayfield (@Heroicos_HM)
Version: 0.2
Date: 03-21-2021
*******************************************************************************
"""

ENV_TOKEN = 'BASCOBOTTOKEN'

class Const(object):
    """
    This class is merely a construct to enforce constant values.
    Each value is represented by a function holding only a return value.
    To get the value, call it with:
    >>> Const.SAMPLE()
    """
    # Returns file descriptor of the opened config.json
    @classmethod
    def CONFIG(self):
        config_file = './config.json'
        try:
            with open(config_file, 'r') as file:
                config = json.load(file)

            config['token'] = os.getenv(ENV_TOKEN)
            if config['token'] is None:
                raise EnvironmentError(f'Missing bot token, please set the \'{ENV_TOKEN}\' environment variable.')

            return config
        except Exception as e:
            raise Exception(f'ERROR: could not open find config file {config_file}')

    # Sample constant, returns a silly value for testing
    @classmethod
    def SAMPLE(self):
        return 0xCABB005E

config = Const.CONFIG()

# Instantiate the bot to use commands prefix from the config file
bot = commands.Bot(
    command_prefix=config['prefix'], case_insensitive=True)

# Save the loaded config to the bot instance, so that it
# can be accessed in other Cogs later.
bot.config = config

# Remove 'help' command for a custom one
bot.remove_command('help')

# Load the bot's extensions here
exts = [
    'cogs.botty',
    'cogs.help'
]
for ext in exts:
    bot.load_extension(ext)


@bot.event
async def on_ready():
    """
    Executes after the connection to Discord has been confirmed.

    NOTE:
        Please avoid putting any meaningful setup in here if possible. It should
        be noted that this method may be triggered multiple times, and should not be
        relied on as a setup tool unless necessary. It is primarily used in logging purposes.
    """
    # Print connection confirmation
    print(f'Logged in as {bot.user} and connected to Discord! (ID: {bot.user.id})')

    # Set the playing status of the bot to show users how to use the help command.
    await bot.change_presence(activity=discord.Game(name=f'{bot.config["prefix"]}help'))

    # An alternative version of the playing status to show that the bot it "Watching" instead.
    """
    activity = discord.Activity(name=f'{len(bot.guilds)} servers.', type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)
    """


# Import the API token
bot.run(bot.config['token'])
