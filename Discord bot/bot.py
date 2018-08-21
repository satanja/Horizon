import discord
from discord.ext import commands
from scraper import getInfo
import tokenfile

#Constants
TEAM = "Team Horizon"

client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
  print ("started")

@client.command()
async def pro():
  await client.say(getInfo(1, TEAM))

@client.command()
async def semi():
  await client.say(getInfo(2, TEAM))

@client.command()
async def amateur():
  await client.say(getInfo(3, TEAM))


client.run(tokenfile.TOKEN)