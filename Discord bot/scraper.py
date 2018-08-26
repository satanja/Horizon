import requests
import string
from bs4 import BeautifulSoup

# Constants
URL = "https://alpha.tl/"


# parsedPage = BeautifulSoup(page, 'html.parser')

def tournamentSelect(type):
  switcher = {
    1: "europro",
    2: "eurosemipro",
    3: "euroamateur"
  }
  return switcher.get(type, "invalid tournament type")

# parses the webpage using BeautifulSoup
def soupify(url):
  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')
  return soup

# finds the calendar of the webpage (output only <a> tags)
def getCalendar(url):
  soup = soupify(url)
  completeCalendar = list(soup.find(id="content"))[3]
  calendar = list(completeCalendar.find_all('a'))
  return calendar

# if no matches found: return 0
# if no matches remaining: return 1
# if there exists a match to be played: return url
def findNextTeamMatch(calendar, team):
  matchList = []
  # find all instances of the matches the team has to play
  for entry in calendar:
    leftTeam = entry.find(class_="tablecol colw160 txtlgnright").get_text()
    rightTeam = entry.find(class_="tablecol colw160 txtlgnleft").get_text()
    if leftTeam == team or rightTeam == team:
      matchList.append(entry)
  
  if len(matchList) == 0:
    # no matches found that contain the team
    return 0
  else:
    for match in matchList:
      matchstatus = match.find(class_="tablecol colw55").get_text()
      print(matchstatus)
      if matchstatus == "-":
        # Found an uncompleted match
        # Return url
        return match['href']
    # No uncompleted match remaining
    return 1

# Finds the both teams of the match and returns them in an array
def getTeams(url):
  matchPage = soupify(url)
  teams = []
  teamElements = list(matchPage.find_all(class_ = "matchclan"))
  for teamElement in teamElements:
    teams.append(teamElement.get_text())
  return teams

# Finds the date, time, and chat channel on the webpage.
# The are returned in an array together with the url of the webpage
def getBasicInfo(url):
  matchPage = soupify(url)
  info = []
  infoElements = list(matchPage.find_all(class_="matchinfo-info"))
  for i in range(0, 3):
    info.append(infoElements[i].get_text())
  info.append(url)
  return info

# Finds the maps of the match and returns them in an array
def getMaps(url):
  matchPage = soupify(url)
  maps = []
  mapElements = list(matchPage.find_all(class_="match-pregame-map"))
  for mapElement in mapElements:
    mapString = string.capwords(mapElement.get_text().lower())
    maps.append(mapString)
  return maps

# Returns all the information of the next match the team has to play
# if there exists a next match:
#   details[0] contains the teams
#   details[1] contains the basic info of the match (date, time, etc)
#   details[2] contains the maps
# otherwise:
#   return a string
def getInfo(type, team):
  #navigate to the tournament page
  if (type < 1 or type > 3):
    print("Invalid type")
  else: 
    url = URL + tournamentSelect(type)
    calendarPage = getCalendar(url)
    nextMatch = findNextTeamMatch(calendarPage, team)
    if nextMatch == 0:
      return "Your team is not signed up"
    elif nextMatch == 1:
      return "No matches remain to be played"
    else:
      details = []
      details.append(getTeams(nextMatch))
      details.append(getBasicInfo(nextMatch))
      details.append(getMaps(nextMatch))
      return details