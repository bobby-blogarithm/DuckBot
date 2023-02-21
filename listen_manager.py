import datetime
import json
import os
import sqlite3
import pytz

import discord.ext.commands as disc_cmds
import discord.utils

from daily_reminder import DailyReminder
from quack import on_message as quack_message


class ListenerManager(disc_cmds.Cog, name='ListenerManager'):
    def __init__(self, bot):
        self.bot = bot
        self.daily_reminder = DailyReminder(self.bot)
        self.conn = sqlite3.connect('messages.sqlite')

    @disc_cmds.Cog.listener(name='on_ready')
    async def on_ready(self):
        self.bot.current_guild = discord.utils.get(self.bot.guilds, name=self.bot.remind_server)
        if not self.bot.current_guild:
            print(f'Warning: remind server {self.bot.remind_server} inaccessible to bot!')
        print('Ready to go!')

    @disc_cmds.Cog.listener(name='on_message')
    async def on_message(self, message):
        c = self.conn.cursor()
        c.execute("INSERT INTO messages VALUES (?,?,?,?,?)",
                  (message.id, message.author.name, message.content, message.channel.name, message.created_at))
        self.conn.commit()

        if 'cum' in message.content and '?cum' not in message.content:
            if os.path.isfile('data/cum.json'):
                with open('data/cum.json') as file:
                    data = json.load(file)

            if message.author.name in data:
                data[message.author.name] += 1
            else:
                data[message.author.name] = 1

            with open('data/cum.json', 'w') as f:
                json.dump(data, f)

        await self.daily_reminder.remind(message)
        await quack_message(message)

    @disc_cmds.Cog.listener(name='on_raw_reaction_add')
    async def on_pin_reaction(self, reaction_event):
        if reaction_event.emoji.name != '📌':
            return
        if reaction_event.user_id == self.bot.user.id
            return

        # Get the destination channel
        channel = discord.utils.get(self.bot.current_guild.text_channels, name=self.bot.pin_channel)
        if not channel:
            print(f'Error: the pin channel {channel} does not exist')
            return

        pin_msg = await self.bot.current_guild.get_channel(reaction_event.channel_id)\
            .fetch_message(reaction_event.message_id)
        if pin_msg.channel == channel:
            # message cannot be on the pin channel
            return
        
        reaction = next((r for r in pin_msg.reactions if r.emoji == '📌'), None)
        if not reaction:
            print(f'Warning: 📌 emoji not found among the reactions, message id: {reaction_event.message_id}')
            return

        users = [user async for user in reaction.users()]
        if self.bot.user.id in [user.id for user in users]:
            # message is already pinned
            return
        
        # Mark as pinned to prevent the double-pinning
        await pin_msg.add_reaction('📌')
        
        pin_requester = users[0].id
        msg_author = pin_msg.author.id
        msg_content = pin_msg.content
        # Cap the message length at 600
        if len(msg_content) > 600:
            msg_content = msg_content[:600] + '...'
        msg_channel = pin_msg.channel
        msg_link = pin_msg.jump_url
        msg_attachments = pin_msg.attachments
        msg_id = pin_msg.id
        msg_time = pin_msg.created_at
        msg_embed = pin_msg.embeds

        # Assemble the pin message
        content = f'<@{pin_requester}> just pinned a message from <#{msg_channel.id}>'
        embed = discord.Embed()
        # embed.title = msg_author
        embed.description = f'<@{msg_author}>: {msg_content}'

        # Only take the first attachment/embed if there are any
        if msg_attachments:
            attachment_url = msg_attachments[0].url
            embed.set_image(url=attachment_url)

            # Embeds doesn't support videos, show its filename instead
            if 'video' in msg_attachments[0].content_type:
                embed.description += f'\n`<{msg_attachments[0].filename}>`'

        embeds = []

        # Example timestring: 06/14/2022 6:03 PM MST
        msg_time_mst = (msg_time - datetime.timedelta(hours=7)).strftime('%m/%d/%Y %I:%M %p MST')
        embed.set_footer(text=f'Message ID {msg_id} · Posted {msg_time_mst}')
        embeds.append(embed)

        if msg_embed:
            embeds.append(msg_embed[0])

        embed.description += f'\n\n**[Jump to the message]({msg_link})**'

        # Mention the users but do not actually ping them
        await channel.send(content=content, embeds=embeds, allowed_mentions=discord.AllowedMentions.none())

