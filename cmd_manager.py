import discord
import discord.ext.commands as disc_cmds
import helpers
import discord

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

    # TODO This command should be used for the bot to update itself
    # ! DEPRECATED for now
    # @disc_cmds.command(name='update')
    # async def update(self, ctx):
    #     print(sys.executable)
    #     print(sys.argv)
    #     await ctx.send('you called?')
