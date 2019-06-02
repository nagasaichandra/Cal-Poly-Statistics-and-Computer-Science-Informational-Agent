import requests
import re
import bleach
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
    Scrapes:
        transfer-min-units
        transfer-articulate-courses
        CSSE-transfer-guidelines
        major-transfer-course-list
"""
def getTag(row ,string):
    retList = []
    for single in row:
        if single.find(string) != None and single.find(string) != -1:
            retList.append(single.find(string))
    return retList
    

def getTagAttrs(row, string, attr, field):
    retList = []
    for single in row:
        if single.find(string, attrs={str(attr): str(field)}) != None and single.find(string, attrs={str(attr) : str(field)}) != -1:
            retList.append(single.find(string, attrs={str(attr): str(field)}))
    return retList


def cleanHtml(string):
    return bleach.clean(string, tags=[], strip=True)


def scrapeTransfer():
    finalDict = {}
    articulatesHtml = []

    #obtain the content of the URL in HTML
    url = "https://admissions.calpoly.edu/computer-science.html"

    myRequest = requests.get(url, verify=False)

    #Create a soup object that parses the HTML
    soup = BeautifulSoup(myRequest.text, "html.parser")

    # gather data
    for transferRow in soup.find_all('div', attrs={"class": "field-item even"}):
        transferUnitsHtml = getTag(transferRow, 'u')
        articulatesHtml = transferRow.find_all('td', attrs={"width": "700"})
        generalGuidesHtml = transferRow.find_all('p')
        bulletsHtml = transferRow.find_all('li')
    
    # clean up and split courses
    articulates = "\n".join(list(map(cleanHtml, articulatesHtml)))
    articulates = re.split(
        r"Major Related 1\*", str(articulates))
    
    matchObj = re.search(r"(Selection.*alone\.)",
                         "\n".join(list(map(cleanHtml, generalGuidesHtml))))

    finalDict['transfer-min-units'] = cleanHtml(transferUnitsHtml[0])
    finalDict['transfer-articulate-courses'] = articulates[1]
    finalDict['CSSE-transfer-guidelines'] = matchObj.group(1) 
    # + "\n" + cleanHtml(bulletsHtml)
    finalDict['major-transfer-course-list'] = "Major Related 1*\n" + articulates[0]
    return finalDict


if __name__ == "__main__":
    # print(scrapeTransfer())
    final = scrapeTransfer()
    print(final['CSSE-transfer-guidelines'])
