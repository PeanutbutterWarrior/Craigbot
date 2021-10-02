import discord
import os.path
import random

with open(os.path.normpath('commands/fun_facts.txt')) as file:
    fun_facts = file.read().splitlines()


async def funfact(message: discord.Message):
    await message.channel.send(random.choice(fun_facts))
