import sqlite3
import os
import json

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
        c = self.conn.cursor()
        c.execute("INSERT INTO messages VALUES (?,?,?,?,?)", (message.id, message.author.name, message.content, message.channel.name, message.created_at))
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