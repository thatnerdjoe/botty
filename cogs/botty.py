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
        print(f"{self.bot.utils.OK} {self.bot.utils.time_log()} Loaded Botty Cog.")

    def cog_unload(self):
        print(f"{self.bot.utils.OK} {self.bot.utils.time_log()} Unloaded Botty Cog.")

    @commands.command()
    async def test(self, ctx):
        """
        A test function for ensuring that extensions and permissions are implemented properly.
        """
        await ctx.send("Hello!")
        await ctx.confirm()

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
        else:
            await ctx.send(f'Could not find role "{role}"')
            return


def setup(bot):
    """
    Required by Discord.py for extensible, multi-file projects typically used with Cogs.
    """
    bot.add_cog(Botty(bot))
