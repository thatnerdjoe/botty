# Import python stdlib modules
import datetime
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
                raise EnvironmentError(
                    f'Missing bot token, please set the \'{ENV_TOKEN}\' environment variable.')

            return config
        except Exception as e:
            raise Exception(
                f'ERROR: could not open find config file {config_file}')

    # Sample constant, returns a silly value for testing
    @classmethod
    def SAMPLE(self):
        return 0xCABB005E


config = Const.CONFIG()


def get_prefix(bot, message):
    """
    Dynamically returns the bot's prefix from its config,
    allowing the bot's prefix to be updated while it is running.

    :param bot: The instance of the Discord Client.
    :param message: The message pertaining to the context.
    :return: The prefix that the bot is meant to use.
    """
    if 'prefix' in bot.config:
        return bot.config['prefix']
    else:
        return '!'


# Instantiate the bot to use commands prefix from the config file
bot = commands.Bot(
    command_prefix=get_prefix, case_insensitive=True)

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
    print(
        f'Logged in as {bot.user} and connected to Discord! (ID: {bot.user.id})')

    # Set the playing status of the bot to show users how to use the help command.
    await bot.change_presence(activity=discord.Game(name=f'{bot.config["prefix"]}help'))

    # An alternative version of the playing status to show that the bot is "Watching" instead.
    """
    activity = discord.Activity(name=f'{len(bot.guilds)} servers.', type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)
    """

class Internal(commands.Cog, name="Internal"):
    """
    Commands used in the core infrastructure of the bot.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="restart", help="Restarts the bot.")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def restart(self, ctx):
        """
        TODO:
          Ask the user for confirmation that they want to restart the bot, as it could result in an error occurring
          with any changed code.
          If cancelled, do nothing, if confirmed, send a message in a logging channel to warn of the restart.
          Add a reaction to the user's original message confirming the restart (likely a check mark)
          Gracefully disconnect all active cogs and log out from Discord, end the MongoDB connection if still active.
          Using some external management script, wait a few seconds then re-run the bot.py file.

        :param ctx: The context of the command execution.
        """

        raise discord.ext.commands.CommandInvokeError('Restart command not implemented.')

    @commands.command(name="prefix", help="Changes the command prefix of the bot.", brief="?")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, prefix: str):
        """
        Updates the active command prefix that the bot uses for communication,
        and saves that to the config file.

        TODO:
          Add some form of logging channel that the updated prefix gets shown in.
          Add input validation to confirm that the prefix matches some set of requirements for a valid prefix.

        :param ctx: The context of the command execution.
        :param prefix: The prefix to update the bot to.
        """

        # Check if the prefix matches the already in use one.
        if self.bot.config['prefix'] == prefix:
            embed = discord.Embed(
                title="Prefix Already in Use",
                description=f"The prefix {prefix} is already being used by the bot."
            )
            embed.set_footer(
                text=self.bot.config['footer']['text'],
                icon_url=self.bot.config['footer']['icon_url']
            )
            return await ctx.send(embed=embed)

        # PREFIX VALIDATION PLACEHOLDER

        # Overwrite the config directly from the file, so that we don't accidentally save the bot's token in the
        # config file.
        with open('./config.json', 'r') as file:
            conf = json.load(file)

        embed = discord.Embed(
            title=f"Updated {self.bot.user.name} Prefix"
        )
        embed.add_field(
            name="Old Prefix",
            value=bot.config['prefix'],
            inline=True
        )
        embed.add_field(
            name="New Prefix",
            value=prefix,
            inline=True
        )
        embed.set_footer(
            text=self.bot.config['footer']['text'],
            icon_url=self.bot.config['footer']['icon_url']
        )

        bot.config['prefix'] = prefix
        conf['prefix'] = prefix
        with open('./config.json', 'w') as file:
            file.write(json.dumps(conf, indent=2))

        await self.bot.change_presence(activity=discord.Game(name=f'{bot.config["prefix"]}help'))

        await ctx.send(embed=embed)

    @commands.group(name="cog",
                    aliases=["cogs"],
                    help="A group of commands for loading, unloading, and reloading cogs.",
                    invoke_without_command=True)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def cog(self, ctx):
        """
        The parent command for all commands related to managing cog extensions.

        :param ctx: The context of the command execution.
        """
        await ctx.send_help(self.cog)

    @cog.command(name="load",
                 help="Load a cog extension file by name.\n`help` refers to the `./cogs/help.py` file.",
                 brief="help")
    async def load(self, ctx, cog_name: str):
        """
        Loads a cog into the system by name.
        NOTE: USE '.' AS A FOLDER PATH SEPARATOR:
        "sample.help" refers to "./cogs/sample/help.py"

        :param ctx: The context of the command execution.
        :param cog_name: The name of the cog to be loaded.
        """

        try:
            # Try to load the extension
            self.bot.load_extension('cogs.' + cog_name)

            embed = discord.Embed(
                title=f"{cog_name} Cog Loaded",
                description="The cog has been loaded successfully.",
                timestamp=datetime.datetime.now(datetime.timezone.utc)
            )
            embed.set_author(
                name=ctx.author.name,
                icon_url=ctx.author.avatar_url
            )
            embed.set_footer(
                text=self.bot.config['footer']['text'],
                icon_url=self.bot.config['footer']['icon_url']
            )
            await ctx.send(embed=embed)
        except commands.ExtensionAlreadyLoaded as e:
            # If the extension is already loaded, handle the error as such.
            embed = discord.Embed(
                title=f"{cog_name} Cog Already Loaded",
                description="The cog you attempted to load was already loaded into the system.",
                timestamp=datetime.datetime.now(datetime.timezone.utc)
            )
            embed.set_author(
                name=ctx.author.name,
                icon_url=ctx.author.avatar_url
            )
            embed.set_footer(
                text=self.bot.config['footer']['text'],
                icon_url=self.bot.config['footer']['icon_url']
            )
            await ctx.send(embed=embed)
        except Exception as e:
            # Handle any other error that may occur (includes SyntaxError when loading an extension, etc.)
            embed = discord.Embed(
                title=f"Failed to Load {cog_name}",
                description=str(e),
                timestamp=datetime.datetime.now(datetime.timezone.utc)
            )
            embed.set_author(
                name=ctx.author.name,
                icon_url=ctx.author.avatar_url
            )
            embed.set_footer(
                text=self.bot.config['footer']['text'],
                icon_url=self.bot.config['footer']['icon_url']
            )
            await ctx.send(embed=embed)

    @cog.command(name="unload",
                 help="Unload a cog by name.\n`help` refers to the `./cogs/help.py` file.",
                 brief="help")
    async def unload(self, ctx, cog_name: str):
        """
        Unloads a registered extension by the name given.
        NOTE: USE '.' AS A FOLDER PATH SEPARATOR:
        "sample.help" refers to "./cogs/sample/help.py"

        :param ctx: The context of the command execution.
        :param cog_name: The name of the cog to be loaded.
        """
        try:
            # Try to remove the extension as provided in the command execution
            self.bot.unload_extension('cogs.' + cog_name)

            embed = discord.Embed(
                title=f"{cog_name} Cog Unloaded",
                description="The cog has been unloaded successfully.",
                timestamp=datetime.datetime.now(datetime.timezone.utc)
            )
            embed.set_author(
                name=ctx.author.name,
                icon_url=ctx.author.avatar_url
            )
            embed.set_footer(
                text=self.bot.config['footer']['text'],
                icon_url=self.bot.config['footer']['icon_url']
            )
            await ctx.send(embed=embed)
        except commands.ExtensionNotLoaded as e:
            # If the extension is not found, handle the error as such.
            embed = discord.Embed(
                title=f"{cog_name} Cog Not Found",
                description="The cog you attempted to load was not found in the system.",
                timestamp=datetime.datetime.now(datetime.timezone.utc)
            )
            embed.set_author(
                name=ctx.author.name,
                icon_url=ctx.author.avatar_url
            )
            embed.set_footer(
                text=self.bot.config['footer']['text'],
                icon_url=self.bot.config['footer']['icon_url']
            )
            await ctx.send(embed=embed)
        except Exception as e:
            # Handle any other error that may occur
            embed = discord.Embed(
                title=f"Failed to Unload {cog_name}",
                description=str(e),
                timestamp=datetime.datetime.now(datetime.timezone.utc)
            )
            embed.set_author(
                name=ctx.author.name,
                icon_url=ctx.author.avatar_url
            )
            embed.set_footer(
                text=self.bot.config['footer']['text'],
                icon_url=self.bot.config['footer']['icon_url']
            )
            await ctx.send(embed=embed)

    @cog.command(name="reload",
                 help="Reload a cog by name.\n`cogs.help` refers to the `./cogs/help.py` file.",
                 brief="help")
    async def reload(self, ctx, cog_name: str):
        """
        Reloads an extension by the given name.
        NOTE: USE '.' AS A FOLDER PATH SEPARATOR:
        "sample.help" refers to "./cogs/sample/help.py"

        :param ctx: The context of the command execution.
        :param cog_name: The name of the cog to be loaded.
        """
        try:
            # Try to reload the extension as provided in the command execution
            self.bot.reload_extension('cogs.' + cog_name)

            embed = discord.Embed(
                title=f"{cog_name} Cog Reloaded",
                description="The cog has been reloaded successfully.",
                timestamp=datetime.datetime.now(datetime.timezone.utc)
            )
            embed.set_author(
                name=ctx.author.name,
                icon_url=ctx.author.avatar_url
            )
            embed.set_footer(
                text=self.bot.config['footer']['text'],
                icon_url=self.bot.config['footer']['icon_url']
            )
            await ctx.send(embed=embed)
        except Exception as e:
            # Handle any other error that may occur
            embed = discord.Embed(
                title=f"Failed to Reload {cog_name}",
                description=str(e),
                timestamp=datetime.datetime.now(datetime.timezone.utc)
            )
            embed.set_author(
                name=ctx.author.name,
                icon_url=ctx.author.avatar_url
            )
            embed.set_footer(
                text=self.bot.config['footer']['text'],
                icon_url=self.bot.config['footer']['icon_url']
            )
            await ctx.send(embed=embed)


# Register the internal commands cog/
bot.add_cog(Internal(bot))

# Run the bot with the API token pulled from the environment variable
try:
    bot.run(bot.config['token'], bot = True, reconnect = True)
except discord.LoginFailure:
    print(f"Invalid {ENV_TOKEN} variable: {bot.config['token']}")
    input("Press enter to continue...")
