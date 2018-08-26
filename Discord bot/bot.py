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
      result += "[" + str(i) + "]: "
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

  #embed = discord.Embed(title="Next alpha teamleauge match", description="", color=0xE67E22)
  #embed.add_field(name="Basic info", value="test")
  #embed.add_field(name="Maps", value = getInfo(1, TEAM))
  #await client.say(embed = embed)

@client.command()
async def semipro():
  color = leagueColors.SEMIPRO
  await client.say(embed = generateEmbed(color, 2, TEAM))

  #embed = discord.Embed(title="Next alpha teamleauge match", description="", color=0x3498DB)
  #embed.add_field(name="Basic info", value="test")
  #embed.add_field(name="Maps", value = getInfo(2, TEAM))
  #await client.say(embed = embed)

@client.command()
async def amateur():
  color = leagueColors.AMATEUR
  await client.say(embed = generateEmbed(color, 3, TEAM))

  #embed = discord.Embed(title="Next alpha teamleauge match", description="", color=0x2ECC71)
  #embed.add_field(name="Basic info", value="test")
  #embed.add_field(name="Maps", value = getInfo(3, TEAM))
  #await client.say(embed = embed)



client.run(tokenfile.TOKEN)