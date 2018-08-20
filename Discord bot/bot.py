import discord
from discord.ext import commands

TOKEN = 'NDgxMDY4NDgyMTkyOTk4NDAw.DlxAtw.bIsvvp5ZDNdQBZ72O0GpdNZnN_U'

client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
  print ("started")

@client.command()
async def pro():
  await client.say('pro')

@client.command()
async def semi():
  await client.say('semi-pro')

@client.command()
async def amateur():
  await client.say('amateur')


client.run(TOKEN)