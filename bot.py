# Import python modules
import discord
import logging
import json
from time import time
from discord.ext import commands


'''
*******************************************************************************

Overview: This is the bot's core infrastructure; it will create the basic 
instance of the Discord bot which loads extensions to implement cogs. 
Extensions are hot-swappable portions of code conducive to development.
Cogs are the classes that contain the added commands, event listeners, and 
attributes of these extensions.

Authors: Joe Miller (@thatnerdjoe)
Version: 0.1
Date: 03-20-2021
*******************************************************************************
'''


def constant(fn):
    '''
    Decorator function to create pseudo constants in Python, see class `_Const`
    '''

    # Raise a TypeError if there is an attempt to modify a constant
    def fset(*args, **kwargs):
        raise TypeError

    # Retrieve the value of the constant
    def fget(*args, **kwargs):
        return fn()

    # Return the value to the caller
    return property(fget, fset)


class _Const(object):
    '''
    This class is merely a construct to enforce constant values.
    Each value is represented by a function holding only a return value.
    To get the value, call it with (assuming CONST is an object of _Const):
    >>> CONST.SAMPLE
    '''
    # Returns file descriptor of the opened config.json
    @constant
    def CONFIG():
        config_file = './config.json'
        try:
            with open(config_file, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f'ERROR: could not open find config file {config_file}')
            exit()

    # Sample constant, returns a silly value for testing
    @ constant
    def SAMPLE():
        return 0xCABB005E


# Instantiate CONSTANTS object
CONST = _Const()

# Instantiate the bot to use commands prefix from the config file
bot = commands.Bot(
    command_prefix=CONST.CONFIG['prefix'], case_insensitive=True)

# Remove 'help' command for a custom one
bot.remove_command('help')

# Load the bot's extensions here
bot.load_extension("cogs.botty")


@bot.event
async def on_ready():
    '''
    on_ready:   Wait for connection to Discord. Set up of the bot's functions.
    '''
    # Print connection status
    print(f'Logged on as {bot.user}')


# Import the API token
bot.run(CONST.CONFIG['token'])
