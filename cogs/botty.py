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
            await ctx.send(f'Please specify a role.')

        # Check provided role
        else:
            # Check if the specified roll exists in the guild
            for eachRole in ctx.guild.roles:
                if role == eachRole.name:
                    role = eachRole
                    break

            # Check if `role` has been set to an object
            if type(role) != str:
                # Try to add the specified role to a user
                try:
                    await ctx.author.add_roles(role)
                    await ctx.send(f'{ctx.author.mention}, successfully added role {role.name}.')
                # Send message to Discord if an exception is raised
                except Exception as e:
                    # Insufficient privileges message
                    if type(e).__name__ == "Forbidden":
                        await ctx.send('Sorry, I do not have sufficient privileges to add roles.')
                    # HTTP Error message
                    else:
                        await ctx.send(e)
            # If role does not exist, prompt user in Discord.
            else:
                await ctx.send(f'Could not find role "{role}".')

    @commands.guild_only()
    @commands.command()
    async def removerole(self, ctx, role=None):
        '''
        removerole: Used to remove guild roles from a user 
        '''
        # Prompt user to specify a role if none provided
        if role == None:
            await ctx.send(f'Please specify a role.')
            return

        # Check provided role
        else:
            # Check if the specified roll exists for the member
            for eachRole in ctx.author.roles:
                if role == eachRole.name:
                    role = eachRole
                    break

            # Check if `role` has been set to an object
            if type(role) != str:
                # Try to remove the specified role from the user
                try:
                    await ctx.author.remove_roles(role)
                    await ctx.send(f'{ctx.author.mention}, successfully removed role {role.name}.')
                # Send message to Discord if an exception is raised
                except Exception as e:
                    # Insufficient privileges message
                    if type(e).__name__ == "Forbidden":
                        await ctx.send('Sorry, I do not have sufficient privileges to remove roles.')
                    # HTTP Error message
                    else:
                        await ctx.send(e)
            # If role does not exist, prompt user in Discord.
            else:
                await ctx.send(f'Could not find role "{role}".')


def setup(bot):
    '''
    setup:  Required by Discord.py for extensible, multi-file projects
            typically used with Cogs.
    '''
    bot.add_cog(Botty(bot))
