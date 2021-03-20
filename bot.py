import discord
import logging
from time import time


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
    This class is merely a construct to hold constant values.
    Each value is represented by a function holding only a return value.
    To get the value, call it with (assuming CONST is an object of _Const): 
    >>> CONST.SAMPLE 
    '''
    # Holds location of the bot's config file
    @constant
    def CONFIG():
        return './config'

    # Sample constant, returns a silly value for testing
    @constant
    def SAMPLE():
        return 0xCABB005E


client = discord.Client()
