# [ms-learning-objectives], [required-ms-units], [ms-total-units], [approved-ms-elective-units],[thesis-ms-units], [graduate-ms-units]
import requests
import re
import bleach
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def getCourses(courseNames):
    tempList = []
    returnList = []

    for course in courseNames:
        if 'CSC' in course:
            tempList.append(course)

    lastElement = tempList.pop()

    for course in tempList:
        returnList.append(''.join([i for i in course[7:] if not i.isdigit()]))

    return returnList

def scrapeMasters():
    finalDict = {}
    learnObjectives = []
    units = []
    courseTable = []
    courseNames = []

    #obtain the content of the URL in HTML
    url = "http://catalog.calpoly.edu/collegesandprograms/collegeofengineering/computersciencesoftwareengineering/mscomputerscience/"

    myRequest = requests.get(url, verify=False)

    #Create a soup object that parses the HTML
    soup = BeautifulSoup(myRequest.text, "html.parser")

    #Print the HTML Title
    # print("Page Title: ",soup.head.title.get_text())

    for mastersRow in soup.find_all('div', attrs={"id": "textcontainer"}):
        learnHtml = mastersRow.find('ol')
        unitsHtml = mastersRow.find('p')
        courseTableHtml = mastersRow.find('tbody')
        
        for row in mastersRow.find_all('tr', attrs={"class": "odd"}):
            courseNames.append(bleach.clean(row, tags=[], strip=True))
        for row in mastersRow.find_all('tr', attrs={"class": "even"}):
            courseNames.append(bleach.clean(row, tags=[], strip=True))


        learnObjectives.append(bleach.clean(learnHtml, tags=[], strip=True))
        units.append(bleach.clean(unitsHtml, tags=[], strip=True))
        courseTable.append(bleach.clean(courseTableHtml, tags=[], strip=True))

    courseNames = getCourses(courseNames)
    matchUnits = re.search(r"(\d+ units)", units[0])
    matchElectiveUnits = re.search(
        r"Selected with Graduate Coordinator approval 2(\d+)", courseTable[0])
    thesisUnits = re.search(r"Thesis(\d+)", courseTable[0])

    finalDict['ms-learning-objectives'] = learnObjectives[0]
    finalDict['required-ms-units'] = matchUnits.group(1)
    finalDict['ms-total-units'] = matchUnits.group(1)
    finalDict['approved-ms-elective-units'] = matchElectiveUnits.group(1)
    finalDict['thesis-ms-units'] = thesisUnits.group(1)
    finalDict['graduate-ms-units'] = matchUnits.group(1)
    finalDict['ms-course-names'] = courseNames
    
    return finalDict

if __name__ == "__main__":
    print(scrapeMasters())
    # scrapeMasters()
