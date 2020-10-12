# Import necessary modules
from bs4 import BeautifulSoup
import requests
import re

# Create Global Variables
welcomeMsg = """
Hello! Welcome to the BaconScraper. Please enter a wiki link that you'd like to start with. \n
"""

# Welcome user to program and request input
print(welcomeMsg.lstrip())
url = input()

# request html from user url
html = requests.get(url)

# make our soup
soup = BeautifulSoup(html.content, 'html.parser')

# get the body content
body = soup.find_all(id='bodyContent')

bodyDiv = soup.find(id='bodyContent').get_text()
bacFinder = re.compile(r'Bacon')
bacon = bacFinder.findall(bodyDiv)
bodyAnch = soup.find(id='bodyContent').find_all('a')

#divBacon = bodyDiv.get_text()
print(bacon)
print("******************************************************")
#print(bodyAnch)
# check our soup for bacon
# divBacon = body.find_all("div", string="Sedgwick was nominated", recursive=True)
# tagBacon = body.find_all('a')

#print(body)
