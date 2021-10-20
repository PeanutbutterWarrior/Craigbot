import os
import discord
import re

import commands
import helpers

shut_ups = {'shut up',
            'shut your up',
            'stfu',
            'shut the fuck up',
            'shut ur up',
            'shut the hell your mouth',
            'shut the hell your up'}


class CustomClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = 'c!'
        self._im_pattern = re.compile('(?:^| )i\'?m (.+)', re.IGNORECASE)
        self._is_cool_pattern = re.compile('([^ ]+) (?:is|are) cool', re.IGNORECASE)
        self.webhook_manager = helpers.WebhookManager()
        self.version = '1.0.0'
        
    async def on_ready(self):
        await self.webhook_manager.init(self)
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        if message.author.bot:
            return

        if message.content.startswith(self.prefix):
            await self.call_command(message)

        if message.content == 'Hi craig':
            await message.channel.send(f'Hi {message.author.display_name}')
        # Checks for I'm ------
        elif (regex_match := self._im_pattern.search(message.content)) is not None:
            if regex_match.group(1).lower() == 'craig':
                await message.channel.send('You\'re not Craig, I\'m Craig!')
            else:
                await message.channel.send(f'Hi {regex_match.group(1)}, I\'m Craig!')
        # Checks for shut up
        elif any(shut_up in message.content.lower() for shut_up in shut_ups):
            await message.channel.send(f'Listen here {message.author.display_name}, I will not tolerate you saying those '
                                       f'bloody words that consist of the letters \'s h u t  u p\' in this server, '
                                       f'so take your own advice and close thine god damn mouth in the name of the '
                                       f'christian minecraft server owner!')
        # Checks for ----- is cool
        elif (regex_match := self._is_cool_pattern.search(message.content)) is not None:
            await message.channel.send(f'{regex_match.group(1).capitalize()} may be cool, but Home Depot is cooler. We sell '
                                       f'top of the line tools, amazing DIY construction products, and premium services '
                                       f'for the discerning customer. Come down today to buy a new drill, or a razor '
                                       f'sharp saw. We might even sell {regex_match.group(1).lower()}!')

    async def call_command(self, message: discord.Message):
        command_name, *arguments = message.content[len(self.prefix):].split(' ')
        if command_name in commands.commands:
            await commands.commands[command_name](message, self, *arguments)


if __name__ == '__main__':
    with open('.env') as env_file:
        for line in env_file.read().split('\n'):
            key, val = line.split('=')
            os.environ[key] = val

    TOKEN = os.getenv('DISCORD_TOKEN')

    client = CustomClient()
    client.run(TOKEN)
