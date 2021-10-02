import os
import discord
import re

with open('.env') as env_file:
    for line in env_file.read().split('\n'):
        key, val = line.split('=')
        os.environ[key] = val

TOKEN = os.getenv('DISCORD_TOKEN')

im_pattern = re.compile('i\'?m (.+)', re.IGNORECASE)

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    if message.author.bot:
        return

    if message.content == 'Hi craig':
        await message.channel.send(f'Hi {message.author.display_name}')
        return
    elif (regex_match := im_pattern.search(message.content)) is not None:
        if regex_match.group(1).lower() == 'craig':
            await message.channel.send('You\'re not Craig, I\'m Craig!')
        else:
            await message.channel.send(f'Hi {regex_match.group(1)}, I\'m Craig!')

client.run(TOKEN)
