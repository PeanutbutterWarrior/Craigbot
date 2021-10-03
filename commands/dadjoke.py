import discord
import random

import helpers

with open('commands/dadjokes.txt') as file:
    dad_jokes = file.read().splitlines()


def dadjoke(message: discord.Message, webhook_manager: helpers.WebhookManager):
    await message.channel.send(random.choice(dad_jokes))
