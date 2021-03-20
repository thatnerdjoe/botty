# Import python modules
import discord
import logging
import json
from time import time

# Import bascobot function modules


def performance(fn):
    '''
    Decorator function to measure the time performance of a function
    '''
    def wrapper(*args, **kwargs):
        # Get start time
        start_time = time()
        # Do the functions
        result = fn(*args, **kwargs)
        # Get end time
        end_time = time()
        # Calculate elapsed time
        total_time = (end_time-start_time)*1000
        # Print the result to stdout
        # EX: "function() took 112 ms to execute"
        print(f'{fn.__name__}() took {total_time:.2f} ms to execute')
        # Return the result from the original functions
        return result
    # Exit decorator
    return wrapper


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
    # Holds location of the bot's config file
    @constant
    def CONFIG():
        config_file = './config.json'
        try:
            data = json.load(open(config_file, 'r'))
            return data
        except Exception as e:
            print(f'ERROR: could not open find config file {config_file}')
            exit()

    # Sample constant, returns a silly value for testing
    @ constant
    def SAMPLE():
        return 0xCABB005E


# Instantiate client object
client = discord.Client()

# Instantiate CONSTANTS object
CONST = _Const()

# specify bot command prefixes using value in the config.json file
bot_command = bot.command(command_prefix=CONST.CONFIG['prefix']


@ client.event
async def on_ready():
    print('Logged on as {0.user}'.format(client))


@ client.event
async def on_message(msg):
    # Do nothing if message is from this box
    if msg.author == client.user:
        return

    # If a server message has the command prefix, do a task
    if message.content.startswith(bot_command):
        await message.channel.send()


# Import the API token
client.run(CONST.CONFIG['token'])
