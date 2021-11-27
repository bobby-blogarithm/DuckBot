import discord.ext.commands as disc_cmds
import os
import sys

class CommandManager(disc_cmds.Cog, name='CommandManager'):
    def __init__(self, bot):
        self.bot = bot

    @disc_cmds.command(name='update')
    async def update(self, ctx):
        print(sys.executable)
        print(sys.argv)
        await ctx.send('you called?')
