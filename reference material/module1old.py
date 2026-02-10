# main crawler functionality (sole purpose)
# -----------------

# import sys
import requests
# import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse #, urljoin

def getAllMainLinksFromURL(currentURL):
    retrievedURLs = []

    try:
        r = requests.get(currentURL, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        for link in soup.find_all('a'):
            path = link.get('href')

            if path and path.startswith('/'):
                # path = urljoin(currentURL, path)
                # retrievedURLs.append(path)
                retrievedURLs.append(currentURL)
            else:
                domain = urlparse(f"{path}").netloc
                retrievedURLs.append(domain)

    except:
        print("something bad happened for this url: " + currentURL)

    try:
        uniqueURLs = turnListIntoSetVersa(retrievedURLs)
    except:
        uniqueURLs = retrievedURLs

    return uniqueURLs


def turnListIntoSetVersa(listOfSorts):
    setBetween = set(listOfSorts)
    listAgain = list(setBetween)

    return listAgain

