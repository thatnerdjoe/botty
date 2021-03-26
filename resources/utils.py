from colorama import Fore
import datetime
import discord
from discord.ext import menus
import re

"""
*******************************************************************************
A collection of utility variables/functions that can be used in many places
throughout the bot.

Classes:
    Utils:
        The main utility functions to be used in the bot.
    Confirmation:
        A class used for creating and running messages that ask a user for a yes/no input.
    TimeLength:
        A class containing attributes representing a length of time in days, hours, minutes, and seconds.

Authors: Houghton Mayfield (@Heroicos_HM)
Version: 0.1
Date: 03-25-2021
*******************************************************************************
"""


class Utils:
    # Constants to be used in logging to the console.
    OK = f"{Fore.GREEN}[OK]{Fore.RESET}  "
    WARN = f"{Fore.YELLOW}[WARN]{Fore.reset}"
    ERR = f"{Fore.RED}[ERR]{Fore.reset} "

    def __init__(self, config):
        self.embed_color = config['embed']['color']
        self.footer = config['embed']['footer']['text']
        self.footer_icon = config['embed']['footer']['icon_url']

    def get_embed(self, title=None, desc=None, fields=None,
                  ts=False, author=None, thumbnail=None, image=None,
                  footer=None, footer_icon=None, url=None, color=None):
        """
        Creates a discord.Embed object from all of the given parameters.
        To gain an understanding of each aspect of an embed, view this visualizer:


        :param title: An optional title for the embedded message.
        :param desc: An optional description field for an embedded message.
        :param fields: An optional list of dictionaries describing embed fields.
        :param ts: A boolean value stating whether to include a timestamp in the embed footer.
        :param author: An optional argument of a string for an author name,
            a dictionary describing author name and icon_url,
            or an instance of either a discord.User or discord.Member object.
        :param thumbnail: An optional argument containing a link to an image to use as the thumbnail for the embed.
        :param image: An optional argument containing a link to an image to use as a large image for the embed.
        :param footer: An optional argument containing a replacement footer text from the default set in the bot config.
            Alternatively, pass the "footer" parameter as False to exclude the footer entirely.
        :param footer_icon: An optional argument containing a replacement footer icon url from the default.
        :param url: An optional argument containing a url to link the title of the embed to.
        :param color: An optional argument containing either a decimal color value or an instance of discord.Color.
        :return: A discord.Embed object created with all of the parameters given.
        """

        # Creating the initial embed object
        embed = discord.Embed(
            title=title,
            description=desc,
            url=url,
            color=self.embed_color if not color else color
        )

        # Setting the footer
        if footer is not False:
            embed.set_footer(
                text=self.footer if not footer else footer,
                icon_url=self.footer_icon if not footer_icon else footer_icon
            )

        # Setting the timestamp
        if ts:
            embed.timestamp = datetime.datetime.now(datetime.timezone.utc)

        # Setting the author
        if author:
            if type(author) == str:
                embed.set_author(name=author)
            elif type(author) == dict:
                if 'icon_url' in author and author['icon_url']:
                    embed.set_author(
                        name=author['name'],
                        icon_url=author['icon_url']
                    )
                elif author['name']:
                    embed.set_author(name=author['name'])
            elif type(author) in [discord.User, discord.Member]:
                embed.set_author(
                    name=author.name,
                    icon_url=author.avatar_url
                )

        # Setting the fields
        if fields:
            for field in fields:
                embed.add_field(
                    name=field['name'],
                    value=field['value'],
                    inline=field['inline'] if 'inline' in field else True
                )

        # Setting the thumbnail
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)

        # Setting the image
        if image:
            embed.set_image(url=image)

        return embed

    def update_embed(self, embed: discord.Embed, title=None, desc=None, fields=None,
                     ts=False, author=None, thumbnail=None, image=None,
                     footer=None, footer_icon=None, url=None):
        """
        Modifies an existing discord.Embed object.

        :param embed: A pre-existing embed object
        :param title: An optional title for the embedded message.
        :param desc: An optional description field for an embedded message.
        :param fields: An optional list of dictionaries describing embed fields.
        :param ts: A boolean value stating whether to include a timestamp in the embed footer.
        :param author: An optional argument of a string for an author name,
            a dictionary describing author name and icon_url,
            or an instance of either a discord.User or discord.Member object.
        :param thumbnail: An optional argument containing a link to an image to use as the thumbnail for the embed.
        :param image: An optional argument containing a link to an image to use as a large image for the embed.
        :param footer: An optional argument containing a replacement footer text from the default set in the bot config.
            Alternatively, pass the "footer" parameter as False to exclude the footer entirely.
        :param footer_icon: An optional argument containing a replacement footer icon url from the default.
        :param url: An optional argument containing a url to link the title of the embed to.
        :return: A modified discord.Embed object created with all of the parameters given.
        """

        # Updating the title
        if title:
            embed.title = title

        # Updating the description
        if desc:
            embed.description = desc

        # Updating the url
        if url:
            embed.url = url

        # Updating the footer
        if footer is not False:
            embed.set_footer(
                text=self.footer if not footer else footer,
                icon_url=self.footer_icon if not footer_icon else footer_icon
            )

        # Updating the timestamp
        if ts is True:
            embed.timestamp = datetime.datetime.now(datetime.timezone.utc)

        # Updating the author
        if author:
            if type(author) == str:
                embed.set_author(name=author)
            elif type(author) == dict:
                if 'icon_url' in author and author['icon_url']:
                    embed.set_author(
                        name=author['name'],
                        icon_url=author['icon_url']
                    )
                elif author['name']:
                    embed.set_author(name=author['name'])
            elif type(author) in [discord.User, discord.Member]:
                embed.set_author(
                    name=author.name,
                    icon_url=author.avatar_url
                )

        # Updating the fields
        if fields:
            embed.clear_fields()
            for field in fields:
                embed.add_field(
                    name=field['name'],
                    value=field['value'],
                    inline=field['inline'] if 'inline' in field else True
                )

        # Updating the thumbnail
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)

        # Updating the image
        if image:
            embed.set_image(url=image)

        return embed

    @staticmethod
    def time_log():
        """
        Returns a formatted string representing the current date and time of the system that the program is
        running on. Used in logging to the console.

        :return: A string-formatted version of the current date and time.
        """
        return datetime.datetime.now().strftime('[%m/%d/%Y | %I:%M:%S %p]')

    @staticmethod
    def time_str(inp: str):
        """
        Converts a time input as a string into a utils.TimeLength object containing the represented
        length of time. Handles days, hours, minutes, and seconds.

        :param inp: An input string representing time in the format "#d #h #m #s", where spacing does not matter.
        :return: An instance of a Utils.TimeLength object.
        """
        time_pattern = re.compile(
            "((?P<days>\d+)+d)?((?P<hours>\d+)+h)?((?P<minutes>\d+)+m)?((?P<seconds>\d+)+s)?",
            re.IGNORECASE
        )

        m = time_pattern.match(inp)

        days = int(m.group("days")) if m.group("days") is not None else 0
        hours = int(m.group("hours")) if m.group("hours") is not None else 0
        minutes = int(m.group("minutes")) if m.group("minutes") is not None else 0
        seconds = int(m.group("minutes")) if m.group("minutes") is not None else 0

        return TimeLength(days, hours, minutes, seconds)

    @staticmethod
    async def confirmation(ctx, embed, timeout: float = 30.0):
        """
        Sends an embedded message to the user requesting a response to a yes/no question.

        :param ctx: The context of the user's message to use when sending messages.
        :param embed: The embed to send to the user when asking for confirmation.
        :param timeout: The length of time to wait for user input before returning None.
        :return: The result of the user input, either True, False, or None if no input was given.
        """
        return await Confirmation(embed, timeout).prompt(ctx)


class Confirmation(menus.Menu):
    def __init__(self, embed, timeout):
        super().__init__(timeout=timeout, delete_message_after=True)
        self.embed = embed
        self.result = None

    async def send_initial_message(self, ctx, channel):
        """
        An overwritten version of the default send_initial_message function,
        which is used in order to send the confirmation embedded message

        :param ctx: The context of the invocation that resulted in this confirmation being sent.
        :param channel: The channel to send the message to.
        """
        return await channel.send(embed=self.embed)

    @menus.button('\N{WHITE HEAVY CHECK MARK}')
    async def do_confirm(self, payload):
        self.result = True
        self.stop()

    @menus.button('\N{CROSS MARK}')
    async def do_deny(self, payload):
        self.result = False
        self.stop()

    async def prompt(self, ctx):
        await self.start(ctx, wait=True)
        return self.result


class TimeLength:
    def __init__(self, days, hours, minutes, seconds):
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
