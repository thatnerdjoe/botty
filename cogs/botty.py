import discord
from discord.ext import commands

"""
*******************************************************************************
This is a Cog. These structures are used by Discord.py to create classes
with their own commands, event listeners, and attributes.

Botty Mc Botface's core functions: More to come!

Authors: Joe Miller (@thatnerdjoe)
Version: 0.
Date: 03-20-2021
*******************************************************************************
"""


class Botty(commands.Cog, name="Botty McBotface"):
    """
    The commands used to self-administer roles and similar actions.
    """

    def __init__(self, bot):
        self.bot = bot
        print("Loaded Botty Cog.")

    def cog_unload(self):
        print("Unloaded Botty Cog.")

    @commands.command()
    async def ping(self, ctx):
        """
        A test function for ensuring that extensions and permissions are implemented properly.
        """
        await ctx.send("pong!")

    @commands.command(name="addrole",
                      help="Adds a server role to self. Case insensitive.",
                      brief="CYBV 301")
    @commands.guild_only()
    async def addrole(self, ctx, *, role=None):
        """
        Used to add guild roles to a user 

        NOTE: These checks are required; `except` does not handle invalid roles.
        """

        if role == None:
            await ctx.send(f'Please specify a role.')

        else:
            for each_role in ctx.guild.roles:
                # case-insensitive roles
                if role.lower() == each_role.name.lower():
                    role = each_role
                    break

            if type(role) == discord.Role:
                try:
                    await ctx.author.add_roles(role)
                    await ctx.send(f'{ctx.author.mention}, successfully added role {role.name}.')

                except discord.Forbidden:
                    await ctx.send('Sorry, I do not have sufficient privileges.')

                except Exception as e:
                    await ctx.send(e)
            else:
                await ctx.send(f'Could not find server role "{role}".')
            """
            TODO:   Implement role suggestions for classes.
                    EXAMPLE - 'You entered "CYBV 352". Did you mean "CSCV 352"?'
            """

    @commands.command(name="removerole",
                      help="Removes a server role from self. Case insensitive.",
                      brief="CYBV 301")
    @commands.guild_only()
    async def removerole(self, ctx, *, role=None):
        """
        Used to remove guild roles from a user 

        NOTE: These checks are required; `except` does not handle invalid roles.
        """
        if role == None:
            await ctx.send(f'Please specify a role.')
            return

        else:
            for each_role in ctx.author.roles:
                # case-insensitive roles
                if role.lower() == each_role.name.lower():
                    role = each_role
                    break

            if type(role) == discord.Role:
                try:
                    await ctx.author.remove_roles(role)
                    await ctx.send(f'{ctx.author.mention}, successfully removed role {role.name}.')

                except discord.Forbidden:
                    await ctx.send('Sorry, I do not have sufficient privileges.')

                except Exception as e:
                    await ctx.send(e)
            else:
                await ctx.send(f'Could not find user role "{role}".')


def setup(bot):
    """
    Required by Discord.py for extensible, multi-file projects typically used with Cogs.
    """
    bot.add_cog(Botty(bot))
