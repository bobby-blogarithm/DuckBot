import discord.ext.commands as disc_cmds

from collections import defaultdict
from daily_reminder import DailyReminder
from economy import Shop, Inventory

class ListenerManager(disc_cmds.Cog, name='ListenerManager'):
    def __init__(self, bot):
        self.bot = bot
        self.daily_reminder = DailyReminder(self.bot)

    @disc_cmds.Cog.listener(name='on_ready')
    async def on_ready(self):
        print('Ready to go!')

    @disc_cmds.Cog.listener(name='on_message')
    async def on_message(self, message):
        # Use a lock to prevent other incoming messages from triggering the daily reminder
        # while the daily reminder is in progress
        async with self.daily_reminder.lock:
            await self.daily_reminder.remind(message)

    @disc_cmds.Cog.listener(name='on_raw_reaction_add')
    async def inv_pages(self, reaction):
        if reaction.member == self.bot.user:
            return None

        inv_server = self.bot.get_guild(reaction.guild_id)
        inv_channel = self.bot.get_channel(reaction.channel_id)
        inv_msg = await inv_channel.fetch_message(reaction.message_id)
        inv = Inventory(inv_server.name, reaction.member.name)

        # Generate pagination for inventory
        pages = defaultdict(list)
        for i, item in enumerate(inv.items):
            page_num = (i // 10)
            pages[page_num].append(item)

        # Get the embed from the inventory and the current page
        inv_embed = inv_msg.embeds[0]
        curr_page = int(inv_embed.footer.text[5:inv_embed.footer.text.find('/') - 1]) - 1
        
        # Remove the reaction
        await inv_msg.remove_reaction(reaction.emoji, reaction.member)

        # Go to next page if they click forward
        if reaction.emoji.name == '▶':
            curr_page += 1 if curr_page + 1 < len(pages) else 0

        # Go to previous page if they click backward
        if reaction.emoji.name == '◀':
            curr_page -= 1 if curr_page - 1 >= 0 else 0

        # Generate the shop content as a message
        name_str = '\n'.join([item.name for item in pages[curr_page]])
        quantity_str = '\n'.join([str(item.quantity) for item in pages[curr_page]])

        inv_embed.title = f'{inv_server.name} Shop'
        inv_embed.set_field_at(0, name='Name', value=name_str if name_str else 'N/A')
        inv_embed.set_field_at(1, name='Quantity', value=quantity_str if quantity_str else 'N/A')
        inv_embed.set_footer(text=f'Page {curr_page + 1} / {len(pages)}')
        await inv_msg.edit(content='', embed=inv_embed)

    @disc_cmds.Cog.listener(name='on_raw_reaction_add')
    async def shop_pages(self, reaction):
        if reaction.member == self.bot.user:
            return None

        shop_server = self.bot.get_guild(reaction.guild_id)
        shop_channel = self.bot.get_channel(reaction.channel_id)
        shop_msg = await shop_channel.fetch_message(reaction.message_id)
        shop = Shop.get_instance(shop_server.name)

        # Generate pagination for shop
        pages = defaultdict(list)
        for i, item in enumerate(shop.items):
            page_num = (i // 10)
            pages[page_num].append(item)

        # Get the embed from the shop and the current page
        shop_embed = shop_msg.embeds[0]
        curr_page = int(shop_embed.footer.text[5:shop_embed.footer.text.find('/') - 1]) - 1
        
        # Remove the reaction
        await shop_msg.remove_reaction(reaction.emoji, reaction.member)

        # Go to next page if they click forward
        if reaction.emoji.name == '▶':
            curr_page += 1 if curr_page + 1 < len(pages) else 0

        # Go to previous page if they click backward
        if reaction.emoji.name == '◀':
            curr_page -= 1 if curr_page - 1 >= 0 else 0

        # Generate the shop content as a message
        name_str = '\n'.join([item.name for item in pages[curr_page]])
        quantity_str = '\n'.join([str(item.quantity) for item in pages[curr_page]])
        cost_str = '\n'.join([str(item.cost) for item in pages[curr_page]])

        shop_embed.title = f'{shop_server.name} Shop'
        shop_embed.set_field_at(0, name='Name', value=name_str if name_str else 'N/A')
        shop_embed.set_field_at(1, name='Quantity', value=quantity_str if quantity_str else 'N/A')
        shop_embed.set_field_at(2, name='Price', value=cost_str if cost_str else 'N/A')
        shop_embed.set_footer(text=f'Page {curr_page + 1} / {len(pages)}')
        await shop_msg.edit(content='', embed=shop_embed)
