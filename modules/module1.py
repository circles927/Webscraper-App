# module1, redefined using youtube video tips

import requests, gzip, xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import urllib.robotparser as robotparser

def getAllMainLinksFromURL(currentURL):
    # Attempt to retrieve and print links from the given URL
    try:
        r = requests.get(currentURL, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')

        for link in soup.find_all('a'):
            # Searches the link
            path = link.get('href')

            if path and path.startswith('/'):
                # Just display main url if path is relative to main domain
                yield currentURL
            else:
                # Cut the link to the main domain name only
                domain = urlparse(f"{path}").netloc
                yield domain

    except:
        print("something bad happened for this url: " + currentURL)

def turnListIntoSetVersa(listOfSorts):
    # Turns a list into a set and back to a list to remove duplicates
    setBetween = set(listOfSorts)
    listAgain = list(setBetween)

    return listAgain