import discord
from discord.ext import commands, menus


class HelpSource(menus.ListPageSource):
    """
    This class is used to manage pagination of the help command.
    """
    def __init__(self, ctx, fields, per_page=3):
        self.ctx = ctx
        self.num_fields = int(len(fields) / per_page)
        if len(fields) % per_page:
            self.num_fields += 1
        super().__init__(fields, per_page=per_page)

    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page

        embed = discord.Embed(
            title=f"\N{NEWSPAPER} Help Menu [{menu.current_page + 1}/{self.num_fields}]",
            description=f"A listing of all available commands sorted by grouping.\n"
                        f"To learn more about specific commands, use `{self.ctx.bot.config['prefix']}help <command>`"
        )
        for field in [field for i, field in enumerate(entries, start=offset)]:
            embed.add_field(
                name=field['name'],
                value=field['value'],
                inline=field['inline']
            )
        embed.set_footer(
            text=self.ctx.bot.config['footer']['text'],
            icon_url=self.ctx.bot.config['footer']['icon_url']
        )
        return embed


class HelpCommand(commands.MinimalHelpCommand):
    """
    Contains all of the features for a custom help message depending on certain
    values set when defining a command in the first place.

    NOTE: Users who use the help command can only see commands that they are actually allowed to use in permissions.
    Similarly, any commands that have `hidden=True` in their decorator are hidden.
    """
    async def send_bot_help(self, mapping):
        """
        Send a help list for all of the bot commands.
        """
        fields = []
        # Parsing through all cogs and all commands contained within each command.
        for cog in mapping.keys():
            if cog:
                command_list = await self.filter_commands(mapping[cog], sort=True)
                if len(command_list) > 0:
                    # If a cog contains visible commands, add the to an embed field.
                    fields.append({
                        "name": cog.qualified_name,
                        "value": f"{cog.description}\nCommands:\n" +
                                 ", ".join(f"`{command}`" for command in command_list),
                        "inline": False
                    })

        # Create the paginated help menu
        pages = menus.MenuPages(source=HelpSource(self.context, fields), delete_message_after=True)
        await pages.start(self.context)

    async def send_cog_help(self, cog):
        """
        Sends help for all commands contained within a cog, by cog name.
        """
        embed = discord.Embed(
            title=f"{cog.qualified_name} Help",
            description=f"{cog.description}\nTo learn more about specific commands, "
                        f"use `{self.clean_prefix}help <command>`"
        )
        embed.set_author(
            name=self.context.message.author,
            icon_url=self.context.message.author.avatar_url
        )
        embed.add_field(
            name="Commands",
            value="\n".join(
                "`{1.qualified_name}`".format(self, command)
                for command in cog.walk_commands()
                if not command.hidden
            )
        )
        embed.set_footer(
            text=self.context.bot.config['footer']['text'],
            icon_url=self.context.bot.config['footer']['icon_url']
        )
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        """
        Sends help message for all commands grouped in a parent command.
        """
        command_list = group.walk_commands()
        command_activation = []
        command_example = []
        for command in command_list:
            if f'`{command.qualified_name} {command.signature}` - {command.help}' not in command_activation:
                if not command.hidden:
                    command_activation.append(f'`{command.qualified_name} {command.signature}` - {command.help}')
                    if command.brief not in [None, ""]:
                        command_example.append(f'`{self.clean_prefix}{command.qualified_name} {command.brief}`')
                    else:
                        command_example.append(f'`{self.clean_prefix}{command.qualified_name}`')

        fields = []
        if group.aliases:
            fields.append({
                "name": "Aliases",
                "value": ", ".join('`{}`'.format(alias) for alias in group.aliases),
                "inline": False
            })
        fields.append({
            "name": "Commands",
            "value": "\n".join(command_activation),
            "inline": False
        })
        fields.append({
            "name": "Examples",
            "value": "\n".join(command_example),
            "inline": False
        })

        embed = discord.Embed(
            title=f"'{group.qualified_name.capitalize()}' Help",
            description=f"{group.help}\n\n"
                        f"For more information on each command, use `{self.clean_prefix}help [command]`."
        )
        for field in fields:
            embed.add_field(
                name=field['name'],
                value=field['value'],
                inline=field['inline']
            )
        embed.set_author(
            name=self.context.message.author,
            icon_url=self.context.message.author.avatar_url
        )
        embed.set_footer(
            text=self.context.bot.config['footer']['text'],
            icon_url=self.context.bot.config['footer']['icon_url']
        )
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        """
        Send help for a specific given single command.
        """
        fields = []
        if command.aliases:
            fields.append({
                "name": "Aliases",
                "value": ", ".join('`{}`'.format(alias) for alias in command.aliases),
                "inline": False
            })
        fields.append({
            "name": "Usage",
            "value": f"`{self.clean_prefix}{command.qualified_name}"
                     f"{' ' + command.signature if command.signature else ''}`",
            "inline": False
        })
        fields.append({
            "name": "Example",
            "value": f"`{self.clean_prefix}{command.qualified_name}"
                     f"{' ' + command.brief if command.brief else ''}`",
            "inline": False
        })

        embed = discord.Embed(
            title=f"'{command.name.capitalize()}' Help",
            description=f"{command.help}"
        )
        for field in fields:
            embed.add_field(
                name=field['name'],
                value=field['value'],
                inline=field['inline']
            )
        embed.set_author(
            name=self.context.message.author,
            icon_url=self.context.message.author.avatar_url
        )
        embed.set_footer(
            text=self.context.bot.config['footer']['text'],
            icon_url=self.context.bot.config['footer']['icon_url']
        )
        await self.get_destination().send(embed=embed)


class LoadHelp(commands.Cog, name="Help"):
    """
    The actual discord cog that is loaded when this file is added, simply wrapping the help command.
    """
    def __init__(self, bot):
        self._original_help_command = bot.help_command
        self.bot = bot
        bot.help_command = HelpCommand()
        bot.help_command.cog = self
        print(f"Loaded Help Cog.")

    """
    Called when the cog is unloaded from the system.
    """
    def cog_unload(self):
        print(f"Unloaded Help Cog.")


def setup(bot):
    """
    The function called by Discord.py when adding a file extension in a multi-file project.
    """
    bot.add_cog(LoadHelp(bot))
