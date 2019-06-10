import requests
from bs4 import BeautifulSoup
import urllib3
import re
#from ..database_connection import make_connection


def scrapeConcentration():
    """Scrapes variables [[CSSE-mission-statement], [major-PEOs], [major-learning-Outcomes-List], [GE-learning-outcomes], [major-Learning-Outcomes-List], [ms-learning-objectives]
    """
    final_dict = {}
    urllib3.disable_warnings()
    url1 = "http://catalog.calpoly.edu/collegesandprograms/collegeofengineering/computersciencesoftwareengineering/bscomputerscience/interactiveentertainmentconcentration/"
    myRequest1 = requests.get(url1, verify=False)
    soup = BeautifulSoup(myRequest1.text, "html.parser")
    courses = []
    matches = soup.find_all('td')
    for match in matches:
        a_matches = match.find_all('a')
        for a_match in a_matches:
            courses.append(a_match['title'].replace(u'\xa0', ' '))
    print(courses)
    concentration_list = ['Interactive Entertainment Concentration']
    final_dict['concentration-required-courses'] = courses
    final_dict['concentration-list'] = concentration_list
    return final_dict



def scraper():
    scrapeConcentration()


if __name__ == '__main__':
    scraper()
