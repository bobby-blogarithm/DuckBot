import discord
import discord.ext.commands as disc_cmds


# Send a message on a specific server to a specific channel
async def send_msg_to(server: discord.Guild, channel: discord.TextChannel, msg, atchmt):
    # Verify that the channel we are sending to is in the server we intend to sent to
    send_channel = channel if channel == discord.utils.get(server.channels, id=channel.id) else discord.utils.get(
        server.channels, name=channel.name)

    if atchmt:
        attachment = discord.File(atchmt)
        await send_channel.send(content=msg, file=attachment)
    else:
        await send_channel.send(content=msg)


class PaginatedMessage(disc_cmds.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.paged_msg = None

    @disc_cmds.Cog.listener(name='on_raw_reaction_add')
    async def switch_page(self, reaction):
        if reaction.member != self.bot.user:
            pass

    def cmd_triggered(self, msg):
        self.paged_msg = msg
