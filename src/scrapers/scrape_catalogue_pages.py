import requests
from bs4 import BeautifulSoup
import re
from ..database_connection import make_connection


def scrape_page(url, program_name):
    myRequest1 = requests.get(url, verify=False)
    soup = BeautifulSoup(myRequest1.text, "html.parser")

    courses = []
    matches = soup.find_all('tr')
    course_type = "Required Course"
    for match in matches:
        if match.find('span'):
            type = match.find('span').text
            if re.match(r'^Approved', type, flags = re.I):
                course_type = "Approved Elective"
            elif re.match(r'^Required', type, flags = re.I):
                course_type = "Required Course"
            elif re.match(r'^Technical|^Select\sTechnical', type, flags = re.I):
                course_type = "Technical Elective"
            elif re.match(r'^Support', type, flags = re.I):
                course_type = "Support Course"
        a_match = match.find('a')
        if a_match:
            course_num = a_match['title'].replace(u'\xa0', ' ')
            courses.append((program_name, course_num, course_type))

    return courses

def scrape_pages():
    url_se = "http://catalog.calpoly.edu/collegesandprograms/collegeofengineering/computersciencesoftwareengineering/bssoftwareengineering/"
    url_cs = "http://catalog.calpoly.edu/collegesandprograms/collegeofengineering/computersciencesoftwareengineering/bscomputerscience/"
    url_cs_minor = "http://catalog.calpoly.edu/collegesandprograms/collegeofengineering/computersciencesoftwareengineering/computerscienceminor/"
    url_data_science = "http://www.catalog.calpoly.edu/collegesandprograms/collegeofsciencemathematics/statistics/crossdisciplinarystudiesminordatascience/"
    url_cia = "http://catalog.calpoly.edu/collegesandprograms/collegeofengineering/computersciencesoftwareengineering/computingforinteractiveartsminor/"
    url_ie_concentration = "http://catalog.calpoly.edu/collegesandprograms/collegeofengineering/computersciencesoftwareengineering/bscomputerscience/interactiveentertainmentconcentration/"

    courses = []
    courses.extend(scrape_page(url_se, "SE"))
    courses.extend(scrape_page(url_cs, "CSC"))
    courses.extend(scrape_page(url_cs_minor, "CSC minor"))
    courses.extend(scrape_page(url_data_science, "Data Science minor"))
    courses.extend(scrape_page(url_cia, "CIA"))
    courses.extend(scrape_page(url_ie_concentration, "IE"))
    return courses

def ingest_catalogues(courses):
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('''TRUNCATE TABLE catalogues;''')
        connection.commit()

        with connection.cursor() as cursor:
            for course in courses:
                cursor.execute(
                    '''INSERT INTO catalogues (program_name, course_id, course_type) 
                    VALUES (%s, %s, %s);''', (course[0], course[1], course[2]))
            connection.commit()

    finally:
        connection.close()

def scrape_catalogues():
    courses = scrape_pages()
    ingest_catalogues(courses)


if __name__ == "__main__":
    scrape_catalogues()
