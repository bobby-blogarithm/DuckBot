import asyncio
import helpers

class DailyReminder:
    def __init__(self, bot):
        self.lock = asyncio.Lock()
        self.cd = 0
        self.prev = None
        self.bot = bot

    async def remind(self, message):
        # Extract information about the message
        msg_server = message.guild
        msg_channel = message.channel
        msg_user = message.author
        send_time = message.created_at

        # Reminder server info
        remind_server = self.bot.remind_server
        remind_channel = self.bot.remind_channel
        remind_msg = 'Congratulations! You\'re the first message of the day. Have a reminder! :)'

        # If this bot was the one who sent the message or the bot receives a DM, then ignore
        if msg_user == self.bot.user or not msg_server or not msg_channel:
            return None

        # Convert the message time from UTC to AZ time
        send_time = helpers.convert_tz(send_time, 'UTC', 'America/Phoenix')

        # The earliest time to find the previous reminder is at yesterday 6 am
        earliest_prev_time = send_time.replace(day=send_time.day - 1, hour=6, minute=0, second=0, microsecond=0)
        earliest_prev_time = helpers.convert_tz(earliest_prev_time, 'America/Phoenix', 'UTC')
        earliest_prev_time = earliest_prev_time.replace(tzinfo=None)

        # Get the last message this bot sent
        if not self.prev:
            last_message = await msg_channel.history(after=earliest_prev_time, oldest_first=False).get(author=self.bot.user, content=remind_msg)
        else:
            last_message = self.prev

        # Only do this check if we actually find there was a last reminder message
        if last_message:
            last_message_time = helpers.convert_tz(last_message.created_at, 'UTC', 'America/Phoenix')

            # If the last message was not from "yesterday" or is before 6 AM AZT then do nothing
            if last_message_time.date().day >= send_time.day or send_time.hour < 6:
                return None

        # If the server and channel the message came from are not the server and channel we want to remind
        # then ignore
        if msg_server.name != remind_server or msg_channel.name != remind_channel:
            return None

        # Send the daily reminder if all these checks are passed
        await helpers.send_msg_to(msg_server, msg_channel, remind_msg, 'images/vaporeon.png')
        
        # Set the previous daily reminder to this one
        self.prev = last_message

        # Set the cooldown for the daily reminder until tomorrow at 6 am
        self.cd = send_time.replace(day=send_time.day + 1, hour=6, minute=0, second=0, microsecond=0) - send_time
        await asyncio.sleep(self.cd.seconds)