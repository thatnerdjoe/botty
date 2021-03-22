import discord
from discord.ext import commands

"""
*******************************************************************************
This is a Cog. These structures are used by Discord.py to create classes
with their own commands, event listeners, and attributes.

Botty Mc Botface's core functions: More to come!

Authors: Joe Miller (@thatnerdjoe)
Version: 0.1
Date: 03-20-2021
*******************************************************************************
"""


class Botty(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Loaded Botty Cog.")

    def cog_unload(self):
        print("Unloaded Botty Cog.")

    @commands.command()
    async def test(self, ctx):
        """
        A test function for ensuring that extensions and permissions are implemented properly.
        """
        await ctx.send("Hello!")

    @commands.guild_only()
    @commands.command(brief="rolename")
    async def addrole(self, ctx, role: discord.Role):
        """
        Used to add guild roles to a user
        """
        if type(role) != str:
            try:
                await ctx.author.add_roles(role)
                await ctx.send(f'{ctx.author}, successfully added role {role.name}')
            except discord.Forbidden:
                await ctx.send('Sorry, I do not have sufficient privileges')
            except Exception as e:
                await ctx.send(e)
            return

    @commands.guild_only()
    @commands.command()
    async def removerole(self, ctx, *, role=None):
        """
        Used to remove guild roles from a user 
        """
        if type(role) != str:
            # Try to remove the specified role from the user
            try:
                await ctx.author.remove_roles(role)
                await ctx.send(f'{ctx.author.mention}, successfully removed role {role.name}.')

            # Send message to Discord if an exception is raised
            except discord.Forbidden:
                await ctx.send('Sorry, I do not have sufficient privileges.')
            except Exception as e:
                await ctx.send(e)


def setup(bot):
    """
    Required by Discord.py for extensible, multi-file projects typically used with Cogs.
    """
    bot.add_cog(Botty(bot))
