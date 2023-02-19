import asyncio
from datetime import datetime
from math import floor
import random
import json
import os

import discord
import discord.ext.commands as disc_cmds
import parsedatetime

import helpers.discord as discord_helpers
from duck_facts import get_fact, get_image
from quack import generate_duck


class CommandManager(disc_cmds.Cog, name='CommandManager'):
    def __init__(self, bot):
        self.bot = bot



    @disc_cmds.command(name='say')
    async def say(self, ctx, server: discord.Guild, channel: discord.TextChannel, msg):
        owner = await self.bot.is_owner(ctx.author)
        if owner:
            await discord_helpers.send_msg_to(server, channel, msg, None)
        else:
            print('You are not the owner')



    @disc_cmds.command(name='leaderboard')
    async def reminder_leaderboard(self, ctx):
        if os.path.isfile('data/leaderboard.json'):
            with open('data/leaderboard.json') as file:
                data = json.load(file)
        
        l_embed = discord.Embed(color=discord.Color.teal())
        l_embed.title = 'Leaderboard Rankings'
        rank = 1
        for name, points in sorted(data.items(), key=lambda x: x[1], reverse=True):
            if rank == 1:
                l_embed.add_field(name=f'#{rank}', value=f'**```🥇{name}: {points}```**')
            elif rank == 2:
                l_embed.add_field(name=f'#{rank}', value=f'**```🥈{name}: {points}```**')
            elif rank == 3:
                l_embed.add_field(name=f'#{rank}', value=f'**```🥉{name}: {points}```**')
            else:
                l_embed.add_field(name=f'#{rank}', value=f'{name}: {points}')
            rank += 1

        await ctx.send(embed=l_embed)



    @disc_cmds.command(name='duckfact')
    async def duck_fact(self, ctx, *args):
        if len(args) > 0:
            return None
        image = await get_image(self.bot.unsplash_access)
        fact, fact_num = get_fact()

        fact_embed = discord.Embed()
        fact_embed.title = f'Duck Fact #{fact_num}'
        fact_embed.description = fact
        fact_embed.set_image(url=image)

        await ctx.send(embed=fact_embed)



    @disc_cmds.command(name='quack')
    async def duck_speak(self, ctx, *args):
        if len(args) > 0:
            await ctx.send(content='Invalid number of arguments, please try again.')
            return None
        duck_say = generate_duck()

        await ctx.send(duck_say)



    @disc_cmds.command(name='r')
    async def roll_ow(self, ctx, *args):
        if len(args) > 1:
            await ctx.send(content='Invalid number of arguments, please try again.')
            return None
        dps_characters = ['Ashe','Bastion','Sojurn','Echo','Genji','Hanzo','Junkrat','McCree','Mei','Pharah','Reaper','Soldier: 76','Sombra','Symmetra', 'Torbjörn','Tracer','Widowmaker']
        tank_characters = ['D.Va','Orisa','Reinhardt','Roadhog','Sigma','Winston','Wrecking Ball','Zarya','Doomfist','Junker Queen','Ramattra']
        support_characters = ['Ana','Baptiste','Lúcio','Mercy','Moira','Brigitte','Zenyatta','Kiriko']

        if len(args) == 1:
            if args[0] == 't':
                msg = random.choice(tank_characters)
            elif args[0] == 's':
                msg = random.choice(support_characters)
            else:
                msg = random.choice(dps_characters)
        else:
            msg = random.choice(dps_characters)
        
        await ctx.send(msg)



    @disc_cmds.command(name='vote')
    async def duckpoll(self, ctx, *args):
        if not args:
            return
            
        duck_up = '<:duck_up:1071706220043452518>'
        duck_down = '<:duck_down:1071706217845624842>'
        
        monkeys_role = discord.utils.get(ctx.guild.roles, name="Monkeys")
        everyone = discord.utils.get(ctx.guild.roles, name="everyone")
        poll_message = " ".join(args)

        if " -e " in poll_message:
            message = await ctx.send(f"***\\*QUACK\\** DUCK POLL BELOW! {everyone.mention}\n----------------------------------------------** \n {poll_message}")
        elif " -m " in poll_message:
            message = await ctx.send(f"***\\*QUACK\\** DUCK POLL BELOW! {monkeys_role.mention}\n----------------------------------------------** \n {poll_message}")
        else:
            message = await ctx.send(f"***\\*QUACK\\** DUCK POLL BELOW! \n----------------------------------------------** \n {poll_message}")

        await message.add_reaction(duck_up)
        await message.add_reaction(duck_down)



    @disc_cmds.command(name='announce')
    async def announce(self, ctx, *args):
        if len(args) == 0 or ctx.message.channel.id != 845824966561890354:
            return
        if not discord.utils.get(ctx.message.author.roles, name='Admin'):
            await ctx.send("You don't have permission to make an announcement.")
            return

        monkeys_role = discord.utils.get(ctx.guild.roles, name="Monkeys")
        announcement = " ".join(args)
        ann_channel = self.bot.get_channel(257701006521925633)

        await ann_channel.send(f"***\\*QUACK\\** ANNOUNCEMENT INCOMING! {monkeys_role.mention}\n--------------------------------------------------------** \n {announcement}")



    @disc_cmds.command(name='timer')
    async def timer(self, ctx, *args):
        message = ' '.join(args)

        # Create a Calendar instance for time parsing
        cal = parsedatetime.Calendar()

        # Parse the message and obtain time delta
        curr_time = datetime.now()
        # res format: (datetime, result_code, start_idx, end_idx, matched_string)
        res = cal.nlp(message)

        # If the nlp returned None type, the parser failed to parse the time
        if not res:
            await ctx.send(content='Failed to parse time duration. Please try again.')
            return None

        res = res[0]
        time_diff = res[0] - curr_time

        # If the timediff is negative, return an error
        if time_diff.total_seconds() < 0:
            await ctx.send(content='The time specified had already expired in the past. Please try again.')
            return None

        # Offset the lost second due to processing (for display only)
        sec_duration = int(floor(time_diff.total_seconds() + 1))

        # Obtain the reminder content
        timer_name = ''.join(message[i] for i in range(len(message)) if i < res[2] or i >= res[3]).strip()
        if timer_name:
            padded_name = '\"' + timer_name + '\" '
        else:
            padded_name = ''

        # Format the output time string
        days, remainder = divmod(sec_duration, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        time_str = [(days, 'day'), (hours, 'hour'), (minutes, 'minute'), (seconds, 'second')]

        # Function to handle converting the time unit into the correct string equivalent
        ftime = lambda x, unit: f'{int(x)} {unit}{"s" if x > 1 else ""}'

        # Only put in the time units that are more than 0 in our final formatted string
        time_str = [ftime(*t) for t in time_str if t[0] > 0]

        # Add 'and' if the final time has more than 2 time units
        time_str[-1] = f'and {time_str[-1]}' if len(time_str) > 2 else time_str[-1]

        # Join string together
        time_str = ', '.join(time_str)

        await ctx.send(content=f'<@{ctx.author.id}> The {padded_name}timer is set to expire in {time_str}',
                       delete_after=sec_duration)
        # Here we use actual timediff here to make our timer as accurate as possible
        await asyncio.sleep(time_diff.total_seconds())
        await ctx.send(content=f'<@{ctx.author.id}> The {padded_name}timer is up!', delete_after=300.0)



    @disc_cmds.command(name='cum')
    async def cum(self, ctx, *args):
        if os.path.isfile('data/cum.json'):
            with open('data/cum.json') as file:
                data = json.load(file)
        
        c_embed = discord.Embed(color=0xFFFFFF)
        c_embed.title = 'The Cum Count'
        rank = 1
        for name, count in sorted(data.items(), key=lambda x: x[1], reverse=True):
            if rank == 1:
                c_embed.add_field(name=f'#{rank}', value=f'😈 {name}: {count}')
            else:
                c_embed.add_field(name=f'#{rank}', value=f'{name}: {count}')
            rank += 1

        await ctx.send(embed=c_embed)