from collections import defaultdict

import discord.ext.commands as disc_cmds

from daily_reminder import DailyReminder
from economy import Economy
from quack import on_message as quack_message


class ListenerManager(disc_cmds.Cog, name='ListenerManager'):
    def __init__(self, bot):
        self.bot = bot
        self.daily_reminder = DailyReminder(self.bot)

    @disc_cmds.Cog.listener(name='on_ready')
    async def on_ready(self):
        print('Ready to go!')

    @disc_cmds.Cog.listener(name='on_message')
    async def on_message(self, message):
        # Use a lock to prevent other incoming messages from triggering the daily reminder
        # while the daily reminder is in progress
        async with self.daily_reminder.lock:
            await self.daily_reminder.remind(message)
        
        await quack_message(message)

    # Listener for leaderboard command
    @disc_cmds.Cog.listener(name='on_raw_reaction_add')
    async def lb_pages(self, reaction):
        if reaction.member == self.bot.user:
            return None

        lb_server = self.bot.get_guild(reaction.guild_id)
        lb_channel = self.bot.get_channel(reaction.channel_id)
        lb_msg = await lb_channel.fetch_message(reaction.message_id)

        # Obtain the rankings for the current server
        economy = Economy.get_instance(lb_server.name)
        rankings = [rank for rank in economy.get_rankings()]

        # Since the scores are stored with userid, we translate them to usernames for presentation
        usernames = await lb_server.query_members(user_ids=[rank[1] for rank in rankings], limit=100)
        for rank, user in zip(rankings, usernames):
            rank[1] = user

        # Generate pagination for leaderboard
        pages = defaultdict(list)
        for i, item in enumerate(rankings):
            page_num = (i // 10)
            pages[page_num].append(item)

        # Get the embed from the leaderboard and the current page
        lb_embed = lb_msg.embeds[0]
        curr_page = int(lb_embed.footer.text[5:lb_embed.footer.text.find('/') - 1]) - 1

        # Check if this is on leaderboard message
        if 'Economy' not in lb_embed.title:
            return None

        # Remove the reaction
        await lb_msg.remove_reaction(reaction.emoji, reaction.member)

        # Go to next page if they click forward
        if reaction.emoji.name == '▶':
            curr_page += 1 if curr_page + 1 < len(pages) else 0

        # Go to previous page if they click backward
        if reaction.emoji.name == '◀':
            curr_page -= 1 if curr_page - 1 >= 0 else 0

        # Select 10 entries for the current page
        lower_bound = curr_page * 10
        upper_bound = curr_page * 10 + 10
        if curr_page == len(pages) - 1:
            upper_bound = len(rankings)
        rankings_current = rankings[lower_bound: upper_bound]
        # Create the leaderboard message
        name_string = '\n'.join([rank[1] for rank in rankings_current])
        point_string = '\n'.join([str(rank[2]) for rank in rankings_current])
        rank_string = '\n'.join([str(rank[0]) for rank in rankings_current])

        lb_embed.title = f'Economy Rankings for {lb_server}'
        lb_embed.set_field_at(0, name='Rank', value=rank_string if rank_string else 'N/A')
        lb_embed.set_field_at(1, name='Names', value=name_string if name_string else 'N/A')
        lb_embed.set_field_at(2, name='Points', value=point_string if point_string else 'N/A')
        lb_embed.set_footer(text=f'Page {curr_page + 1} / {len(pages)}')
        await lb_msg.edit(content='', embed=lb_embed)