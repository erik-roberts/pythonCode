# Instructions:
# 1) Create an account at "boardgamegeek.com"
# 2) Add all of your games to your collection
# 3) Install python3
# 4) Use pip3 to install 'requests', `pip3 install requests`
# 5) Edit 'bggUsername' below
# 6) The code waits 1 sec by default between each game in the found collection out of respect to the BGG servers and to prevent getting your IP banned. However, this number, 'sleepTime', can be reduced, which may be ideal for larger collections. The site robots.txt file requests a 5 sec delay, but I've used a 0 and .1 sec delay without issues in the past. Do so at your own risk though.


############## EDIT ############

# Insert your board game geek username as string below:
bggUsername = ''

# Time between requests to BGG server for each game
sleepTime = 1 # sec delay

##################################
import xml.etree.ElementTree as ET
import requests
from time import sleep

class Game:
    def __init__(self):
        self.bgName = ''
        self.bggID = None
        self.value = 0

    def __str__(self):
        return self.bgName

# get xml from url
url = 'http://www.boardgamegeek.com/xmlapi2/collection?username=' + bggUsername + '&own=1&marketplace=1'
r = requests.get(url)
xmlFile = r.text

# parse xml
items = ET.fromstring(xmlFile)

# if need to wait for server processing collection
if items.find('message'):
    sleep(10)
    r = requests.get(url)
    xmlFile = r.text
    
    # parse xml
    items = ET.fromstring(xmlFile)
    
totalValue = 0
nItems = len(items)
numGamesMissingValue = 0
collection = []

for (ind, item) in enumerate(items):
    print('Game ({}/{}), ETA to completion: {:.1f} min'.format(ind+1,nItems, (nItems-ind)*sleepTime/60 ) )
    
    game = Game()

    game.bgName = item.find('name').text
    game.objectid = item.get('objectid')

    sleep(sleepTime)

    # get game specific xml and parse
    gameURL = 'http://boardgamegeek.com/xmlapi2/thing?id=' + game.objectid + '&marketplace=1'
    gameXmlFile = requests.get(gameURL).text

    #try:
    
    # parse gameXml
    gameItems = ET.fromstring(gameXmlFile)
    gameItem = gameItems[0]

    # get category, mechanics
    if gameItem.find('marketplacelistings'):
        for listing in gameItem.find('marketplacelistings'):
            if listing.find('price').get('currency') == 'USD':
                game.value = float(listing.find('price').get('value'))
                break

    if game.value == 0:
        numGamesMissingValue += 1

    totalValue += game.value

    collection.append(game)
    
print('')
print( 'Estimated Game Collection Value = ${:.2f} (Based on current BGG market prices)'.format(totalValue) )
print( 'Note: {:.1f}% of collection not accounted for in total value'.format(numGamesMissingValue/nItems *100) )