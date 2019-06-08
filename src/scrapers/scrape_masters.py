import requests
import re
import bleach
import urllib3
from bs4 import BeautifulSoup
from ..database_connection import make_connection
from ..data_sustainer import DataSustainer


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


"""
    Scrapes:
    [ms-learning-objectives]
    [required-ms-units]
    [ms-total-units]
    [approved-ms-elective-units]
    [thesis-ms-units]
    [graduate-ms-units]
    ['blended-benefits']
    ['blended-requirements']
    ['blended-description']
"""


def get_courses(course_names):
    temp_list = []
    return_list = []

    for course in course_names:
        if 'CSC' in course:
            temp_list.append(course)

    last_element = temp_list.pop()

    for course in temp_list:
        return_list.append(''.join([i for i in course[7:] if not i.isdigit()]))

    return return_list


def scrape_masters():
    ms_url = '''http://catalog.calpoly.edu/collegesandprograms/collegeofengineering/computersciencesoftwareengineering/mscomputerscience/'''
    final_dict = {}
    learn_objectives = []
    units = []
    course_table = []
    course_names = []

    # obtain the content of the URL in HTML
    my_request = requests.get(ms_url, verify=False)

    # Create a soup object that parses the HTML
    soup = BeautifulSoup(my_request.text, "html.parser")

    # Print the HTML Title
    # print("Page Title: ",soup.head.title.get_text())

    for mastersRow in soup.find_all('div', attrs={"id": "textcontainer"}):
        learn_html = mastersRow.find('ol')
        units_html = mastersRow.find('p')
        course_table_html = mastersRow.find('tbody')

        for row in mastersRow.find_all('tr', attrs={"class": "odd"}):
            course_names.append(bleach.clean(row, tags=[], strip=True))
        for row in mastersRow.find_all('tr', attrs={"class": "even"}):
            course_names.append(bleach.clean(row, tags=[], strip=True))

        learn_objectives.append(bleach.clean(learn_html, tags=[], strip=True))
        units.append(bleach.clean(units_html, tags=[], strip=True))
        course_table.append(bleach.clean(course_table_html, tags=[], strip=True))

    course_names = get_courses(course_names)
    match_units = re.search(r"(\d+ units)", units[0])
    match_elective_units = re.search(
        r"Selected with Graduate Coordinator approval 2(\d+)", course_table[0])
    thesis_units = re.search(r"Thesis(\d+)", course_table[0])

    final_dict['ms-learning-objectives'] = learn_objectives[0]
    final_dict['required-ms-units'] = match_units.group(1)
    final_dict['ms-total-units'] = match_units.group(1)
    final_dict['approved-ms-elective-units'] = match_elective_units.group(1)
    final_dict['thesis-ms-units'] = thesis_units.group(1)
    final_dict['graduate-ms-units'] = match_units.group(1)
    final_dict['ms-course-names'] = ', '.join(course_names)

    remove_masters()
    ingest_masters(final_dict)

    return final_dict


def scrape_blended():
    final_dict = {}

    # Intends to scrape variables [blended-requirements], [blended-description], [blended-benefits]

    url1 = "http://catalog.calpoly.edu/collegesandprograms/collegeofengineering/computersciencesoftwareengineering/#blendedbsmstext"
    url2 = "http://catalog.calpoly.edu/graduateeducation/#generalpoliciesgoverninggraduatestudiestext"
    url0 = "https://csc.calpoly.edu/programs/"

    my_request0 = requests.get(url0, verify=False)
    my_request1 = requests.get(url1, verify=False)
    my_request2 = requests.get(url2, verify=False)

    soup0 = BeautifulSoup(my_request0.text, "html.parser")
    soup1 = BeautifulSoup(my_request1.text, "html.parser")
    soup2 = BeautifulSoup(my_request2.text, "html.parser")

    blended_benefits = list()

    match = re.search(r'Blended Program Benefits\n\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n\nGraduate', soup0.get_text())
    for i in range(1, 7):
        blended_benefits.append(match.group(i))
    final_dict['blended-benefits'] = blended_benefits

    match = re.search(r'Eligibility\n\n(.*\n.*\n.*\n.*\n.*\n)\nProcess to Graduate with Both Degrees', soup2.get_text())
    general_eligibility = match.group(1)

    match = re.search(r'(Majors that are eligible for the blended program are:\n\n.*\n.*\n.*\n\n)Participation',
                      soup1.get_text())
    cs_blended_eligible_majors = match.group(1)
    blended_requirements = cs_blended_eligible_majors + general_eligibility

    final_dict['blended-requirements'] = blended_requirements

    match = re.search(r"Blended Bachelor's \+ Master's Programs\nOverview\n(.*\n.*\n.*\n)Eligibility", soup2.get_text())
    final_dict['blended-description'] = (match.group(1))

    return final_dict


def ingest_masters(masters):
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO masters VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s");',
                (masters['ms-learning-objectives'],
                    masters[
                        'required-ms-units'],
                    masters[
                        'ms-total-units'],
                    masters[
                        'approved-ms-elective-units'],
                    masters[
                        'thesis-ms-units'],
                    masters[
                        'graduate-ms-units'],
                    masters[
                        'ms-course-names']))
            connection.commit()
    finally:
        connection.close()

def ingest_blended(blended):
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO blended VALUES ("%s", "%s", "%s");',
                (blended['blended-benefits'],
                    blended[
                        'blended-requirements'],
                    blended[
                        'blended-description']))
            connection.commit()
    finally:
        connection.close()


def remove_masters():
    """Removes all rows from the courses table.  """
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('''TRUNCATE TABLE masters;''')
            # cursor.execute('''TRUNCATE TABLE blended;''')
            connection.commit()
    finally:
        connection.close()


def remove_blended():
    """Removes all rows from the courses table.  """
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            # cursor.execute('''TRUNCATE TABLE masters;''')
            cursor.execute('''TRUNCATE TABLE blended;''')
            connection.commit()
    finally:
        connection.close()


if __name__ == "__main__":
    masters = scrape_masters()
    blended = scrape_blended()
    # data_sustainer = DataSustainer()
    # data_sustainer.create_tables(filename="createTableBlended.sql")

    # remove_masters()
    # ingest_masters(masters)
    remove_blended()
    ingest_blended(blended)
