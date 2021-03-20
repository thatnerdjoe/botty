import discord
from discord.ext import commands

'''
*******************************************************************************
This is a Cog. These structures are used by Discord.py to create classes
with their own commands, event listeners, and attributes.

Botty Mc Botface's core functions: More to come!


Authors: Joe Miller (@thatnerdjoe)
Version: 0.1
Date: 03-20-2021
*******************************************************************************
'''


class Botty(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        '''
        hello:  A test function for ensuring that extensions and permissions 
        are implemented properly.
        '''
        await ctx.send("Hello!")


def setup(bot):
    '''
    setup:  Required by Discord.py for extensible, multi-file projects
            typically used with Cogs.
    '''
    bot.add_cog(Botty(bot))
