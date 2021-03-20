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
    async def test(self, ctx):
        '''
        hello:  A test function for ensuring that extensions and permissions 
        are implemented properly.
        '''
        await ctx.send("Hello!")

    @commands.guild_only()
    @commands.command()
    async def addrole(self, ctx, role=None):
        '''
        addrole: Used to add guild roles to a user 
        '''
        # Prompt user to specify a role if none provided
        if role == None:
            await ctx.send(f'Please specify a role')
            return

        # Check if the specified roll exists
        for eachRole in ctx.guild.roles:
            if role == eachRole.name:
                role = eachRole
                break

        if type(role) != str:
            try:
                await ctx.author.add_roles(role)
                await ctx.send(f'{ctx.author}, successfully added role {role.name}')
            except Exception as e:
                if type(e).__name__ == "Forbidden":
                    await ctx.send('Sorry, I do not have sufficient privileges')
                else:
                    await ctx.send(e)
            return
        else:
            await ctx.send(f'Could not find role "{role}"')
            return


def setup(bot):
    '''
    setup:  Required by Discord.py for extensible, multi-file projects
            typically used with Cogs.
    '''
    bot.add_cog(Botty(bot))
