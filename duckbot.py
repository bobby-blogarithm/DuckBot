import discord
import yaml
import datetime as dt
import helpers

CONFIG_FILE = 'config.yml'

class DuckBot(discord.Client):
    def __init__(self, *args, **kwargs):
        # Load bot config file
        with open(CONFIG_FILE) as config_file:
            self.config = yaml.safe_load(config_file)
        self.token = self.config['token']
        self.name = 'Duck?'
        self.daily_reminder_in_progress = False

        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print('Ready to go!')

    async def on_message(self, message):
        # Daily reminder event
        await self.daily_reminder(message)

    # Daily reminder
    async def daily_reminder(self, message):
        # Extract information about the message
        msg_server = message.guild
        msg_channel = message.channel
        msg_user = message.author
        send_time = message.created_at

        # Reminder server info
        remind_server = 'Rip Daddy Weave'
        remind_channel = 'argle-bargle'
        remind_msg = 'Congratulations! You\'re the first message of the day. Have a reminder! :)'

        # If this bot was the one who sent the message or the daily reminder is already in progress, then ignore
        if msg_user.name == self.name or self.daily_reminder_in_progress:
            return None

        # Convert the message time from UTC to AZ time
        send_time = helpers.convert_tz(send_time, 'UTC', 'America/Phoenix')

        # Get the message before the current message was sent (i.e. get the last message)
        last_message = await msg_channel.history(limit=2).flatten()

        # Only do this check if we actually find there was a last message
        if len(last_message) == 2:
            last_message = last_message[1]
            last_message_time = helpers.convert_tz(last_message.created_at, 'UTC', 'America/Phoenix')

            # If the last message was not from "yesterday" or is before 6 AM AZT then do nothing
            if last_message_time.date().day >= send_time.date().day or send_time.time().hour < 6:
                return None

        # Send the daily reminder if all these checks are passed
        self.daily_reminder_in_progress = True
        await self.send_msg_to(msg_server, msg_channel, remind_server, remind_channel, remind_msg, 'images/vaporeon.png')
        self.daily_reminder_in_progress = False

    # Helper function to send a message on a specific server to a specific channel
    async def send_msg_to(self, msg_server, msg_channel, server, channel, msg, fp):
        if msg_server.name == server and msg_channel.name == channel:
            attachment = discord.File(fp)
            await msg_channel.send(content=msg, file=attachment)

def main():
    # Create client for bot
    client = DuckBot()

    # Connect client to discord
    client.run(client.token)
    
if __name__ == '__main__':
    main()