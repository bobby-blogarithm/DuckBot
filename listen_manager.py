import sqlite3

import discord.ext.commands as disc_cmds

from daily_reminder import DailyReminder
from quack import on_message as quack_message


class ListenerManager(disc_cmds.Cog, name='ListenerManager'):
    def __init__(self, bot):
        self.bot = bot
        self.daily_reminder = DailyReminder(self.bot)
        self.conn = sqlite3.connect('messages.sqlite')

    @disc_cmds.Cog.listener(name='on_ready')
    async def on_ready(self):
        print('Ready to go!')

    @disc_cmds.Cog.listener(name='on_message')
    async def on_message(self, message):
        # Use a lock to prevent other incoming messages from triggering the daily reminder
        # while the daily reminder is in progress
        async with self.daily_reminder.lock:
            await self.daily_reminder.remind(message)

        c = self.conn.cursor()
        c.execute("INSERT INTO messages VALUES (?,?,?,?,?)", (message.id, message.author.name, message.content, message.channel.name, message.created_at))
        self.conn.commit()
        
        await quack_message(message)