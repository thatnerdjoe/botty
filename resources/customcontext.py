import discord
from discord import AllowedMentions, File
from discord.errors import InvalidArgument
from discord.ext import commands

"""
*******************************************************************************
This is a custom Context class that is used to modify the base Context that
the bot will use, in order to allow easier responding to contexts. In order
for the custom context to be applied, it is also necessary to override the
get_context method in the discord.ext.commands.Bot class as well.

Authors: Houghton Mayfield (@Heroicos_HM)
Version: 0.1
Date: 03-26-2021
*******************************************************************************
"""


class CustomContext(commands.Context):
    async def confirm(self):
        """
        Adds a check mark emoji reaction to the message the context refers to.
        """
        try:
            await self.message.add_reaction('\N{WHITE HEAVY CHECK MARK}')
        except discord.HTTPException:
            # Sometimes errors can occur with adding reactions, like lacking permissions,
            # so the bot will just ignore that here.
            pass

    async def send(self, content=None, *, tts=False, embed=None,
                   file=None, files=None, delete_after=None,
                   nonce=None, allowed_mentions=None,
                   reference=None, mention_author=None):
        """
        A modified form of the default send command for a context. The only change to the command
        is that any purely plaintext responses are converted into an embedded message for the
        sake of cleanliness.
        """

        channel = await self._get_channel()
        state = self._state

        content = str(content) if content is not None else None

        # This segment is the only one that was modified.
        # It simply creates an embedded message for the response instead of a plaintext response
        # if an embedded message is not included.
        if embed is not None:
            embed = embed.to_dict()
        elif content is not None:
            embed = self.bot.utils.get_embed(desc=content).to_dict()
            content = None

        if allowed_mentions is not None:
            if state.allowed_mentions is not None:
                allowed_mentions = state.allowed_mentions.merge(allowed_mentions).to_dict()
            else:
                allowed_mentions = allowed_mentions.to_dict()
        else:
            allowed_mentions = state.allowed_mentions and state.allowed_mentions.to_dict()

        if mention_author is not None:
            allowed_mentions = allowed_mentions or AllowedMentions().to_dict()
            allowed_mentions['replied_user'] = bool(mention_author)

        if reference is not None:
            try:
                reference = reference.to_message_reference_dict()
            except AttributeError:
                raise InvalidArgument('reference parameter must be Message or MessageReference') from None

        if file is not None and files is not None:
            raise InvalidArgument('cannot pass both file and files parameter to send()')

        if file is not None:
            if not isinstance(file, File):
                raise InvalidArgument('file parameter must be File')

            try:
                data = await state.http.send_files(
                    channel.id, files=[file], allowed_mentions=allowed_mentions,
                    content=content, tts=tts, embed=embed, nonce=nonce,
                    message_reference=reference
                )
            finally:
                file.close()

        elif files is not None:
            if len(files) > 10:
                raise InvalidArgument('files parameter must be a list of up to 10 elements')
            elif not all(isinstance(file, File) for file in files):
                raise InvalidArgument('files parameter must be a list of File')

            try:
                data = await state.http.send_files(
                    channel.id, files=files, content=content, tts=tts,
                    embed=embed, nonce=nonce, allowed_mentions=allowed_mentions,
                    message_reference=reference
                )
            finally:
                for f in files:
                    f.close()
        else:
            data = await state.http.send_message(
                channel.id, content, tts=tts, embed=embed,
                nonce=nonce, allowed_mentions=allowed_mentions,
                message_reference=reference
            )

        ret = state.create_message(channel=channel, data=data)
        if delete_after is not None:
            await ret.delete(delay=delete_after)
        return ret


class CustomBot(commands.Bot):
    async def get_context(self, message, *, cls=CustomContext):
        # By passing the CustomContext subclass to the super() method,
        # this tells the bot to use that class for contexts.
        return await super().get_context(message, cls=cls)
