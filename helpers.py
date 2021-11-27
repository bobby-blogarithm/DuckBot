import discord
from dateutil import tz

"""
    This file is dedicated to utility and helper functions that
    are NOT associated with a specific class or feature
"""

# Converts the current time from one timezone to another
def convert_tz(current_time, origin_tz, desired_tz):
    from_tz = tz.gettz(origin_tz)
    to_tz = tz.gettz(desired_tz)
    result = current_time.replace(tzinfo=from_tz)

    return result.astimezone(to_tz)

# Send a message on a specific server to a specific channel
async def send_msg_to(msg_server, msg_channel, server, channel, msg, fp):
    if msg_server.name == server and msg_channel.name == channel:
        attachment = discord.File(fp)
        await msg_channel.send(content=msg, file=attachment)