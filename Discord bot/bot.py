import discord
from discord.ext import commands
from scraper import getInfo
import tokenfile
import leagueColors

#Constants
TEAM = "Team Horizon"

client = commands.Bot(command_prefix = '!')

# returns the teams in a string
def formatTeams(teams):
  return "**" + teams[0] + " vs " + teams[1] + "**"

# returns the information in a string
def formatInfo(info):
  return "\n".join(info)

def formatMaps(maps):
  result = ""
  for i in range(0, 5):
    if (i == 4):
      result += "[ACE]: "
    else:
      result += "[" + str(i + 1) + "]: "
    result += maps[i] + "\n"
  return result

def generateEmbed(color, type, team):

  details = getInfo(type, team)

  embed = None
  if isinstance(details, str):
    color = 0xff0000
    embed = discord.Embed(title = details, color = color)
  else:
    title = formatTeams(details[0])
    desc = formatInfo(details[1])
    maps = formatMaps(details[2])
    embed = discord.Embed(title = title, description = desc, color = color)
    embed.add_field(name = "**Maps**", value = maps)
  return embed

@client.event
async def on_ready():
  print ("started")

@client.command()
async def pro():
  color = leagueColors.PRO
  await client.say(embed = generateEmbed(color, 1, TEAM))

@client.command()
async def semipro():
  color = leagueColors.SEMIPRO
  await client.say(embed = generateEmbed(color, 2, TEAM))

@client.command()
async def amateur():
  color = leagueColors.AMATEUR
  await client.say(embed = generateEmbed(color, 3, TEAM))

client.run(process.env.BOT_TOKEN)