import requests
from bs4 import BeautifulSoup
import re
from ..database_connection import make_connection


def parse_course(course_tag):
    ''' This function requires a tag for each class block and it returns
    a dictionary of the attributes of the class passed.'''
    course_dict = {}
    class_tag = course_tag.find('p', attrs={'class': 'courseblocktitle'})
    course_complete = class_tag.find('strong').text

    course_name_re = re.search(r'[0-9]{3}\. ([^.\n]*)\.', course_complete)
    if course_name_re:
        course_name = course_name_re.group(1)
        course_dict['course_name'] = course_name

    course_num_re = re.search(r'([1-5][0-9][0-9])', course_complete)
    if course_num_re:
        course_num = course_num_re.group(1)
        course_dict['course_num'] = course_num

    units_text = class_tag.find('span', attrs={'class': re.compile('courseblockhours')}).text
    units_re = re.search(r'([1-9]+)', units_text)

    if units_re:
        units_num = units_re.group(1)
        course_dict['units'] = units_num

    course_desc_tag = course_tag.find('div', attrs={'class': re.compile('courseblockdesc')})
    if course_desc_tag:
        course_dict['course_desc'] = course_desc_tag.text.replace('\n', '')

    course_offered_tag = course_tag.find('p', attrs={'class': 'noindent'})
    if course_offered_tag:
        course_offered_text = course_offered_tag.text
        course_offered_list = re.findall(r'(F|W|SP|SU|TBD)[,]?', course_offered_text)
        course_dict['offered_in'] = course_offered_list

    return course_dict


def parse_courses():
    url = "http://catalog.calpoly.edu/coursesaz/csc/"
    myRequest = requests.get(url)
    soup = BeautifulSoup(myRequest.text, "html.parser")
    courses = soup.find_all('div', attrs={'class': 'courseblock'})
    courses_dicts = list(map(parse_course, courses))
    return courses_dicts


def ingest_courses(courses):
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            for course_dict in courses:
                cursor.execute(
                    '''INSERT INTO course (course_number, course_area, course_name, 
                    course_description, course_units) VALUES (%s, %s, %s, %s, %s);''', (int(course_dict['course_num']),
                                                                                   'CSC', course_dict['course_name'],
                                                                                   course_dict['course_desc'],
                                                                                   int(course_dict['units']),))
            connection.commit()
    finally:
        connection.close()


def ingest_offered_in(courses):
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            for course in courses:
                if course['offered_in']:
                    for quarter in course['offered_in']:
                        cursor.execute(
                            '''INSERT INTO offered_in (course_number, course_area, quarter_id) VALUES (%s, %s, %s);''',
                            (course['course_num'], 'CSC', quarter,))
            connection.commit()
    finally:
        connection.close()


def remove_content():
    '''Removes all rows from the courses table.  '''
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('''TRUNCATE TABLE course;''')
            cursor.execute('''TRUNCATE TABLE offered_in;''')
            connection.commit()
    finally:
        connection.close()


def scrape_catalog():
    courses = parse_courses()
    remove_content()
    ingest_courses(courses)
    ingest_offered_in(courses)


if __name__ == '__main__':
    scrape_catalog()
