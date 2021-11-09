import discord
import os

from dotenv import load_dotenv

load_dotenv()

#Authenticate to Discord
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following server:\n'
        f'{guild.name}(id: {guild.id})'
    )

async def on_proposal():
    channel = await client.fetch_channel(906169022268182611)
    await channel.send("@everyone Beep boop! New r/Ethtrader Governance Poll: ")

client.run(TOKEN)
