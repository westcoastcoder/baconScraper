# Import necessary modules
from bs4 import BeautifulSoup
import requests
import re

# Create Global Variables
welcomeMsg = """
Hello! Welcome to the BaconScraper.
Please enter a wiki link that you'd like to start with.
"""

# Welcome user to program and request input
print(welcomeMsg)
url = input()

# request html from user url
html = requests.get(url)

# Make our soup
soup = BeautifulSoup(html.content, 'html.parser')

# Pulls the actual text (not anchors/tags content) from the html using
# the .get_text() function
bodyCon = soup.find(id='bodyContent').get_text()

# This is the regex used to search our soup for bacon
bacFinder = re.compile(r'Kevin Bacon')

# Search of the website's text for bacon
bacon = bacFinder.findall(bodyCon)

# Let the user know if the page mentions KB at all
if len(bacon) > 0:
    print("\nKevin Bacon is mentioned on this page!\n")
else:
    print("\nIt doesn't look like Kevin Bacon is mentioned here...\n")

# bodyAnch = soup.find(id='bodyContent').find_all('a')
