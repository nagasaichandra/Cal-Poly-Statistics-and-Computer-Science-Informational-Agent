import os
import sys
import random
import requests
from bs4 import BeautifulSoup
import re
import bleach
import pandas as pd
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# function that filters vowels
def filterMinStandards(line):
    exclude = ['[', '', 'Minimum Standards']
    if (line not in exclude):
        return True
    else:
        return False


def filterProcess(line):
    exclude = ['[', ']', '']
    if (line not in exclude):
        return True
    else:
        return False


def scrapeChangeMajor():
    finalDict = {}
    minStandardsList = []
    processList = []
    initialList = []

    #obtain the content of the URL in HTML
    url = "https://eadvise.calpoly.edu/changing-majors-to-csc-se-or-cpe/"
    myRequest = requests.get(url, verify=False)

    #Create a soup object that parses the HTML
    soup = BeautifulSoup(myRequest.text, "html.parser")

    #Print the HTML Title
    # print("Page Title: ",soup.head.title.get_text())

    for changeRow in soup.find_all('div', attrs={"id": "mainLeftFull"}):
        initialList.append(changeRow)

    initialList = re.split(
        r"<h3><strong>Process<\/strong><\/h3>", str(initialList))

    minStandardsList = str(bleach.clean(initialList[0], tags=[], strip=True))
    processList = str(bleach.clean(initialList[1], tags=[], strip=True))

    minStandardsList = filter(
        filterMinStandards, minStandardsList.splitlines())
    processList = filter(
        filterProcess, processList.splitlines())
    
    # print('\n'.join(list(minStandardsList)))
    # print(
    tempList  ='\n'.join(list(processList))
        # )
    # print(tempList)
    matchObj = re.search(r"\(all GPAs at least a (\d+\.\d+)\)", tempList)
    
    # if matchObj:
    #     print(matchObj.group(1))

    # [change-major-steps], [change-major-criteria], [minimum-gpa-change-major]
    finalDict['change-major-criteria'] = '\n'.join(list(minStandardsList))
    finalDict['change-major-steps'] = '\n'.join(list(processList))
    finalDict['minimum-gpa-change-major'] = matchObj.group(1)

    return finalDict


if __name__ == "__main__":
    print(scrapeChangeMajor())

