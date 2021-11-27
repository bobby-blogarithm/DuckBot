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
async def send_msg_to(server : discord.Guild, channel : discord.TextChannel, msg, atchmt):
    # Verify that the channel we are sending to is in the server we intend to sent to
    send_channel = channel if channel == discord.utils.get(server.channels, id=channel.id) else discord.utils.get(server.channels, name=channel.name)

    if atchmt:
        attachment = discord.File(atchmt)
        await send_channel.send(content=msg, file=attachment)
    else:
        await send_channel.send(content=msg)