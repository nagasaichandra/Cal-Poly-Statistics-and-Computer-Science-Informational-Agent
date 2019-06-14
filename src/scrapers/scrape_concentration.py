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

def scrape_minor(url):
    myRequest1 = requests.get(url, verify=False)
    soup = BeautifulSoup(myRequest1.text, "html.parser")

    courses = []
    matches = soup.find_all('td')
    course_type = "Required Course"
    for match in matches:
        if match.find('span'):
            type = match.find('span').text
            if re.match(r'^Approved', type, flags = re.I):
                course_type = "Approved Elective"
            elif re.match(r'^Required', type, flags = re.I):
                course_type = "Required Course"
            elif re.match(r'^Technical', type, flags = re.I):
                course_type = "Technical Elective"
            elif re.match(r'^Free', type, flags = re.I):
                course_type = "Free Elective"
        a_matches = match.find_all('a')
        for a_match in a_matches:
            courses.append(a_match['title'].replace(u'\xa0', ' '))
    return courses



def scrapeMinorCourses():
    '''Variables: [minor-courses]'''
    final_dict = {}
    url1 = "http://catalog.calpoly.edu/collegesandprograms/collegeofengineering/computersciencesoftwareengineering/computerscienceminor/"
    url2 = "http://www.catalog.calpoly.edu/collegesandprograms/collegeofsciencemathematics/statistics/crossdisciplinarystudiesminordatascience/"
    url3 = "http://catalog.calpoly.edu/collegesandprograms/collegeofengineering/computersciencesoftwareengineering/computingforinteractiveartsminor/"

    final_dict['CSC minor'] = ', '.join(scrape_minor(url1))
    final_dict['Data Science minor'] = ', '.join(scrape_minor(url2))
    final_dict['CIA'] = ', '.join(scrape_minor(url3))
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
