import sys
import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Voer starturl in (zoals bijvoorbeeld: "https://kranten.startpagina.nl")
urlStart = "https://www.startpagina.nl"

def get_links_from_url(currentURL):
    retrievedURLs = []

    try:
        r = requests.get(currentURL, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        for link in soup.find_all('a'):
            path = link.get('href')
            
            if path and path.startswith('/'):
                path = urljoin(currentURL, path)
                retrievedURLs.append(path)
            else:
                retrievedURLs.append(path)

    except:
        print("something bad happened for this url: " + currentURL)
    
    return retrievedURLs

def check_for_doubles(fileToCheckName, checkingNr):
    originalFile = read_from_file(fileToCheckName)

    fileSetForm = set()
    
    for line in originalFile:
        fileSetForm.add(line)
    
    newList = []

    for item in fileSetForm:
        newList.append(item)

    write_to_file(newList, 'uniqueKranten' + str(checkingNr) + '.txt', False)

    return 'uniqueKranten' + str(checkingNr)

# --- read and write to/from file

def read_from_file(nameFile):
    with open(nameFile + '.txt', 'r') as fileIn:
        textFileInput = fileIn.readlines()
        return textFileInput

def write_to_file(listOfStrings, nameFile, boolForEndline):
    with open(nameFile, 'a') as fileOut:
        for singleString in listOfStrings:
            try: 
                if (singleString != "") and boolForEndline == True:
                    fileOut.writelines(str(singleString) + '\n')
                elif (singleString != "") and boolForEndline == False:
                    fileOut.writelines(str(singleString))
                else:
                    print("didn't write this line")
            except:
                fileOut.writelines("encountered error during printing this line\n")

def attempt_to_remove_empty_lines(nameFile):
    with open(nameFile + '.txt') as reader, open(nameFile + '.txt', 'r+') as writer:
        for line in reader:
            if line.strip():
                writer.write(line)
            writer.truncate()

    return nameFile

# --- loops

def startInitialLoop():
    result = get_links_from_url(urlStart)
    write_to_file(result, 'krantenlinks.txt')

    return 'krantenlinks'

def furtherLoop(loopFile, loopNr):
    inputList = read_from_file(loopFile)

    result = []

    for link in inputList:
        print(link)
        result.append(get_links_from_url(link))

    for links in result:
        write_to_file(links, 'krantenlinks' + str(loopNr) + '.txt', True)
    
    returnString = 'krantenlinks' + str(loopNr)

    return returnString

def mainLoop():
    # ronde 1 --------------------------------------------
    fileName = startInitialLoop()
    nextFileName = check_for_doubles(fileName, 1)
    # ronde 2 --------------------------------------------
    nextFileName = furtherLoop(nextFileName, 1)
    nextFileName = check_for_doubles(nextFileName, 2)
    # een eventuele ronde 3 ------------------------------

    # nextFileName = furtherLoop(nextFileName, 2)
    # nextFileName = check_for_doubles(nextFileName, 3)
    
    # resultaat ------------------------------------------
    print("latest results written in file: " + nextFileName + ".txt")

mainLoop()