import discord
import discord.ext.commands as disc_cmds
import os
import sys
import helpers
import discord

from daily_reminder import ReminderLeaderboard

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

    @disc_cmds.command(name='leaderboard')
    async def reminder_leaderboard(self, ctx, limit: int = 10):
        # Get the rankings from the reminder leaderboard
        leaderboard = ReminderLeaderboard('data/reminder_leaderboard.csv')
        rankings = leaderboard.get_rankings()

        # Python is stupid and generators don't have iteration limits, so here it is a for-loop with an if statement
        ranks = []
        for i, ranking in enumerate(rankings):
            if i == limit:
                break
            ranks.append(ranking)

        # Create the leaderboard message and send
        leaderboard_embed = discord.Embed()
        leaderboard_embed.add_field(name='Names', value='\n'.join([rank[0] for rank in ranks]))
        leaderboard_embed.add_field(name='Scores', value='\n'.join([str(rank[1]) for rank in ranks]))
        await ctx.send(embed=leaderboard_embed)

    # TODO This command should be used for the bot to update itself
    @disc_cmds.command(name='update')
    async def update(self, ctx):
        print(sys.executable)
        print(sys.argv)
        await ctx.send('you called?')
