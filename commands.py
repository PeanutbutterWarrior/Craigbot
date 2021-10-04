import discord
import os.path
import random

import helpers

with open(os.path.normpath('commands/embarrassing_phrases.txt')) as file:
    embarrassing_phrases = file.read().splitlines()

with open(os.path.normpath('commands/fun_facts.txt')) as file:
    fun_facts = file.read().splitlines()

with open('commands/dadjokes.txt') as file:
    dad_jokes = file.read().splitlines()


async def embarrass(message: discord.Message, webhook_manager):
    webhook = await webhook_manager.get_webhook(message.channel)
    await webhook.send(random.choice(embarrassing_phrases),
                       username=message.author.display_name,
                       avatar_url=message.author.avatar_url)


async def funfact(message: discord.Message, webhook_manager):
    await message.channel.send(random.choice(fun_facts))


def dadjoke(message: discord.Message, webhook_manager: helpers.WebhookManager):
    await message.channel.send(random.choice(dad_jokes))
