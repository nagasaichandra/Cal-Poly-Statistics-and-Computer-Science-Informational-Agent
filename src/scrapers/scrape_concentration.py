import requests
from bs4 import BeautifulSoup
import urllib3
import re
from ..database_connection import make_connection


def scrapeConcentration():
    """Variables : [concentration-required-courses], [concentration-list]"""
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

    concentration_list = ['Interactive Entertainment Concentration']
    final_dict['concentration-required-courses'] = courses
    final_dict['concentration-list'] = concentration_list
    return final_dict


def scrapeMinorCourses():
    '''Variables: [minor-courses]'''
    final_dict = {}
    urllib3.disable_warnings()
    url1 = "http://catalog.calpoly.edu/collegesandprograms/collegeofengineering/computersciencesoftwareengineering/computerscienceminor/"
    myRequest1 = requests.get(url1, verify=False)
    soup1 = BeautifulSoup(myRequest1.text, "html.parser")
    url2 = "http://www.catalog.calpoly.edu/collegesandprograms/collegeofsciencemathematics/statistics/crossdisciplinarystudiesminordatascience/"
    myRequest2 = requests.get(url2, verify=False)
    soup2 = BeautifulSoup(myRequest2.text, "html.parser")
    url3 = "http://catalog.calpoly.edu/collegesandprograms/collegeofengineering/computersciencesoftwareengineering/computingforinteractiveartsminor/"
    myRequest3 = requests.get(url3, verify=False)
    soup3 = BeautifulSoup(myRequest3.text, "html.parser")
    # print(soup1.get_text())
    match = re.search(r'(Required Courses .*)', soup1.get_text())
    #print(match.group())
    cs_minor_courses = match.group()
    # print(soup2.get_text())
    match = re.search(r'(.* Total units\d\d)', soup2.get_text())
    #print(match.group())
    ds_minor_courses = match.group()
    # print(soup3.get_text())
    match = re.search(r'(Required Courses .*)', soup3.get_text())
    #print(match.group())
    ia_minor_courses = match.group()
    final_dict['CS minor'] = cs_minor_courses
    final_dict['Data Science minor'] = ds_minor_courses
    final_dict['Computing for Interactive Arts minor'] = ia_minor_courses

    return final_dict


def ingest_minor_courses(minor_courses):
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE minor_courses;')
            for minor in minor_courses:
                cursor.execute('''INSERT INTO minor_courses VALUES (%s, %s);''',
                               (minor, minor_courses[minor]))
                connection.commit()
    finally:
        connection.close()


def ingest_concentration(concentrations):
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE concentration;')
            cursor.execute('INSERT INTO concentration '
                           '(concentration_required_courses, concentration_list)'
                           ' VALUES (%s, %s)', (','.join(concentrations['concentration-required-courses']),
                                                    concentrations['concentration-list']))
            connection.commit()
    finally:
        connection.close()



def scrape_concentration():
    # scrapeConcentration()
    minor_courses = scrapeMinorCourses()
    ingest_minor_courses(minor_courses)
    ingest_concentration(scrapeConcentration())

if __name__ == '__main__':
    scrape_concentration()
