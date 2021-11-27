import discord
import discord.ext.commands as disc_cmds
import os
import sys
import helpers

class CommandManager(disc_cmds.Cog, name='CommandManager'):
    def __init__(self, bot):
        self.bot = bot

    @disc_cmds.command(name='say')
    async def say(self, ctx, server : discord.Guild, channel : discord.TextChannel, msg):
        owner = await self.bot.is_owner(ctx.author)
        if owner:
            await helpers.send_msg_to(server, channel, msg, None)
        else:
            print('You are not the owner')

    # TODO This command should be used for the bot to update itself
    @disc_cmds.command(name='update')
    async def update(self, ctx):
        print(sys.executable)
        print(sys.argv)
        await ctx.send('you called?')
