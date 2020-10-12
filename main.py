# Import necessary modules
from bs4 import BeautifulSoup
import requests

# Create Global Variables
welcomeMsg = """
Hello! Welcome to the BaconScraper. Please enter a wiki link that you'd like to
start with \n
"""

# Welcome user to program and request input
print(welcomeMsg)
url = input()

# request html from user url
html = requests.get(url)
