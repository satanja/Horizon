import requests
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

# Returns all the details of the match
# url must correspond to a match page
def getDetailsMatchPage(url):
  matchPage = soupify(url)
  message = []
  #Get the teams
  teams = list(matchPage.find_all(class_="matchclan"))
  message.append("**" + teams[0].get_text() + " vs " + teams[1].get_text() + "**")
  
  #Get the info
  info = list(matchPage.find_all(class_="matchinfo-info"))
  counter = 0
  for infoEntry in info:
    if counter < 3:
      message.append(infoEntry.get_text())
      counter += 1
  
  #Add seperation
  message.append("")

  #Get the maps
  message.append("**Maps:**")
  maps = list(matchPage.find_all(class_="match-pregame-map"))
  counter = 1
  for map in maps:
    if counter == 5:
      message.append("[ACE]: " + map.get_text().lower())
    else:
      message.append("[" + "{}".format(counter) + "]: " + map.get_text().lower())
      counter += 1
 
  return message

def getInfo(type, team):
  #navigate to the tournament page
  if (type < 1 or type > 3):
    print("Invalid type")
  else: 
    #TODO remove 
    print(URL + tournamentSelect(type))

    url = URL + tournamentSelect(type)
    calendarPage = getCalendar(url)
    nextMatch = findNextTeamMatch(calendarPage, team)
    if nextMatch == 0:
      return "Your team is not signed up"
    elif nextMatch == 1:
      return "No matches remain to be played"
    else:
      message = [nextMatch]
      details = getDetailsMatchPage(nextMatch)
      message.extend(details)
      return "\n".join(message)