import discord
import random
import os.path

with open(os.path.normpath('commands/embarrassing_phrases.txt')) as file:
    embarrassing_phrases = file.read().splitlines()


async def embarrass(message: discord.Message, webhook_manager):
    webhook = await webhook_manager.get_webhook(message.channel)
    await webhook.send(random.choice(embarrassing_phrases),
                       username=message.author.display_name,
                       avatar_url=message.author.avatar_url)
