import datetime as dt
import json
import os
import random

import discord
import pytz

from duck_facts import get_image


class DailyReminder:
    def __init__(self, bot):
        self.bot = bot
        self.remind_title = ["Congratulations!", "Great job!", "Awesome work!", "Well done!", "You nailed it!",
                             "Fantastic!", "Outstanding!", "Excellent work!", "Impressive!", "Brilliant job!",
                             "Superb!", "Amazing work!", "You're a rockstar!", "Keep up the great work!", "Way to go!",
                             "Terrific job!", "You're killing it!", "Fabulous!", "Sensational!", "Exceptional work!",
                             "You're a superstar!", "Remarkable job!", "Incredible!", "You're crushing it!",
                             "Top-notch!", "Stellar job!", "You're a champ!", "Splendid!", "You're a winner!",
                             "Breathtaking!", "You're amazing!", "You're unstoppable!", "You're a shining star!",
                             "You're a superstar!", "You're one in a million!", "You're a star performer!",
                             "You're a wizard!", "You're a miracle worker!", "You're the best!", "You're a virtuoso!",
                             "You're a pro!", "You're a natural!", "You're a gifted problem solver!",
                             "You're a gifted communicator!", "You have an amazing attitude!",
                             "You're an invaluable part of the team!", "You're a real people person!",
                             "You have a heart of gold!", "You're a true professional!",
                             "You're a valued member of the team!", "You're a respected leader!",
                             "You have an exceptional work ethic!", "You're a real go-getter!",
                             "You have a positive influence on others!", "You're a true friend!",
                             "You're an outstanding asset to the team!", "You have a sharp mind!",
                             "You're a true visionary!", "You have an amazing spirit!",
                             "You're an extraordinary problem solver!", "You're a natural leader!",
                             "You're a skilled negotiator!"]
        self.remind_msg = '<:duck_up:1071706220043452518> The first message of the day, enjoy your points <:duck_up:1071706220043452518>'
        self.remind_img = None
        self.tz = pytz.timezone('America/Phoenix')

    async def build_remind(self):
        self.remind_img = await get_image(self.bot.unsplash_access)

        # Reminder
        embed = discord.Embed(color=discord.Color.gold())
        embed.title = random.choice(self.remind_title)
        embed.description = self.remind_msg
        embed.set_image(url=self.remind_img)
        return embed

    async def remind(self, msg):
        # Message info
        channel = msg.channel
        msg_user = msg.author
        send_time = msg.created_at.replace(tzinfo=pytz.utc).astimezone(self.tz)

        # Time info
        now = dt.datetime.now(self.tz)

        # If this bot was the one who sent the message or the bot receives a DM, then ignore
        if msg_user == self.bot.user:  # or msg.channel.id != 257701006521925633:
            return None

        if not os.path.isfile('data/remind.txt'):
            fresh = now - dt.timedelta(days=2)
            with open('data/remind.txt', "w") as file:
                file.write(fresh.strftime('%Y/%m/%d'))

        with open('data/remind.txt', 'r') as file:
            file_contents = file.read()
        last_date = self.tz.localize(dt.datetime.strptime(file_contents, '%Y/%m/%d'))

        if send_time.hour >= 0 and send_time.hour < 6:
            if (send_time - last_date).days > 1:
                await channel.send(embed=await self.build_remind())
                with open('data/remind.txt', "w") as file:
                    file.write((now - dt.timedelta(days=1)).strftime('%Y/%m/%d'))

                with open('data/leaderboard.json', 'r+') as file:
                    # Load the data from the file
                    data = json.load(file)

                    # Modify the data
                    if msg_user.name in data:
                        data[msg_user.name] += 10
                    else:
                        data[msg_user.name] = 10

                    # Write the modified data back to the file
                    file.seek(0)
                    json.dump(data, file)
                    file.truncate()

        else:
            if (send_time - last_date).days > 0:
                await channel.send(embed=await self.build_remind())
                with open('data/remind.txt', "w") as file:
                    file.write(now.strftime('%Y/%m/%d'))

                with open('data/leaderboard.json', 'r+') as file:
                    # Load the data from the file
                    data = json.load(file)

                    # Modify the data
                    if msg_user.name in data:
                        data[msg_user.name] += 10
                    else:
                        data[msg_user.name] = 10

                    # Write the modified data back to the file
                    file.seek(0)
                    json.dump(data, file)
                    file.truncate()
