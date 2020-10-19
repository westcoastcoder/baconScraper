# Import necessary modules
from bs4 import BeautifulSoup
import requests
import re
import sys
import sqlite3

# Create Global Variables
welcomeMsg = """
Hello! Welcome to the BaconScraper.
Please enter a wiki link that you'd like to start with.
"""


# Create Bacon Database
def Baconbase(url, soup):
    conn = sqlite3.connect("baconscraper.sqlite", isolation_level=None)
    cur = conn.cursor()

    # Create table if necessary
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Baconpages (
        page_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        page_title TEXT UNIQUE,
        page_link TEXT UNIQUE)
    ''')

    page_title = soup.find(id="firstHeading")
    page_title = page_title.text

    templink = url.find('/wiki/')
    page_link = url[templink:]

    dbSQL = ("""INSERT OR IGNORE INTO\
    Baconpages (page_title, page_link) VALUES (?,?)""")

    cur.execute(dbSQL, (page_title, page_link))

# Create Crawler Function
def crawlForBacon(url, soup):
    """Optional Crawler to find more wikipedia pages that mention Bacon"""
    tags = soup.find(id='bodyContent').find_all('a')

    baconLinks = []

    for tag in tags:
        try:
            # We only want wikipedia links (no external links)
            # and links that are fun (not deadends)
            if (tag['href'].find("/wiki/") != -1
                    and tag['href'].find("https://") != 0
                    and tag['href'].find("/Category:") == -1
                    and tag['href'].find("(identifier)") == -1
                    and tag['href'].find("/File:") == -1
                    and tag['href'].find("/Help:") == -1
                    and tag['href'].find("Special:BookSources") == -1
                    and tag['href'].find("/Template:") == -1):
                baconLinks.append(tag['href'])
        # This is to catch any errors where an href attribute is not present
        except KeyError:
            print("Error: No href attribute present in 'a' tag.")
            continue


# Create Scrape Function
def scrapeForBacon(url):
    """scrape to determine if Kevin Bacon is mentioned"""

    # Confirm link is to a Wikipedia page - exit if not
    if re.search(r'wikipedia',  url.lower()) is None:
        print("\nThat doesn't look like a Wikipedia link...")
        print("Try again with a Wikipedia link!")
        sys.exit(1)

    # request html from user url
    html = requests.get(url)

    # Make our soup
    soup = BeautifulSoup(html.content, 'html.parser')

    # Pulls the actual text (not anchors/tags content) from the html using
    # the .get_text() function
    bodyCon = soup.find(id='bodyContent').get_text()
    # print(bodyCon)

    # This is the regex used to search our soup for bacon
    bacFinder = re.compile(r'Kevin Bacon')

    # Search of the website's text for bacon
    bacon = bacFinder.findall(bodyCon)
    # print(bacon)

    # Let the user know if the page mentions KB at all
    if len(bacon) > 0:
        print("\nKevin Bacon is mentioned on this page!\n")
    else:
        print("\nIt doesn't look like Kevin Bacon is mentioned here...\n")

    # Scrape out sentences that mention Kevin Bacon and
    # return each sentence to user in the form of a page summary
    # sentenceFind = re.compile(r'[^.]Kevin Bacon[^.]*\.')
    # sentencebac = sentenceFind.findall(bodyCon)
    # print(bodyCon)
    # for line in sentencebac:
    #    print(line)
    # On further research, this is a pretty complex issue (e.g. how do
    # you define what a sentence is?).

    # bodyAnch = soup.find(id='bodyContent').find_all('a')
    Baconbase(url, soup)


# Welcome user to program and request input
print(welcomeMsg)
url = input()
scrapeForBacon(url)
