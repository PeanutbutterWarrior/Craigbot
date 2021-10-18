import discord
import os.path
import random

import helpers
from main import CustomClient

commands = {}


class Command:
    def __init__(self, function, name, description, explanation, usage):
        self.name = name
        self.description = description
        self.usage = usage
        self.function = function
        self.explanation = explanation

    async def __call__(self, message: discord.Message, client: CustomClient, *args):
        await self.function(message, client, *args)


def command(name, description, explanation=None, usage=''):
    if explanation is None:
        explanation = description

    def wrapper(func):
        to_return = Command(func, name, description, explanation, name + usage)
        commands[name] = to_return
        return to_return

    return wrapper


with open(os.path.normpath('data/embarrassing_phrases.txt')) as file:
    embarrassing_phrases = file.read().splitlines()

with open(os.path.normpath('data/fun_facts.txt')) as file:
    fun_facts = file.read().splitlines()

with open('data/dadjokes.txt') as file:
    dad_jokes = file.read().splitlines()

with open('data/advice.txt') as file:
    advice = file.read().splitlines()


@command(name='embarrass',
         description='Embarrass yourself or others',
         explanation='Send an embarrassing message as you, or another person. Provide a person by @pinging them.',
         usage=' [person]')
async def embarrass(message: discord.Message, client: CustomClient, *args):
    if len(args) == 0:
        webhook = await client.webhook_manager.get_webhook(message.channel)
        await webhook.send(random.choice(embarrassing_phrases),
                           username=message.author.display_name,
                           avatar_url=message.author.avatar_url)
    else:
        message.channel.send('This isn\'t implemented yet. Maybe in the next version')
        raise NotImplemented


@command(name='funfact',
         description='Get a fun fact from Craig',
         explanation='Get a fun fact about Home Depot:tm: from Craig')
async def funfact_command(message: discord.Message, client: CustomClient, *args):
    await message.channel.send(random.choice(fun_facts))


@command(name='dadjoke',
         description='Have Craig tell you a dad joke')
async def dadjoke_command(message: discord.Message, client: CustomClient, *args):
    await message.channel.send(random.choice(dad_jokes))


@command(name='advice',
         description='Get Craig\'s advice')
async def advice_command(message: discord.Message, client: CustomClient, *args):
    await message.channel.send(random.choice(advice))


@command(name='help',
         description='This help text',
         explanation='This command is used to view information about all commands, or detailed information about a command',
         usage=' [command]')
async def help_command(message: discord.Message, client: CustomClient, *args):
    try:
        command = commands[args[0]]
    except (KeyError, IndexError):
        help_text = f'Craig _v{client.version}_\n\nCommands:'
        command_list = []
        for command in sorted(commands.values(), key=lambda i: i.name):
            command_list.append(f'\n    {client.prefix}**{command.name}**: {command.description}')
        help_text += ''.join(command_list)
        help_text += '\n\nUse c!help [command] to get help for a specific command'
        await message.channel.send(help_text)
    else:
        help_text = f'{client.prefix}**{command.name}**\n{command.explanation}'

