import os
import discord

with open('.env') as env_file:
    for line in env_file.read().split('\n'):
        key, val = line.split('=')
        os.environ[key] = val

TOKEN = os.getenv('DISCORD_TOKEN')

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
client.run(TOKEN)
