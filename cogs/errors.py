import discord
from discord.ext import commands

"""
*******************************************************************************
This is a custom error handler cog that is meant to handle any of the
built-in Discord.py errors that may occur during the bot's execution.

NOTE: You should remove this Cog using the `cog unload` command when bug testing, as the
        error listeners will prevent a full stack trace from being printed and will instead
        defer to the listeners to handle the error. This is useful in a production state, but can lead to
        a developer not receiving enough information on an error when bug testing.

Authors: Houghton Mayfield (@Heroicos_HM)
Version: 0.1
Date: 03-25-2021
*******************************************************************************
"""


class Errors(commands.Cog, name="Error Handler"):
    def __init__(self, bot):
        self.bot = bot
        print(f"{self.bot.utils.OK} {self.bot.utils.time_log()} Loaded Error Cog.")

    def cog_unload(self):
        print(f"{self.bot.utils.OK} {self.bot.utils.time_log()} Unloaded Error Cog.")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """
        This listener will catch any errors that occur during a command's execution
        and pass them to this function instead of causing issues in the command itself.

        NOTE: This will not protect against basic logic errors like dividing by zero or other such issues.

        TODO:
          Print the errors that occur here to some form of log channel in Discord.

        :param ctx: The context surrounding the command that is raiding the error.
        :param error:  The error being raised.
        """

        if isinstance(error, commands.CommandNotFound):
            # This occurs if a user tries to use a command that does not exist.

            if ctx.message.content.startswith(f"{self.bot.config['prefix'] * 2}"):
                # Protects against a message not being meant to be used as a command but starts with two of the prefixes
                return

            # Print error information to the console
            self.print_log(log_type=self.bot.utils.WARN, message="Command Not Found", ctx=ctx)

            # Send error message to the user
            embed = self.bot.utils.get_embed(
                title="\N{CROSS MARK} Command Not Found",
                author=ctx.author
            )
            await ctx.send(embed=embed)

        elif isinstance(error, commands.BadArgument) and "not found" in str(error):
            # Print error information to the console
            self.print_log(
                log_type=self.bot.utils.ERR,
                message=f"{str(error).split(' ')[0]} Not Found",
                ctx=ctx,
                err=error
            )

            # Send error message to the user
            embed = self.bot.utils.get_embed(
                title=f"\N{CROSS MARK} {str(error).split(' ')[0]} Not Found",
                author=ctx.author,
                fields=[{
                    "name": "Received",
                    "value": "`" + str(error).split('\"')[1] + "`",
                    "inline": False
                }]
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CheckFailure):
            # Print error information to the console
            self.print_log(
                log_type=self.bot.utils.WARN,
                message="User attempted to use command without permission",
                ctx=ctx
            )

            # Send error message to the user
            embed = self.bot.utils.get_embed(
                title="\N{CROSS MARK} Permission Denied",
                desc=f"I'm sorry {ctx.author.name}, I'm afraid I can't do that.",
                author=ctx.author
            )
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingRequiredArgument):
            error = str(error).split(' ')
            error[0] = f"`{error[0]}`"
            error = ' '.join(error)

            # Print error information to the console
            self.print_log(
                log_type=self.bot.utils.ERR,
                message="Missing required parameter",
                err=error,
                ctx=ctx
            )

            # Send error message to the user
            embed = self.bot.utils.get_embed(
                title="Missing Required Parameter",
                desc=error.split(' ')[0],
                author=ctx.author
            )
            await ctx.send(embed=embed)

        else:
            # Handle any non-specific errors.
            # Print error information to the console
            self.print_log(
                log_type=self.bot.utils.ERR,
                message=error
            )

            # Send error message to the user
            embed = self.bot.utils.get_embed(
                title="Command Failed",
                desc=str(error),
                author=ctx.author
            )
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_error(self, error):
        """
        The global error handler that catches most exceptions that can occur during bot execution.
        This should ideally prevent the suspension of the bot runtime should an error occur,
        but again, there are some errors that this will not handle.

        TODO:
          Print the errors that occur here to come form of log channel in Discord.

        :param error: The exception that needs to be handled.
        """
        self.print_log(log_type=self.bot.utils.ERR, message=error)

    def print_log(self, log_type, message, err=None, ctx=None):
        """
        A helper function used to log information about a command error or a general bot error
        to the console.

        :param log_type: The type of error occurring. Should be one of either self.OK, WARN, or ERROR.
        :param message: The message to be logged as the error description.
        :param err: An optional instance of an error that occurred.
        :param ctx: An optional context for a command that caused an error when invoked.
        """

        print(f"{log_type} {self.bot.utils.time_log()} {message}:")
        spacing = ' '*35
        if err:
            print(f"{spacing} Error: {err}")
        if ctx:
            failed_com = ctx.message.content.split(' ')
            if len(failed_com) > 1:
                print(f"{spacing} Command: {failed_com[0]} | Args: {' '.join(failed_com[1:])}")
            else:
                print(f"{spacing} Command: {failed_com[0]}")
            print(f"{spacing} Author: {ctx.author} | ID: {ctx.author.id}")
            print(f"{spacing} Channel: {ctx.channel} | ID: {ctx.channel.id}")


def setup(bot):
    """
    The function called automatically by discord.py when loading an extension file.

    :param bot: The instance of the discord.ext.commands.Bot that is being run.
    """
    bot.add_cog(Errors(bot))