import discord.ext.commands as disc_cmds

from daily_reminder import DailyReminder

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

    @disc_cmds.Cog.listener(name='on_raw_reaction_add')
    async def on_raw_reaction_add(self, reaction):
        print(reaction.message_id)