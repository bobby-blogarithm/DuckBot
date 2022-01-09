import asyncio
import discord
import discord.ext.commands as disc_cmds
import helpers

from economy import Economy
from duck_facts import DuckFact

class CommandManager(disc_cmds.Cog, name='CommandManager'):
    def __init__(self, bot):
        self.bot = bot

    @disc_cmds.command(name='say')
    async def say(self, ctx, server : discord.Guild, channel : discord.TextChannel, msg):
        owner = await self.bot.is_owner(ctx.author)
        if owner:
            await helpers.send_msg_to(server, channel, msg, None)
        else:
            print('You are not the owner')

    @disc_cmds.command(name='leaderboard')
    async def reminder_leaderboard(self, ctx, limit: int = 10):
        # TODO Implement pagination
        # Get the rankings from the reminder leaderboard
        economy = Economy(ctx.guild.name)
        rankings = [rank for rank in economy.get_rankings(limit)]

        # Create the leaderboard message and send
        name_string = '\n'.join([rank[1] for rank in rankings])
        point_string = '\n'.join([str(rank[2]) for rank in rankings])
        rank_string = '\n'.join([str(rank[0]) for rank in rankings])

        leaderboard_embed = discord.Embed()
        leaderboard_embed.title = f'Economy Rankings for {ctx.guild.name}'
        leaderboard_embed.add_field(name='Rank', value=rank_string if rank_string else 'N/A')
        leaderboard_embed.add_field(name='Names', value=name_string if name_string else 'N/A')
        leaderboard_embed.add_field(name='Points', value=point_string if point_string else 'N/A')
        await ctx.send(embed=leaderboard_embed)

    @disc_cmds.command(name='duckfact')
    async def duck_fact(self, ctx, *args):
        if len(args) > 0:
            await ctx.send(content='Invalid number of arguments, please try again.')
            return None
        duck = DuckFact()
        image = duck.get_image()
        fact, fact_num = duck.get_fact()

        fact_embed = discord.Embed()
        fact_embed.title = f'Duck Fact #{fact_num}'
        fact_embed.description = fact
        fact_embed.set_image(url=image)

        await ctx.send(embed=fact_embed)

    @disc_cmds.command(name='shop')
    async def shop(self, ctx):
        shop_msg = await ctx.send(content='test shop')
        arrows = ['\U000025C0', '\U000025B6']
        for arrow in arrows:
            await shop_msg.add_reaction(arrow)

    @disc_cmds.command(name='timer')
    async def timer(self, ctx, duration : int, unit='sec', name='', *args):
        if len(args) > 0:
            await ctx.send(content='Invalid number of arguments, please try again.')
            return None

        sec_duration = duration
        if unit in ['min', 'minute', 'minutes', 'm']:
            sec_duration = duration * 60
        elif unit in ['hr', 'hour', 'hours' 'h']:
            sec_duration = duration * 3600
        elif unit in ['day', 'days', 'd']:
            sec_duration = duration * 86400
        elif unit not in ['sec', 'second', 'seconds', 's']:
            await ctx.send(content='Invalid time unit specified, please try again.')
            return None

        padded_name = name + (' ' if name else '')
        
        await ctx.send(content=f'<@{ctx.author.id}> The {padded_name}timer is set for {duration} {unit}(s)', delete_after=sec_duration)
        await asyncio.sleep(sec_duration)
        await ctx.send(content=f'<@{ctx.author.id}> The {padded_name}timer is up!', delete_after=300.0)

    # TODO This command should be used for the bot to update itself
    # ! DEPRECATED for now
    # @disc_cmds.command(name='update')
    # async def update(self, ctx):
    #     print(sys.executable)
    #     print(sys.argv)
    #     await ctx.send('you called?')
