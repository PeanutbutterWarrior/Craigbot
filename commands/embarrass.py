import discord
import random
import os.path

with open(os.path.normpath('commands/embarrassing_phrases.txt')) as file:
    embarrassing_phrases = file.read().splitlines()


async def embarrass(message: discord.Message):
    webhook = await message.channel.create_webhook(name='Craighook')
    await webhook.send(random.choice(embarrassing_phrases),
                       username=message.author.display_name,
                       avatar_url=message.author.avatar_url)
