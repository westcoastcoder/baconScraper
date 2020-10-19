# Import necessary modules
from bs4 import BeautifulSoup
import requests
import re
import sys
import sqlite3
import random
import time

# Create Global Variables
welcomeMsg = """
Hello! Welcome to the BaconScraper.
This program takes Wikipedia links as input and tells you
whether or not Kevin Bacon is mentioned.

First, do you want to use the auto-crawler? (y/n)
"""

secMessage = """
Okay, got it!
Please enter a wiki link that you'd like to start with.
"""

crawlCount = 0


# Create Bacon Database
def Baconbase(url, soup, bacRadar):
    conn = sqlite3.connect("baconscraper.sqlite", isolation_level=None)
    cur = conn.cursor()

    # Create table if necessary
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Baconpages (
        page_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        page_title TEXT UNIQUE,
        page_link TEXT UNIQUE,
        bacon_found TEXT)
    ''')

    page_title = soup.find(id="firstHeading")
    page_title = page_title.text
    print("Added " + page_title + " to the Baconbase.\n")

    templink = url.find('/wiki/')
    page_link = url[templink:]

    dbSQL = ("""INSERT OR IGNORE INTO\
    Baconpages (page_title, page_link, bacon_found) VALUES (?,?,?)""")

    cur.execute(dbSQL, (page_title, page_link, bacRadar))


# Create Crawler Function
def crawlForBacon(url, soup):
    """Optional Crawler to find more wikipedia pages that mention Bacon"""

    # Bring in the global counter var
    global crawlCount
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

    # randomly shuffle the available wiki links
    random.shuffle(baconLinks)
    # adjust counter
    crawlCount += 1
    print(crawlCount)
    # make sure our crawler doesn't move too fast
    time.sleep(1)
    if crawlCount < 21:
        print(baconLinks[0])
        scrapeForBacon("https://en.wikipedia.org" + baconLinks[0], 'y')
    else:
        print("Crawl complete!")


# Create Scrape Function
def scrapeForBacon(url, crawler):
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
        bacRadar = 'Bacon Found'
    else:
        print("\nIt doesn't look like Kevin Bacon is mentioned here...\n")
        bacRadar = 'No Bacon'

    # Update the bacon database
    Baconbase(url, soup, bacRadar)
    # If User has requested crawl, then call crawlfunc
    crawler = True if crawler == 'y' else False

    if crawler is True:
        crawlForBacon(url, soup)


# Welcome user to program and request input
print(welcomeMsg)
crawler = input()
if crawler not in ('y', 'n'):
    print("Invalid command. Use 'y' or 'n'.")
    sys.exit(1)
print(secMessage)
url = input()

scrapeForBacon(url, crawler)

# Scrape out sentences that mention Kevin Bacon and
# return each sentence to user in the form of a page summary
# sentenceFind = re.compile(r'[^.]Kevin Bacon[^.]*\.')
# sentencebac = sentenceFind.findall(bodyCon)
# print(bodyCon)
# for line in sentencebac:
#    print(line)
# On further research, this is a pretty complex issue (e.g. how do
# you define what a sentence is?).
