import discord
import yaml
import datetime as dt

from dateutil import tz

CONFIG_FILE = 'config.yml'

class DuckBot(discord.Client):
    def __init__(self, *args, **kwargs):
        # Load bot config file
        with open(CONFIG_FILE) as config_file:
            self.config = yaml.safe_load(config_file)
        self.token = self.config['token']
        self.name = 'Duck?'

        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print('Ready to go!')

    async def on_message(self, message):
        # Extract information about the message
        msg_server = message.guild
        msg_channel = message.channel
        msg_user = message.author
        send_time = message.created_at

        # Reminder server info
        remind_server = 'Rip Daddy Weave'
        remind_channel = 'argle-bargle'
        remind_msg = 'Congratulations! You\'re the first message of the day. Have a reminder! :)'

        # If this bot was the one who sent the message, then ignore
        if msg_user.name == self.name:
            return None

        # Date format used by the bot
        date_fmt = '%m-%d-%Y'

        # Convert the message time from UTC to AZ time
        utc_tz = tz.gettz('UTC')
        az_tz = tz.gettz('America/Phoenix')
        send_time = send_time.replace(tzinfo=utc_tz)
        send_time = send_time.astimezone(az_tz)

        # If we find a message from "yesterday" and have not sent the daily reminder, send it
        if 'last_message' in self.config.keys():
            last_message_time = dt.datetime.strptime(self.config['last_message'], date_fmt)

            if last_message_time.date().day < send_time.date().day:
                await self.send_msg_to(msg_server, msg_channel, remind_server, remind_channel, remind_msg, 'images/vaporeon.png')

        # Set this message as the last message
        self.config['last_message'] = send_time.strftime(date_fmt)
        with open(CONFIG_FILE, 'w') as config_file:
            yaml.safe_dump(self.config, config_file)

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