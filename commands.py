import discord
import os.path
import random

import helpers

commands = {}


class Command:
    def __init__(self, function, name, description, usage):
        self.name = name
        self.description = description
        self.usage = usage
        self.function = function

    async def __call__(self, message: discord.Message, webhook_manager: helpers.WebhookManager, *args):
        if helpers.WebhookManager in self.function.__annotations__.values():
            await self.function(message, webhook_manager, *args)
        else:
            await self.function(message, *args)


def command(name, description, usage=''):
    def wrapper(func):
        to_return = Command(func, name, description, name + usage)
        commands[name] = to_return
        return to_return
    return wrapper


with open(os.path.normpath('data/embarrassing_phrases.txt')) as file:
    embarrassing_phrases = file.read().splitlines()

with open(os.path.normpath('data/fun_facts.txt')) as file:
    fun_facts = file.read().splitlines()

with open('data/dadjokes.txt') as file:
    dad_jokes = file.read().splitlines()


@command(name='embarrass',
         description='Embarrass yourself or others',
         usage=' [person]')
async def embarrass(message: discord.Message, webhook_manager: helpers.WebhookManager):
    webhook = await webhook_manager.get_webhook(message.channel)
    await webhook.send(random.choice(embarrassing_phrases),
                       username=message.author.display_name,
                       avatar_url=message.author.avatar_url)


@command(name='funfact',
         description='Get a fun fact from Craig')
async def funfact(message: discord.Message):
    await message.channel.send(random.choice(fun_facts))


@command(name='dadjoke',
         description='Have Craig tell you a dad joke')
async def dadjoke(message: discord.Message):
    await message.channel.send(random.choice(dad_jokes))
